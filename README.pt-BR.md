# AI Data Investigator

🇺🇸 **English:** [README.md](./README.md)

> Uma plataforma de IA autônoma que investiga dados públicos brasileiros utilizando Engenharia de Dados, Análise de Dados, Machine Learning, Grandes Modelos de Linguagem (LLMs) e Agentes de IA para responder perguntas em linguagem natural.

---

## 🚧 Status do Projeto

**Em desenvolvimento inicial**

Este projeto está sendo desenvolvido seguindo práticas profissionais de engenharia de software, incluindo Git Flow, Pull Requests, Code Reviews, Integração Contínua (CI) e documentação completa.

---

## 🎯 Visão Geral

O **AI Data Investigator** é uma plataforma completa para coletar, processar, analisar e explicar dados públicos brasileiros.

Em vez de explorar manualmente diferentes bases de dados, o usuário poderá fazer perguntas em linguagem natural e o sistema será capaz de:

- 📥 Coletar dados de diversas fontes públicas
- 🔄 Executar pipelines de ETL
- 🗄️ Armazenar e organizar os dados
- 📊 Realizar análises estatísticas
- 📈 Gerar visualizações interativas
- 🤖 Orquestrar agentes especializados de IA
- 📝 Produzir relatórios automáticos
- 💬 Responder perguntas em linguagem natural

Exemplos:

- Existe relação entre desemprego e violência?
- Quais estados reduziram a mortalidade infantil após aumento dos investimentos em saúde?
- Existe correlação entre queimadas e temperatura?
- Quais municípios apresentaram maior evolução educacional na última década?

---

## 🏗️ Arquitetura (Planejada)

```text
Fontes Públicas
      │
      ▼
Pipelines ETL
      │
      ▼
Data Warehouse (DuckDB)
      │
      ▼
Agentes Especializados de IA
      │
      ▼
Análises Estatísticas
      │
      ▼
Visualizações
      │
      ▼
Relatórios e Respostas em Linguagem Natural
```

---

## ⚙️ Stack Tecnológica

### Linguagem

- Python

### Engenharia de Dados

- Pandas
- Polars
- DuckDB
- PyArrow

### Inteligência Artificial

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

## 📂 Funcionalidades Planejadas

- Pipelines ETL automatizados
- Integração com dados públicos brasileiros
- Orquestração de Agentes de IA
- Análises estatísticas
- Modelos de Machine Learning
- Dashboards interativos
- Geração automática de relatórios
- API REST
- Interface em linguagem natural

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License**. Consulte o arquivo [LICENSE](./LICENSE) para mais detalhes.
