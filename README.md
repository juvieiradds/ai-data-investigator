# AI Data Investigator

🇧🇷 **Português:** [README.pt-BR](./README.pt-BR.md)

> An autonomous AI platform that investigates Brazilian public datasets using Data Engineering, Analytics, Machine Learning, Large Language Models (LLMs), and AI Agents to answer natural language questions.

---

## 🚧 Project Status

**Early Development**

This project is currently under active development and follows a professional software engineering workflow with Git Flow, Pull Requests, Code Reviews, Continuous Integration, and comprehensive documentation.

---

## 🎯 Project Overview

**AI Data Investigator** is an end-to-end platform designed to automatically collect, process, analyze, and explain Brazilian public datasets.

Instead of manually exploring datasets, users can ask questions in natural language, and the platform will:

- 📥 Collect data from multiple public sources
- 🔄 Execute ETL pipelines
- 🗄️ Store and organize data
- 📊 Perform statistical analyses
- 📈 Generate interactive visualizations
- 🤖 Coordinate specialized AI agents
- 📝 Produce automated reports
- 💬 Answer questions using natural language

Example questions:

- Is there a relationship between unemployment and violence?
- Which states reduced infant mortality after increasing healthcare investments?
- Is there a correlation between wildfires and temperature?
- Which municipalities showed the greatest educational improvement over the last decade?

---

## 🏗️ Architecture (Planned)

```text
Public Data Sources
        │
        ▼
   ETL Pipelines
        │
        ▼
    DuckDB Warehouse
        │
        ▼
 Specialized AI Agents
        │
        ▼
 Statistical Analysis
        │
        ▼
 Data Visualization
        │
        ▼
 Reports & Natural Language Answers
```

---

## ⚙️ Tech Stack

### Programming

- Python

### Data Engineering

- Pandas
- Polars
- DuckDB
- PyArrow

### Artificial Intelligence

- LangGraph
- LangChain
- OpenAI
- Claude
- Ollama

### API

- FastAPI

### Dashboard

- Streamlit
- Plotly

### DevOps

- Docker
- GitHub Actions
- Pre-commit
- Ruff
- Pytest

---

## 📂 Planned Features

- Automated ETL pipelines
- Public dataset integration
- AI Agent orchestration
- Statistical analysis
- Machine Learning models
- Interactive dashboards
- Automated report generation
- REST API
- Natural language interface

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.
