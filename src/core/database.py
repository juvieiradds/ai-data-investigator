"""
Database abstraction layer (Facade pattern).

This module provides a unified interface for all data operations across
the Medallion architecture (raw, processed, warehouse), abstracting away
DuckDB implementation details.

Responsibilities (ADR 0003):
- Manage DuckDB connections
- Execute queries with structured error handling
- Read/write tables across all data layers
- Provide audit logging of all operations

Non-responsibilities:
- Managing file paths (belongs to StoragePaths)
- Data transformation logic (belongs to ETL)
"""

from __future__ import annotations

import logging
from datetime import date
from typing import Optional

import duckdb
import pandas as pd

from src.core.logging import get_logger
from src.core.storage_paths import StoragePaths


class DatabaseError(Exception):
    """Custom exception for database-related errors."""

    pass


class DataWarehouseConnection:
    """
    Facade for DuckDB operations across the Medallion architecture.

    Provides a high-level, type-safe interface for reading and writing
    data across raw, processed, and warehouse layers, with built-in
    error handling and audit logging.

    Attributes
    ----------
    storage_paths : StoragePaths
        Handles resolution of physical data paths.

    _connection : duckdb.DuckDBPyConnection
        Lazy-initialized DuckDB connection.

    _logger : logging.Logger
        Structured logger for audit trails.
    """

    def __init__(self, storage_paths: Optional[StoragePaths] = None) -> None:
        """
        Initialize the database facade.

        Parameters
        ----------
        storage_paths : StoragePaths, optional
            Path resolver. If omitted, a new instance is created.
        """
        self.storage_paths = storage_paths or StoragePaths()
        self._connection: Optional[duckdb.DuckDBPyConnection] = None
        self._logger = get_logger()

        # Ensure data directories exist
        self.storage_paths.ensure_dirs()
        self._logger.info("DataWarehouseConnection initialized")

    # =====================================================================
    # Connection Management
    # =====================================================================

    @property
    def connection(self) -> duckdb.DuckDBPyConnection:
        """
        Lazy-initialized DuckDB connection.

        Returns
        -------
        duckdb.DuckDBPyConnection
            Active database connection.
        """
        if self._connection is None:
            self._logger.info("Initializing DuckDB connection (in-memory)")
            self._connection = duckdb.connect(":memory:")
            # Configure DuckDB pragmas for performance
            # Performance tuning can be added later when needed
            # self._connection.execute("SET threads = 4")
            self._logger.debug("DuckDB connection initialized with pragmas")
        return self._connection

    def close(self) -> None:
        """Close the database connection."""
        if self._connection is not None:
            self._logger.info("Closing DuckDB connection")
            self._connection.close()
            self._connection = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    # =====================================================================
    # Query Execution
    # =====================================================================

    def execute_query(self, sql: str) -> duckdb.DuckDBPyRelation:
        """
        Execute a SQL query against the database.

        Parameters
        ----------
        sql : str
            SQL query to execute.

        Returns
        -------
        duckdb.DuckDBPyRelation
            Query result.

        Raises
        ------
        DatabaseError
            If the query execution fails.

        Example
        -------
        >>> result = db.execute_query("SELECT * FROM warehouse_states LIMIT 5")
        >>> df = result.to_df()
        """
        try:
            self._logger.debug(f"Executing query: {sql[:100]}...")
            relation = self.connection.execute(sql)
            self._logger.info("Query executed successfully")
            return relation
        except Exception as e:
            self._logger.error(f"Query execution failed: {str(e)}")
            raise DatabaseError(f"Query execution failed: {str(e)}") from e

    # =====================================================================
    # Table Operations (Read / Write)
    # =====================================================================

    def read_table(
        self,
        table_name: str,
        layer: str = "warehouse",
    ) -> pd.DataFrame:
        """
        Read a table from a specific layer.

        Parameters
        ----------
        table_name : str
            Name of the table to read.

        layer : str
            Data layer: 'raw', 'processed', or 'warehouse'.

        Returns
        -------
        pd.DataFrame
            Table contents as a Pandas DataFrame.

        Raises
        ------
        DatabaseError
            If the table does not exist or read fails.
        """
        try:
            self._logger.info(f"Reading table '{table_name}' from layer '{layer}'")
            sql = f"SELECT * FROM read_parquet('data/{layer}/**/{table_name}*.parquet')"
            relation = self.execute_query(sql)
            df = relation.to_df()
            self._logger.info(
                f"Successfully read table '{table_name}' "
                f"({len(df)} rows, {len(df.columns)} columns)"
            )
            return df
        except Exception as e:
            self._logger.error(f"Failed to read table '{table_name}': {str(e)}")
            raise DatabaseError(f"Failed to read table '{table_name}': {str(e)}") from e

    def write_table(
        self,
        table_name: str,
        data: pd.DataFrame,
        layer: str = "raw",
        dataset_name: Optional[str] = None,
        ingestion_date: Optional[date] = None,
    ) -> None:
        """
        Write a DataFrame to a specific layer as Parquet.

        Parameters
        ----------
        table_name : str
            Name of the table (used as filename).

        data : pd.DataFrame
            Data to write.

        layer : str
            Target layer: 'raw', 'processed', or 'warehouse'.

        dataset_name : str, optional
            Dataset identifier (for organizing raw/processed/warehouse).
            Required for all layers.

        ingestion_date : date, optional
            For raw layer, the snapshot date. Defaults to today.

        Raises
        ------
        DatabaseError
            If the write operation fails.
        ValueError
            If required parameters are missing.

        Example
        -------
        >>> import pandas as pd
        >>> from datetime import date
        >>> df = pd.read_json("data.json")
        >>> db.write_table(
        ...     "states",
        ...     df,
        ...     layer="raw",
        ...     dataset_name="ibge_localidades",
        ...     ingestion_date=date(2026, 7, 3)
        ... )
        """
        try:
            # Validate required parameter
            if dataset_name is None:
                raise ValueError(f"dataset_name is required for layer '{layer}'")

            # Determine output path based on layer
            if layer == "raw":
                output_dir = self.storage_paths.raw_dataset(
                    dataset_name,
                    ingestion_date,
                )
            elif layer == "processed":
                output_dir = self.storage_paths.processed_dataset(dataset_name)
            elif layer == "warehouse":
                output_dir = self.storage_paths.warehouse_dataset(dataset_name)
            else:
                raise ValueError(f"Invalid layer: {layer}")

            # Create directory if it doesn't exist
            output_dir.mkdir(parents=True, exist_ok=True)

            # Write as Parquet
            output_path = output_dir / f"{table_name}.parquet"

            self._logger.info(
                f"Writing table '{table_name}' to {layer}/{dataset_name} "
                f"({len(data)} rows, {len(data.columns)} columns)"
            )

            # Use DuckDB to write (more robust than pandas)
            self.connection.from_df(data).write_parquet(str(output_path))

            self._logger.info(f"Successfully wrote {output_path}")

        except (ValueError, OSError) as e:
            self._logger.error(f"Failed to write table '{table_name}': {str(e)}")
            raise DatabaseError(
                f"Failed to write table '{table_name}': {str(e)}"
            ) from e
        except Exception as e:
            self._logger.error(
                f"Unexpected error writing table '{table_name}': {str(e)}"
            )
            raise DatabaseError(
                f"Unexpected error writing table '{table_name}': {str(e)}"
            ) from e

    # =====================================================================
    # Utility Methods
    # =====================================================================

    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the database.

        Parameters
        ----------
        table_name : str
            Table name to check.

        Returns
        -------
        bool
            True if table exists, False otherwise.
        """
        try:
            self.connection.execute(
                f"SELECT 1 FROM information_schema.tables "
                f"WHERE table_name = '{table_name}' LIMIT 1"
            )
            return True
        except Exception:
            return False

    def list_tables(self) -> list[str]:
        """
        List all tables currently in the database.

        Returns
        -------
        list[str]
            List of table names, or empty list if none exist.
        """
        try:
            result = self.execute_query(
                "SELECT table_name FROM information_schema.tables ORDER BY table_name"
            )
            return [row[0] for row in result.fetchall()]
        except Exception as e:
            self._logger.error(f"Failed to list tables: {str(e)}")
            return []

    def get_table_info(self, table_name: str) -> pd.DataFrame:
        """
        Get schema information (column names and types) for a table.

        Parameters
        ----------
        table_name : str
            Table name.

        Returns
        -------
        pd.DataFrame
            Schema information with columns: name, type.

        Raises
        ------
        DatabaseError
            If table does not exist.
        """
        try:
            result = self.execute_query(f"DESCRIBE {table_name}")
            return result.to_df()
        except Exception as e:
            self._logger.error(f"Failed to get info for table '{table_name}'")
            raise DatabaseError(
                f"Failed to get info for table '{table_name}': {str(e)}"
            ) from e

    # =====================================================================
    # Representation
    # =====================================================================

    def __repr__(self) -> str:
        """String representation of the connection."""
        return (
            f"{self.__class__.__name__}("
            f"storage_paths={self.storage_paths}, "
            f"connected={self._connection is not None})"
        )
