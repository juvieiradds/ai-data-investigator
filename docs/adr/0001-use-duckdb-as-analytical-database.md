# 0001. Use DuckDB as the analytical database

## TL;DR

DuckDB was chosen as the embedded analytical database engine to enable fast, local-first OLAP workloads without requiring server infrastructure, prioritizing simplicity and performance for data exploration.

## Status

Accepted

---

## Context

AI Data Investigator needs to ingest, process and analyze multiple Brazilian public datasets (IBGE, DataSUS, INEP, IBAMA, INMET).

These datasets have the following characteristics:

- Large tabular structures (CSV, Parquet)
- High read/analysis workload (OLAP-style queries)
- Low requirement for transactional consistency (OLTP is not the focus)
- Mostly batch ingestion rather than real-time writes
- Single-developer / local-first execution model (initially)

In this context, we need a database engine optimized for analytical workloads, easy local setup, and strong integration with Python data tools.

We also want to avoid early infrastructure complexity (running database servers, managing connections, migrations overhead) while still maintaining production-like architecture principles.

---

## Decision

We will use **DuckDB** as the primary analytical database engine for the project.

DuckDB will be responsible for:

- Querying large datasets locally
- Performing analytical SQL operations over Parquet/CSV files
- Supporting transformations in ETL pipelines
- Serving as the main compute engine for data analysis layers

PostgreSQL (introduced later) will be reserved for:

- User management
- Authentication data
- Application metadata
- Long-term persisted system state (if needed)

---

## Alternatives Considered

### PostgreSQL

- Industry standard relational database
- Strong concurrency support
- Mature ecosystem
- Suitable for production multi-user systems
- Requires server setup and operational overhead
- Overkill for local-first analytical workloads at early stage

### SQLite

- Extremely lightweight and embedded
- Zero configuration setup
- Good for small-scale applications
- Limited performance for large analytical workloads
- Weak parallel analytical query performance
- Not optimized for heavy OLAP-style processing

---

## Consequences

### Positive

- Simplifies local development (no database server required)
- Fast iteration on data pipelines and analytics workflows
- High performance for large dataset exploration
- Reduces infrastructure complexity in early stages
- Aligns with modern local-first data engineering practices

### Negative / Trade-offs

- Not suitable for concurrent write-heavy workloads
- Cannot replace PostgreSQL for multi-user transactional systems
- Requires migration strategy if system evolves into OLTP needs
- Some SQL dialect differences vs PostgreSQL
- Not designed for distributed computing

---

## Architectural Impact (EXTENSION TO BE STANDARDIZED)

This section is an **explicit architectural extension beyond the base ADR template** and will be standardized across all future ADRs.

- Encourages file-based data lake approach (Parquet/CSV first)
- Keeps ETL and analytics tightly integrated in Python layer
- Delays need for full database infrastructure stack
- Clearly separates:
  - Analytical layer → DuckDB
  - Application layer → PostgreSQL (future)

---

## Summary

DuckDB was chosen to optimize for **speed of development, analytical performance, and simplicity**, while keeping the architecture flexible enough to introduce PostgreSQL later for transactional and user-facing needs.
