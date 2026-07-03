"""
Tests for the IBGE Localidades ETL pipeline in src.etl.ibge_localidades.

Tests cover:
- API fetch functionality (mocked)
- Schema validation
- Data cleaning/normalization
- Full pipeline orchestration
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

from src.etl.ibge_localidades import (
    clean_and_normalize,
    fetch_states_from_ibge,
    ingest_ibge_localidades,
    validate_schema,
)


class TestFetchStatesFromIBGE:
    """Test fetch_states_from_ibge() function."""

    def test_fetch_with_mocked_api(self, mock_ibge_api_response: list[dict]) -> None:
        """fetch_states_from_ibge() should return DataFrame with correct shape."""
        with patch("src.etl.ibge_localidades.requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_ibge_api_response

            df = fetch_states_from_ibge()

            assert isinstance(df, pd.DataFrame)
            assert len(df) == 3
            assert "id" in df.columns
            assert "sigla" in df.columns

    def test_fetch_calls_correct_url(self, mock_ibge_api_response: list[dict]) -> None:
        """fetch_states_from_ibge() should call the correct IBGE endpoint."""
        with patch("src.etl.ibge_localidades.requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_ibge_api_response

            fetch_states_from_ibge()

            # Verify the correct URL was called
            mock_get.assert_called_once()
            call_args = mock_get.call_args
            assert "servicodados.ibge.gov.br" in str(call_args)


class TestValidateSchema:
    """Test validate_schema() function."""

    def test_validate_passes_with_all_columns(
        self, sample_states_dataframe: pd.DataFrame
    ) -> None:
        """validate_schema() should pass when all expected columns exist."""
        # Should not raise
        validate_schema(sample_states_dataframe)

    def test_validate_fails_with_missing_column(self) -> None:
        """validate_schema() should raise ValueError when columns are missing."""
        df = pd.DataFrame(
            {
                "id": [1, 2],
                "sigla": ["SP", "RJ"],
                # Missing 'nome' and 'regiao'
            }
        )

        with pytest.raises(ValueError):
            validate_schema(df)


class TestCleanAndNormalize:
    """Test clean_and_normalize() function."""

    def test_clean_removes_regiao_column(
        self, sample_states_dataframe: pd.DataFrame
    ) -> None:
        """clean_and_normalize() should remove 'regiao' column."""
        df_clean = clean_and_normalize(sample_states_dataframe)

        assert "regiao" not in df_clean.columns
        assert "id" in df_clean.columns
        assert "sigla" in df_clean.columns
        assert "nome" in df_clean.columns

    def test_clean_preserves_row_count(
        self, sample_states_dataframe: pd.DataFrame
    ) -> None:
        """clean_and_normalize() should keep same number of rows."""
        df_clean = clean_and_normalize(sample_states_dataframe)

        assert len(df_clean) == len(sample_states_dataframe)

    def test_clean_results_in_three_columns(
        self, sample_states_dataframe: pd.DataFrame
    ) -> None:
        """clean_and_normalize() should result in exactly 3 columns."""
        df_clean = clean_and_normalize(sample_states_dataframe)

        assert len(df_clean.columns) == 3


class TestIngestPipeline:
    """Test full ingest_ibge_localidades() pipeline."""

    def test_ingest_returns_tuple_with_count_and_path(
        self,
        mock_ibge_api_response: list[dict],
        test_ingestion_date: date,
    ) -> None:
        """ingest_ibge_localidades() should return (count, path) tuple."""
        with patch("src.etl.ibge_localidades.requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_ibge_api_response

            # Mock DataWarehouseConnection to use temp dir
            with patch("src.etl.ibge_localidades.DataWarehouseConnection") as mock_db:
                mock_instance = mock_db.return_value
                mock_instance.storage_paths.raw_dataset.return_value = Path(
                    "/tmp/test_path"
                )

                count, path = ingest_ibge_localidades(
                    ingestion_date=test_ingestion_date
                )

                assert isinstance(count, int)
                assert count == 3  # Mock has 3 records
                assert isinstance(path, str)

    def test_ingest_propagates_validation_error(self) -> None:
        """ingest_ibge_localidades() should propagate schema validation errors."""
        with patch("src.etl.ibge_localidades.requests.get") as mock_get:
            # Return data missing required columns
            mock_get.return_value.json.return_value = [
                {"id": 1, "sigla": "SP"}  # Missing 'nome' and 'regiao'
            ]

            with pytest.raises(ValueError):
                ingest_ibge_localidades()

    def test_ingest_calls_database_write(
        self,
        mock_ibge_api_response: list[dict],
        test_ingestion_date: date,
    ) -> None:
        """ingest_ibge_localidades() should call DataWarehouseConnection.write_table()."""
        with patch("src.etl.ibge_localidades.requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_ibge_api_response

            with patch("src.etl.ibge_localidades.DataWarehouseConnection") as mock_db:
                mock_instance = mock_db.return_value
                mock_instance.storage_paths.raw_dataset.return_value = Path(
                    "/tmp/test_path"
                )

                ingest_ibge_localidades(ingestion_date=test_ingestion_date)

                # Verify write_table was called
                mock_instance.write_table.assert_called_once()
