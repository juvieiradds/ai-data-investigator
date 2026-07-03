"""
Tests for the StoragePaths class in src.core.storage_paths.

Tests cover:
- Path resolution and construction
- Directory creation
- Date versioning for raw layer
- Flat structure for processed/warehouse layers
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from src.core.storage_paths import StoragePaths


class TestStoragePathsInitialization:
    """Test StoragePaths initialization and path resolution."""

    def test_storage_paths_initializes(self) -> None:
        """StoragePaths should initialize without error."""
        sp = StoragePaths()
        assert sp is not None

    def test_base_dirs_exist_as_properties(self) -> None:
        """Base directories should be accessible as properties."""
        sp = StoragePaths()
        assert isinstance(sp.raw_dir, Path)
        assert isinstance(sp.processed_dir, Path)
        assert isinstance(sp.warehouse_dir, Path)

    def test_base_dirs_end_with_correct_names(self) -> None:
        """Base directories should end with correct layer names."""
        sp = StoragePaths()
        assert sp.raw_dir.name == "raw"
        assert sp.processed_dir.name == "processed"
        assert sp.warehouse_dir.name == "warehouse"


class TestRawLayerVersioning:
    """Test raw layer date-based versioning (ADR 0002)."""

    def test_raw_dataset_with_date(self, test_ingestion_date: date) -> None:
        """raw_dataset() should include date in path."""
        sp = StoragePaths()
        path = sp.raw_dataset("test_dataset", ingestion_date=test_ingestion_date)

        # Path should contain date as directory
        assert "2026-07-03" in str(path)
        assert "test_dataset" in str(path)

    def test_raw_dataset_default_date_is_today(self) -> None:
        """raw_dataset() without date should use today's date."""
        sp = StoragePaths()
        path = sp.raw_dataset("test_dataset")

        # Should contain today's date
        today_str = date.today().isoformat()
        assert today_str in str(path)

    def test_raw_dataset_format_iso_8601(self, test_ingestion_date: date) -> None:
        """raw_dataset() should format date as YYYY-MM-DD (ISO 8601)."""
        sp = StoragePaths()
        path = sp.raw_dataset("test_dataset", ingestion_date=test_ingestion_date)

        # Check ISO format: 2026-07-03
        path_str = str(path)
        assert "2026-07-03" in path_str
        # Should NOT have other formats like 07/03/2026 or 03-07-2026
        assert "07/03" not in path_str


class TestProcessedAndWarehouseLayers:
    """Test processed and warehouse layers (flat structure)."""

    def test_processed_dataset_no_date_in_path(self) -> None:
        """processed_dataset() should NOT include date."""
        sp = StoragePaths()
        path = sp.processed_dataset("test_dataset")

        # Should not contain date patterns
        path_str = str(path)
        assert "2026-07-03" not in path_str
        assert "processed" in path_str
        assert "test_dataset" in path_str

    def test_warehouse_dataset_no_date_in_path(self) -> None:
        """warehouse_dataset() should NOT include date."""
        sp = StoragePaths()
        path = sp.warehouse_dataset("test_dataset")

        # Should not contain date patterns
        path_str = str(path)
        assert "2026-07-03" not in path_str
        assert "warehouse" in path_str
        assert "test_dataset" in path_str


class TestDirectoryCreation:
    """Test directory creation methods (sanity checks)."""

    def test_ensure_dirs_method_exists(self) -> None:
        """ensure_dirs() method should be callable."""
        sp = StoragePaths()
        # Should not raise
        sp.ensure_dirs()

    def test_ensure_dataset_dirs_method_exists(self) -> None:
        """ensure_dataset_dirs() method should be callable."""
        sp = StoragePaths()
        # Should not raise
        sp.ensure_dataset_dirs("test_dataset")


class TestPathStructure:
    """Test overall path structure compliance with architecture."""

    def test_paths_follow_medallion_architecture(
        self, test_ingestion_date: date
    ) -> None:
        """Paths should follow Medallion Architecture (raw→processed→warehouse)."""
        sp = StoragePaths()

        raw_path = sp.raw_dataset("states", ingestion_date=test_ingestion_date)
        processed_path = sp.processed_dataset("states")
        warehouse_path = sp.warehouse_dataset("states")

        # All should contain dataset name
        assert "states" in str(raw_path)
        assert "states" in str(processed_path)
        assert "states" in str(warehouse_path)

        # Raw should have date, others should not
        assert "2026-07-03" in str(raw_path)
        assert "2026-07-03" not in str(processed_path)
        assert "2026-07-03" not in str(warehouse_path)

        # Each should be in their respective layer
        assert "raw" in str(raw_path)
        assert "processed" in str(processed_path)
        assert "warehouse" in str(warehouse_path)
