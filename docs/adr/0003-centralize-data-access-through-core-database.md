# 0003. Centralize Data Access Through core/database.py

## TL;DR

All data access across the system (ETL writes, agent reads, analysis reads)
must go through a single centralized facade layer (`core/database.py` and
`core/storage_paths.py`), preventing direct and inconsistent DuckDB usage
across modules.

---

## Status

Accepted

---

## Context

As the system evolves to include multiple consumers of data (ETL pipelines,
AI agents, analysis modules, API layer, and dashboard), each component
interacts with the same underlying datasets but with different access patterns.

Without a centralized access layer, several concrete issues emerge:

- Multiple modules independently opening DuckDB connections, leading to inconsistent configuration and execution behavior
- SQL logic being duplicated across ETL, analysis, and agent layers
- File path logic for `raw/`, `processed/`, and `warehouse/` being hardcoded in multiple places
- Lack of global control over query execution rules, pragmas, or performance tuning
- Increased difficulty to refactor storage strategy in the future (e.g., introducing PostgreSQL, object storage, or caching layers)

In addition, debugging becomes significantly harder because there is no single point where data access can be inspected, logged, or validated.

Without this control layer, the system risks evolving into a fragmented set of scripts that operate on shared data without consistent rules.

---

## Decision

All data access in the system MUST be mediated through a single abstraction layer:

- `core/database.py` → responsible for all DuckDB interactions (connection management, query execution, write operations)
- `core/storage_paths.py` → responsible for resolving dataset locations across `raw/`, `processed/`, and `warehouse/`

This design follows the **Facade Pattern**, providing a unified interface over
the underlying data infrastructure while hiding implementation details from
consuming modules.

Under this rule:

- No module (ETL, agents, analysis, API, dashboard) may open its own DuckDB connection directly
- No module may hardcode dataset paths
- All SQL execution must be routed through `core/database.py`

This ensures a single entry point for all data operations in the system.

---

## Alternatives Considered

### 1. Each module manages its own DuckDB connection

Each layer (ETL, agents, analysis) directly opens and manages its own database
connection and executes queries independently.

❌ Problems:

- Inconsistent connection configuration across modules
- Duplicated SQL and execution logic
- Harder to enforce standards (logging, performance tuning, caching)
- High coupling between business logic and storage implementation
- Difficult to refactor if database engine changes

---

### 2. Partial shared access (ETL + agents share, analysis independent)

Only some modules (e.g., ETL and agents) use a shared database layer,
while others (analysis, API) access data independently.

❌ Problems:

- Creates inconsistent architectural boundaries
- Splits system into "controlled" vs "uncontrolled" data access zones
- Makes debugging and lineage tracing inconsistent
- Does not solve long-term maintainability issues
- Leads to implicit duplication of database logic

---

## Consequences

### Positive

- Single source of truth for all data access logic
- Easier debugging through centralized query execution layer
- Improved testability (database layer can be mocked or replaced)
- Enables future migration strategies (DuckDB → hybrid PostgreSQL setup)
- Consistent handling of dataset paths and storage layers
- Clear enforcement point for query standards and logging

### Negative / Trade-offs

- Introduces strong dependency on `core/` across all system modules
- Risk of creating a bottleneck if `core/database.py` becomes overly complex
- Requires discipline to prevent bypassing the abstraction layer
- A bug in the central layer can affect the entire system
- Slight overhead in simple one-off data operations due to abstraction

---

## Architectural Impact

This decision directly reinforces and depends on previous ADRs:

- **ADR 0001 (DuckDB as analytical engine)** defines the storage/query engine
- **ADR 0002 (Medallion architecture)** defines how data is physically organized
- **This ADR (0003)** defines how all system components interact with that data

Together, they establish a coherent layered architecture:

- Storage Layer → DuckDB (ADR 0001)
- Data Organization Layer → raw / processed / warehouse (ADR 0002)
- Access Layer → core/database.py Facade (this ADR)

This separation ensures that future system components (agents, APIs, dashboards)
do not depend on storage implementation details, enabling scalability and
future infrastructure evolution without widespread refactoring.
