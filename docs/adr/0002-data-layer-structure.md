# 0002. Data Layer Structure (Medallion Architecture)

## Status

Accepted

---

## Context

AI Data Investigator ingests datasets from multiple heterogeneous public sources (IBGE, DataSUS, INEP, IBAMA, INMET), each with different formats (CSV, JSON, ZIP archives), update frequencies, and varying levels of data quality.

Without a clear separation between ingestion stages, transformation logic tends to become tightly coupled with raw source data, making it difficult to:

- audit errors introduced during transformation
- reprocess datasets after changes in business rules or cleaning logic
- trace analytical results back to their original raw inputs
- maintain reproducibility across pipeline executions

In a naive ETL approach (single-step transformation), raw data is often overwritten or immediately transformed, eliminating the ability to reconstruct intermediate states. This turns the pipeline into a "black box", where outputs cannot be reliably explained or debugged.

To ensure reproducibility, auditability, and maintainability, a structured multi-layer data architecture is required.

---

## Decision

We will adopt a **three-layer Medallion architecture** for all data processing workflows:

### Raw Layer (raw/)

- Stores data exactly as received from external sources
- Immutable after ingestion (never overwritten)
- Versioned by ingestion date or batch identifier
- Format: CSV, JSON, or original source format (unchanged)
- Serves as the single source of truth for audit and reprocessing

### Processed Layer (processed/)

- Contains cleaned and standardized datasets
- Data types normalized (dates, numerics, categories)
- Duplicates removed and schema validated
- Maintains row-level granularity (no aggregation)
- Format: Parquet (optimized for columnar processing with DuckDB)

### Warehouse Layer (warehouse/)

- Contains aggregated, analysis-ready datasets
- Joins multiple processed sources when needed
- Optimized for querying, analytics, and AI agent consumption
- Format: Parquet (high-performance analytical queries)

### Core Rules

- Raw data is NEVER modified after ingestion
- Each ingestion creates a new immutable snapshot in raw/
- Processed and warehouse layers are fully derived from raw data
- DuckDB operates primarily over processed and warehouse layers for analytical workloads

---

## Alternatives Considered

### Single-layer pipeline (no separation)

- All transformations applied directly to raw data in one step
- Simpler initial implementation
- ❌ Eliminates reproducibility and auditability
- ❌ Impossible to debug intermediate transformation errors
- ❌ Forces full recomputation for any logic change

### Two-layer model (raw + warehouse only)

- Raw data directly transformed into final analytical tables
- Reduces storage complexity
- ❌ Removes intermediate validation stage
- ❌ Couples cleaning logic with aggregation logic
- ❌ Reduces reusability of cleaned datasets for different analyses

---

## Consequences

### Positive

- Strong data lineage and reproducibility
- Easier debugging through separation of transformation stages
- Ability to reprocess data without losing original inputs
- Cleaner separation of concerns across ETL pipeline stages
- Aligns with modern data engineering practices (Medallion Architecture)

### Negative / Trade-offs

- Increased storage usage due to multiple data representations
- More complex ETL pipeline orchestration
- Slightly higher engineering overhead in early development
- Requires discipline to maintain immutability of raw layer
- More moving parts compared to single-step pipelines

---

## Architectural Impact (EXTENSION TO BE STANDARDIZED)

This section extends the base ADR template and will be standardized across all future ADRs.

- Establishes a clear Medallion architecture foundation for all datasets
- Defines strict separation between ingestion, processing, and analytics
- Enables DuckDB to operate efficiently on optimized Parquet layers
- Encourages reproducible, audit-friendly data engineering practices
- Provides structural foundation for future AI agent data consumption

---

## Summary

The Medallion architecture was adopted to ensure **reproducibility, auditability, and scalability of data workflows**, enabling a clear separation between raw ingestion, cleaned datasets, and analytical data products while maintaining compatibility with DuckDB-based analytics.
