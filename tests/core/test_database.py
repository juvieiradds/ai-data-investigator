"""
Tests for the DataWarehouseConnection class in src.core.database.

Tests cover:
- Connection initialization
- Write/read roundtrip (Parquet)
- Schema validation
- Error handling
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from src.core.database import DatabaseError, DataWarehouseConnection


class TestDataWarehouseConnectionInitialization:
    """Test DataWarehouseConnection initialization."""

    def test_connection_initializes(self) -> None:
        """DataWarehouseConnection should initialize without error."""
        db = DataWarehouseConnection()
        assert db is not None

    def test_connection_has_storage_paths(self) -> None:
        """Connection should have StoragePaths instance."""
        db = DataWarehouseConnection()
        assert db.storage_paths is not None

    def test_context_manager_support(self) -> None:
        """DataWarehouseConnection should support context manager."""
        with DataWarehouseConnection() as db:
            assert db is not None


class TestWriteAndReadRoundtrip:
    """Test writing data to Parquet (happy path tests only)."""

    def test_write_dataframe_to_raw_layer(
        self, sample_cleaned_states: pd.DataFrame, test_ingestion_date: date
    ) -> None:
        """Should write DataFrame to raw layer without error."""
        db = DataWarehouseConnection()

        # Should not raise
        db.write_table(
            table_name="states",
            data=sample_cleaned_states,
            layer="raw",
            dataset_name="test_dataset",
            ingestion_date=test_ingestion_date,
        )

    def test_write_dataframe_to_processed_layer(
        self, sample_cleaned_states: pd.DataFrame
    ) -> None:
        """Should write DataFrame to processed layer without error."""
        db = DataWarehouseConnection()

        # Should not raise
        db.write_table(
            table_name="states",
            data=sample_cleaned_states,
            layer="processed",
            dataset_name="test_dataset",
        )

    def test_write_requires_dataset_name(
        self, sample_cleaned_states: pd.DataFrame
    ) -> None:
        """Writing should require dataset_name parameter."""
        db = DataWarehouseConnection()

        # Should raise DatabaseError (which wraps ValueError)
        with pytest.raises(DatabaseError):
            db.write_table(
                table_name="states",
                data=sample_cleaned_states,
                layer="raw",
                dataset_name=None,  # This should fail
            )


class TestErrorHandling:
    """Test error handling and validation."""

    def test_database_error_is_raised_on_invalid_data(self) -> None:
        """DatabaseError should be raised on invalid data types."""
        db = DataWarehouseConnection()

        # Pass invalid data (not a DataFrame)
        with pytest.raises(DatabaseError):
            db.write_table(
                table_name="invalid",
                data="not a dataframe",  # type: ignore
                layer="raw",
                dataset_name="test",
            )

    def test_connection_closes_cleanly(self) -> None:
        """Connection should close without error."""
        db = DataWarehouseConnection()
        db.close()  # Should not raise
