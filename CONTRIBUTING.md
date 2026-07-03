# Contributing to AI Data Investigator

Thank you for contributing to this project.

This repository follows **professional data engineering and AI engineering practices**, simulating a real-world production system with pipelines, agents, APIs, and CI/CD.

---

# 🧭 Project Philosophy

This is not a notebook project.

This is a **production-style AI data platform**, focused on:

- Reproducible data pipelines
- Modular AI agents
- Scalable analytics architecture
- Observable and testable systems
- Clean and maintainable code

All contributions must follow these principles.

---

# 🌿 Branching Strategy (GitHub Flow-based)

We follow **GitHub Flow with strict branch isolation**:

- `main` → production-ready code only (protected)
- No direct commits allowed to `main`

All changes must be made in short-lived feature branches and merged via Pull Requests.

---

## 🧱 Branch Naming Convention

| Prefix      | Purpose                   | Example                      |
| ----------- | ------------------------- | ---------------------------- |
| `feature/`  | New functionality         | feature/etl-ibge-pipeline    |
| `fix/`      | Bug fixes                 | fix/duckdb-query-performance |
| `docs/`     | Documentation updates     | docs/add-contributing-guide  |
| `chore/`    | Maintenance & tooling     | chore/setup-docker-env       |
| `refactor/` | Code restructuring        | refactor/etl-cleanup         |
| `test/`     | Test additions or updates | test/etl-pipeline            |

> Note: `refactor/` and `test/` branches exist to clearly separate structural changes and validation work from feature development, improving review clarity and traceability.

---

# 🧾 Commit Convention

We use **Conventional Commits** strictly.

## Format

```
type(scope): short imperative description
```

## Rules

- Use English only
- Keep description concise but meaningful
- Scope is required when applicable
- Use imperative mood (add, fix, remove, update)

## Types

- `feat` → new functionality
- `fix` → bug fixes
- `docs` → documentation only
- `chore` → maintenance / config / dependencies
- `refactor` → code restructuring without behavior change
- `test` → test additions or updates
- `perf` → performance improvements
- `ci` → CI/CD changes

## Examples

```
feat(etl): add IBGE dataset ingestion pipeline
fix(database): resolve DuckDB connection timeout
docs(readme): improve architecture overview
chore(env): configure development dependencies
refactor(agents): simplify dataset selection logic
```

---

# 🔁 Pull Request Workflow

All changes must go through Pull Requests.

## Steps

1. Create a branch from `main`
2. Implement changes in small, atomic commits
3. Ensure code follows project conventions
4. Run local tests and linting (when available)
5. Push branch to remote repository
6. Open a Pull Request against `main`
7. Fill PR description with clear technical context
8. Self-review changes before requesting merge
9. Ensure all CI checks pass (when configured)
10. Merge only after approval and successful checks
11. Delete branch after merge

---

# ✅ Definition of Done (DoD)

A contribution is considered complete only when:

- Code follows project structure and conventions
- All tests pass locally and in CI (when available)
- Linting passes (Ruff or equivalent)
- Commit messages follow Conventional Commits
- PR is self-reviewed
- Documentation is updated if required
- No experimental or unused code remains

---

# 🧪 Quality Standards

This project enforces software engineering best practices:

## Code Quality

- Clean Code principles
- SOLID principles (when applicable)
- Modular architecture
- Separation of concerns

## Data Engineering

- Reproducible pipelines
- Deterministic transformations
- Clear data lineage
- Structured data contracts between steps

## AI / Agents

- Each agent has a single responsibility
- Inputs and outputs must be structured
- Prompts must be versioned and maintainable

---

# ⚙️ CI / CD Expectations

This project is designed to integrate with:

- GitHub Actions CI pipeline
- Automated linting (Ruff)
- Automated testing (Pytest)
- Future Docker-based deployment

All contributions must remain CI-compatible as the system evolves.

---

# 🧠 Engineering Mindset

When contributing, ask:

> “Would this design survive in a production system with multiple engineers, datasets, and AI agents?”

If not → iterate before submitting.

---

# 🧪 Development Setup

See [README](./README.md) for environment setup instructions.

---

# 🚨 Important Rules

- No direct commits to `main`
- All changes must go through Pull Requests
- Keep commits small and atomic
- Experimental code must not be merged
- Maintain consistency across modules and layers

---

# 🚀 Final Note

This project simulates a **real-world AI + Data Engineering platform**, designed to demonstrate production-level engineering skills for portfolio and technical evaluation purposes.
