# Source Architecture Overview

This directory contains the core architecture of the **AI Data Investigator** system.

The structure follows a modular design separating concerns across data ingestion, processing, AI agents, and application interfaces.

---

## core/

Shared infrastructure components used across the entire system.

- database.py → DuckDB connection and query execution layer
- storage_paths.py → Definition and management of raw/processed/warehouse paths
- config.py → Environment configuration and system settings
- logging.py → Centralized logging configuration

---

## etl/

Data ingestion and transformation pipelines.

- Downloads datasets from external sources
- Applies cleaning and normalization logic
- Writes to raw/, processed/, and warehouse/ layers

Depends on core/ for storage and database access.

---

## agents/

AI agent layer built on top of structured data.

- Implements reasoning workflows
- Queries warehouse datasets via DuckDB
- Provides structured outputs for analysis and decision-making

---

## analysis/

Statistical and analytical computation layer.

- Exploratory data analysis
- Correlation and aggregation logic
- Machine learning experiments (if applicable)

Consumes processed/ and warehouse/ data.

---

## llm/

Integration layer with Large Language Models.

- OpenAI / Claude / local LLM connectors
- Prompt management
- Tool-calling abstractions

Used by agents/ and API layer.

---

## api/

Backend interface layer (FastAPI).

- Exposes system capabilities via REST endpoints
- Connects agents and analysis modules to external clients
- Handles request/response orchestration

---

## dashboard/

Frontend visualization layer (Streamlit or similar).

- Data visualization dashboards
- Analytical reports
- Interactive exploration of datasets

---

## Design Principles

- Separation of concerns by responsibility, not by technology
- core/ contains shared infrastructure only
- ETL writes data, does not perform analysis logic
- agents/ and analysis/ are read-oriented layers
- All data access is mediated via core/database.py (DuckDB abstraction)

---

## Architecture Alignment

This structure directly reflects the system-level decisions defined in:

- ADR 0001 → DuckDB as analytical engine
- ADR 0002 → Medallion data architecture (raw/processed/warehouse)

Together, these ensure a local-first, reproducible, and scalable data engineering system.
