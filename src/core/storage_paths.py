"""
Centralized storage path management.

This module provides a single source of truth for the physical location of the
project's data layers defined by ADR 0002 (Medallion Architecture).

Responsibilities:
- Resolve project data directories.
- Expose raw, processed, and warehouse paths.
- Create directory structures when necessary.

Non-responsibilities:
- Reading or writing files.
- Executing DuckDB queries.
- Managing dataset contents.

Those responsibilities belong to the ETL layer and the database facade
(core/database.py) defined in ADR 0003.
"""

from datetime import date
from pathlib import Path
from typing import Optional


class StoragePaths:
    """
    Centralized management of project data layer paths.

    The class abstracts the physical layout of the project's data directory,
    allowing the rest of the application to remain independent from filesystem
    organization.

    Directory structure:

    project_root/
    ├── data/
    │   ├── raw/
    │   ├── processed/
    │   └── warehouse/
    └── src/

    Attributes
    ----------
    base_dir : Path
        Project root directory.

    data_dir : Path
        Root directory containing all data layers.
    """

    RAW_LAYER = "raw"
    PROCESSED_LAYER = "processed"
    WAREHOUSE_LAYER = "warehouse"

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        """
        Initialize storage paths.

        Parameters
        ----------
        base_dir : Path, optional
            Project root directory.

            If omitted, the project root is automatically inferred
            from the current file location.
        """

        if base_dir is None:
            # storage_paths.py
            # └── core/
            #     └── src/
            #         └── project_root/
            base_dir = Path(__file__).resolve().parent.parent.parent

        self.base_dir = Path(base_dir)
        self.data_dir = self.base_dir / "data"

    # ------------------------------------------------------------------
    # Base layer directories
    # ------------------------------------------------------------------

    @property
    def raw_dir(self) -> Path:
        """Return the root directory of the raw layer."""
        return self.data_dir / self.RAW_LAYER

    @property
    def processed_dir(self) -> Path:
        """Return the root directory of the processed layer."""
        return self.data_dir / self.PROCESSED_LAYER

    @property
    def warehouse_dir(self) -> Path:
        """Return the root directory of the warehouse layer."""
        return self.data_dir / self.WAREHOUSE_LAYER

    # ------------------------------------------------------------------
    # Dataset-specific helpers
    # ------------------------------------------------------------------

    def raw_dataset(
        self,
        dataset_name: str,
        ingestion_date: Optional[date] = None,
    ) -> Path:
        """
        Return the directory for a dataset snapshot inside the raw layer,
        versioned by ingestion date to preserve immutability (ADR 0002).

        Parameters
        ----------
        dataset_name : str
            Dataset identifier.

        ingestion_date : date, optional
            Snapshot date. Defaults to today's date.

        Example
        -------
        data/raw/ibge_localidades/2026-07-03/
        """

        if ingestion_date is None:
            ingestion_date = date.today()

        return self.raw_dir / dataset_name / ingestion_date.isoformat()

    def processed_dataset(self, dataset_name: str) -> Path:
        """
        Return the directory for a dataset inside the processed layer.

        Example
        -------
        data/processed/ibge_localidades/
        """
        return self.processed_dir / dataset_name

    def warehouse_dataset(self, dataset_name: str) -> Path:
        """
        Return the directory for a dataset inside the warehouse layer.

        Example
        -------
        data/warehouse/ibge_localidades/
        """
        return self.warehouse_dir / dataset_name

    # ------------------------------------------------------------------
    # Directory creation
    # ------------------------------------------------------------------

    def ensure_dirs(self) -> None:
        """
        Create the three Medallion data layers if they do not exist.
        """

        for directory in (
            self.raw_dir,
            self.processed_dir,
            self.warehouse_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)

    def ensure_dataset_dirs(self, dataset_name: str) -> None:
        """
        Create dataset directories for processed and warehouse layers.

        The raw layer is intentionally excluded because each ingestion
        generates an immutable snapshot versioned by date (ADR 0002).
        Creation of the raw snapshot directory is the responsibility of
        the ETL pipeline, which knows the ingestion date or batch identifier.

        Example
        -------
        data/
            processed/
                ibge_localidades/
            warehouse/
                ibge_localidades/
        """

        for directory in (
            self.processed_dataset(dataset_name),
            self.warehouse_dataset(dataset_name),
        ):
            directory.mkdir(parents=True, exist_ok=True)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"base_dir='{self.base_dir}', "
            f"data_dir='{self.data_dir}')"
        )
