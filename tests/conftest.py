"""
Pytest configuration and shared fixtures for the entire test suite.

This file contains fixtures that can be used by any test module in the project.
Fixtures are automatically discovered by pytest and reused across test files.
"""

from __future__ import annotations

import tempfile
from datetime import date
from pathlib import Path
from typing import Generator

import pandas as pd
import pytest


@pytest.fixture
def temp_data_dir() -> Generator[Path, None, None]:
    """
    Create a temporary directory for test data.

    Yields a Path to a temporary directory that is cleaned up after the test.
    Useful for testing file I/O without polluting the actual data directory.

    Yields
    ------
    Path
        Temporary directory path

    Example
    -------
    >>> def test_something(temp_data_dir):
    ...     test_file = temp_data_dir / "test.txt"
    ...     test_file.write_text("hello")
    ...     assert test_file.exists()
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_states_dataframe() -> pd.DataFrame:
    """
    Create a sample DataFrame mimicking IBGE states API response.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: id, sigla, nome, regiao
        Contains 3 sample Brazilian states

    Example
    -------
    >>> def test_validate(sample_states_dataframe):
    ...     assert len(sample_states_dataframe) == 3
    ...     assert "id" in sample_states_dataframe.columns
    """
    return pd.DataFrame(
        {
            "id": [35, 33, 31],
            "sigla": ["SP", "RJ", "MG"],
            "nome": ["São Paulo", "Rio de Janeiro", "Minas Gerais"],
            "regiao": [
                {"id": 3, "sigla": "SE", "nome": "Sudeste"},
                {"id": 3, "sigla": "SE", "nome": "Sudeste"},
                {"id": 3, "sigla": "SE", "nome": "Sudeste"},
            ],
        }
    )


@pytest.fixture
def sample_cleaned_states() -> pd.DataFrame:
    """
    Create a sample cleaned states DataFrame (post-normalization).

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: id, sigla, nome (regiao removed)
        Contains 3 sample states with no nested objects

    Example
    -------
    >>> def test_cleaned(sample_cleaned_states):
    ...     assert "regiao" not in sample_cleaned_states.columns
    ...     assert len(sample_cleaned_states.columns) == 3
    """
    return pd.DataFrame(
        {
            "id": [35, 33, 31],
            "sigla": ["SP", "RJ", "MG"],
            "nome": ["São Paulo", "Rio de Janeiro", "Minas Gerais"],
        }
    )


@pytest.fixture
def test_ingestion_date() -> date:
    """
    Return a fixed test date for reproducible tests.

    Returns
    -------
    date
        Fixed date: 2026-07-03

    Example
    -------
    >>> def test_versioning(test_ingestion_date):
    ...     assert test_ingestion_date == date(2026, 7, 3)
    """
    return date(2026, 7, 3)


@pytest.fixture
def mock_ibge_api_response() -> list[dict]:
    """
    Create a mock IBGE API response (JSON-like).

    Returns
    -------
    list[dict]
        List of state dictionaries as returned by IBGE API

    Example
    -------
    >>> def test_fetch(mock_ibge_api_response):
    ...     assert len(mock_ibge_api_response) == 3
    ...     assert mock_ibge_api_response[0]["sigla"] == "SP"
    """
    return [
        {
            "id": 35,
            "sigla": "SP",
            "nome": "São Paulo",
            "regiao": {"id": 3, "sigla": "SE", "nome": "Sudeste"},
        },
        {
            "id": 33,
            "sigla": "RJ",
            "nome": "Rio de Janeiro",
            "regiao": {"id": 3, "sigla": "SE", "nome": "Sudeste"},
        },
        {
            "id": 31,
            "sigla": "MG",
            "nome": "Minas Gerais",
            "regiao": {"id": 3, "sigla": "SE", "nome": "Sudeste"},
        },
    ]
