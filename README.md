# Redis Context Engineering Workshop

This repository contains:
- **Workshop notebooks** in `workshop/` 
- **Six staged agent demos** in `demos/` that cover baseline RAG → context engineering → full agent → ReAct → memory.

---

## Workshop Setup

### Prerequisites

- **Python**: 3.11+
- **Docker**: for Redis + Agent Memory Server
- **OpenAI API key**: set `OPENAI_API_KEY`

### Quick setup (recommended: `uv`)
Setup the Python environment:
```bash
uv sync
```
Create an env file:
```
cp .env.example .env
```
Edit env file as needed. Start the docker infra stack:
```bash
docker-compose up -d
```
Load the workshop data:
```bash
uv run load-hierarchical-courses \
  -i src/redis_context_course/data/hierarchical/hierarchical_courses.json \
  --force
```

### Verification (optional)

```bash
uv run pytest tests/ -v
```

- **Troubleshooting**: see `SETUP.md`

---

## Workshop Outline

This workshop guides you through the essential steps of building advanced agentic systems: starting with foundational context engineering concepts, progressing through RAG techniques, diving into practical data engineering, and culminating in the design of memory-enhanced AI agents.

### Sections

| Module | Time | Notebook | Key Highlights |
|--------|------|----------|----------------|
| **1. Introduction** | 45 min | `01_introduction_to_context_engineering.ipynb` | Overview of context types, failures, and token budgeting strategies. |
| **2. RAG Essentials** | 60 min | `02_rag_essentials.ipynb` | Semantic search, embeddings, and RAG patterns. |
| **3. Data Engineering** | 75 min | `03_data_engineering_theory.ipynb` | Data pipelines, chunking methods, and preparing retrieval-ready data. |
| **4. Memory Systems** | 90 min | `04_memory_systems.ipynb` | Working vs. long-term memory and memory-augmented RAG for agents. |


### Running notebooks

```bash
cd workshop

# Execute a specific notebook (optional)
jupyter execute 02_rag_essentials.ipynb --inplace
```

**Module 4 note:** the Redis `Agent Memory Server` must be running with `OPENAI_API_KEY` set (the provided `docker-compose.yml` loads it from your `.env`).

---

## Agent Demos

Six CLI demos that progressively add capabilities. Use `--help` for all options, `--quiet` for minimal output, `--show-reasoning` for ReAct traces (stages 4–6).

```bash
# 1. Baseline RAG — naive retrieval, no optimization
uv run 1-baseline-rag "What machine learning courses are available?"

# 2. Context-engineered — cleaned/transformed context, progressive disclosure
uv run 2-context-engineered "What machine learning courses are available?"

# 3. LangGraph agent — structured workflow with intent routing
uv run 3-langgraph-agent "What courses teach machine learning?"

# 4. Hybrid + ReAct — adds NER-based hybrid search and visible reasoning
uv run 4-hybrid-react --show-reasoning "What are the prerequisites for CS002?"

# 5. Working memory — multi-turn conversations within a session
uv run 5-working-memory --student-id alice --session-id s1 "What is CS004?"

# 6. Full memory — working + long-term memory with preference tracking
uv run 6-full-memory --student-id alice --show-reasoning "What courses do you recommend?"
```

