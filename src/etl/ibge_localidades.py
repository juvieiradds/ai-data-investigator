"""
ETL pipeline for IBGE Localidades (Brazilian states and regions).

Downloads geographic and administrative data from IBGE public API and stores
it in the raw data layer following the Medallion architecture pattern.

API: https://servicodados.ibge.gov.br/api/v1/localidades/estados
"""

from __future__ import annotations

import logging
from datetime import date
from typing import Optional

import pandas as pd
import requests

from src.core.database import DatabaseError, DataWarehouseConnection
from src.core.logging import get_logger

# IBGE API Configuration
IBGE_BASE_URL = "https://servicodados.ibge.gov.br/api/v1/localidades"
STATES_ENDPOINT = f"{IBGE_BASE_URL}/estados"
DATASET_NAME = "ibge_localidades"

# Expected schema for IBGE states response
EXPECTED_COLUMNS = {"id", "sigla", "nome", "regiao"}


class IBGEFetchError(Exception):
    """Custom exception for IBGE API fetch failures."""

    pass


def fetch_states_from_ibge() -> pd.DataFrame:
    """
    Fetch Brazilian states data from IBGE public API.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: id, sigla, nome, regiao

    Raises
    ------
    IBGEFetchError
        If the API request fails or returns invalid data.

    Example
    -------
    >>> df = fetch_states_from_ibge()
    >>> print(df.shape)  # (27, 4)
    """
    logger = get_logger()

    try:
        logger.info(f"Fetching states from IBGE API: {STATES_ENDPOINT}")
        response = requests.get(STATES_ENDPOINT, timeout=10)
        response.raise_for_status()

        data = response.json()
        logger.debug(f"Received {len(data)} records from IBGE API")

        df = pd.DataFrame(data)
        logger.info(f"Successfully fetched {len(df)} states")

        return df

    except requests.RequestException as e:
        logger.error(f"IBGE API request failed: {str(e)}")
        raise IBGEFetchError(f"Failed to fetch states from IBGE: {str(e)}") from e
    except (ValueError, KeyError) as e:
        logger.error(f"Invalid JSON response from IBGE: {str(e)}")
        raise IBGEFetchError(f"IBGE response is not valid JSON: {str(e)}") from e


def validate_schema(df: pd.DataFrame) -> None:
    """
    Validate that the DataFrame contains all expected columns.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to validate

    Raises
    ------
    ValueError
        If any expected columns are missing

    Example
    -------
    >>> df = pd.DataFrame({"id": [1], "sigla": ["SP"], "nome": ["São Paulo"], "regiao": [{"id": 3, "sigla": "SE"}]})
    >>> validate_schema(df)  # Passes
    """
    logger = get_logger()

    missing_columns = EXPECTED_COLUMNS - set(df.columns)

    if missing_columns:
        logger.error(f"Missing columns: {missing_columns}")
        raise ValueError(f"DataFrame missing expected columns: {missing_columns}")

    logger.info(f"Schema validation passed. Columns: {set(df.columns)}")


def clean_and_normalize(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and normalize the raw DataFrame.

    Currently performs minimal transformations:
    - Ensure required columns are present and non-null

    Parameters
    ----------
    df : pd.DataFrame
        Raw DataFrame from IBGE API

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame

    Example
    -------
    >>> df = pd.DataFrame({"id": [1, 2], "sigla": ["SP", "RJ"], "nome": ["São Paulo", "Rio"], "regiao": [{}, {}]})
    >>> cleaned = clean_and_normalize(df)
    """
    logger = get_logger()

    # Keep only expected columns (ignore 'regiao' which is a dict)
    df_clean = df[["id", "sigla", "nome"]].copy()

    # Check for nulls in key fields
    null_count = df_clean.isnull().sum().sum()
    if null_count > 0:
        logger.warning(f"Found {null_count} null values in key fields")

    logger.info(
        f"Cleaned data: {len(df_clean)} records, {len(df_clean.columns)} columns"
    )

    return df_clean


def ingest_ibge_localidades(ingestion_date: Optional[date] = None) -> tuple[int, str]:
    """
    Main ETL pipeline: fetch, validate, clean, and store IBGE states data.

    Parameters
    ----------
    ingestion_date : date, optional
        Date to use for raw data versioning. If None, uses today's date.

    Returns
    -------
    tuple[int, str]
        (record_count, output_path) — number of records ingested and storage path

    Raises
    ------
    IBGEFetchError
        If API fetch fails
    ValueError
        If schema validation fails
    DatabaseError
        If database write fails

    Example
    -------
    >>> count, path = ingest_ibge_localidades()
    >>> print(f"Ingested {count} states to {path}")
    Ingested 27 states to C:\\...\\data\\raw\\ibge_localidades\\2026-07-03
    """
    logger = get_logger()

    if ingestion_date is None:
        ingestion_date = date.today()

    logger.info(f"Starting IBGE Localidades ETL pipeline (date: {ingestion_date})")

    try:
        # Step 1: Fetch
        df_raw = fetch_states_from_ibge()

        # Step 2: Validate schema
        validate_schema(df_raw)

        # Step 3: Clean and normalize
        df_clean = clean_and_normalize(df_raw)

        # Step 4: Store to raw layer
        db = DataWarehouseConnection()
        db.write_table(
            table_name="estados",
            data=df_clean,
            layer="raw",
            dataset_name=DATASET_NAME,
            ingestion_date=ingestion_date,
        )

        logger.info(
            f"ETL pipeline completed successfully. "
            f"Ingested {len(df_clean)} records to raw layer."
        )

        # Return stats
        output_path = str(db.storage_paths.raw_dataset(DATASET_NAME, ingestion_date))
        return len(df_clean), output_path

    except (IBGEFetchError, ValueError, DatabaseError) as e:
        logger.error(f"ETL pipeline failed: {str(e)}")
        raise


def main() -> None:
    """
    CLI entry point for the IBGE Localidades ETL pipeline.

    Runs the full pipeline and prints results to console.
    """
    from src.core.logging import configure_logging

    # Configure logging for standalone execution
    configure_logging(level=logging.INFO)
    logger = get_logger()

    try:
        count, path = ingest_ibge_localidades()
        logger.info(f"\n✅ SUCCESS: Ingested {count} states")
        logger.info(f"📁 Output path: {path}")
        print(f"\n✅ IBGE Localidades ETL completed!")
        print(f"   Records: {count}")
        print(f"   Location: {path}")

    except Exception as e:
        logger.error(f"\n❌ FAILED: {str(e)}")
        print(f"\n❌ ETL failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
