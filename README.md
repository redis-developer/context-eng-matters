# Context Engineering for LLMs with Redis

Learn to build production-ready AI agents with optimized context management, memory systems, and intelligent retrieval using Redis, LangGraph, and LangChain.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Redis](https://img.shields.io/badge/Redis-8.0+-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-1C3C3C?logo=chainlink&logoColor=white)](https://python.langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## What You'll Learn

This hands-on course teaches practical context engineering patterns through building a **Course Advisor Agent**:

- **RAG Fundamentals** — Build retrieval-augmented generation systems with Redis vector search
- **Context Engineering** — Optimize token efficiency using progressive disclosure and hierarchical context
- **LangGraph Agents** — Create observable, stateful workflows with tool calling
- **Hybrid Search** — Combine semantic search with exact-match retrieval using NER
- **Memory Systems** — Implement working memory and long-term memory for personalization
- **ReAct Pattern** — Build agents with explicit reasoning (Thought → Action → Observation)

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **Python** | 3.11 or higher |
| **Redis Stack** | Local Docker or [Redis Cloud](https://redis.io/cloud/) |
| **OpenAI API Key** | For GPT-4o access |
| **Agent Memory Server** | For memory stages (5+) |
| **Docker** | For running Redis and Agent Memory Server |

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/redis-developer/context-engineering-reinvent.git
cd context-engineering-reinvent
```

### 2. Create Virtual Environment

```bash
# Using UV (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync

# Or using pip
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

### 3. Set Environment Variables

```bash
# Create .env file from example
cp .env.example .env

# Edit .env and add your OpenAI API key
```

**Environment Variables:**

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | - | Your OpenAI API key for embeddings and LLM |
| `REDIS_URL` | No | `redis://localhost:6379` | Redis connection URL |
| `AGENT_MEMORY_SERVER_URL` | No | `http://localhost:8088` | Agent Memory Server URL |
| `REDIS_INDEX_NAME` | No | `course_catalog` | Redis index name for course data |
| `OPENAI_MODEL` | No | `gpt-4o` | OpenAI model to use |

### 4. Start Services

```bash
# Start Redis and Agent Memory Server
docker-compose up -d

# Verify services are running
docker ps
```

### 5. Load Course Data into Redis

The progressive agents require course data in Redis. The data must be loaded into the `hierarchical_courses` index, which contains courses with complete syllabus information.

```bash
# Ingest courses into the hierarchical_courses index (required for progressive agents)
uv run python -m redis_context_course.scripts.ingest_courses \
  --catalog src/redis_context_course/data/courses.json \
  --index-name hierarchical_courses \
  --clear
```

> **Note:** The `courses.json` file is synced with `hierarchical_courses.json` to ensure all courses have complete syllabus data. If you modify the hierarchical data, regenerate `courses.json`:
> ```bash
> uv run python src/redis_context_course/scripts/generate_courses_from_hierarchical.py
> ```

### 6. Verify Installation

```bash
# Run tests
uv run pytest tests/ -v

# Or with pip
pytest tests/ -v
```

---

## Quick Start

Try the ReAct agent with visible reasoning in under 2 minutes:

```bash
cd progressive_agents/stage4_hybrid_search

# Ask about a course with visible reasoning
python cli.py --show-reasoning "What are the prerequisites for CS002?"
```

**Example output:**
```
🧠 Reasoning Trace:
================================================================================
💭 Thought: The user is asking about prerequisites. I'll use exact match.

🔧 Action: search_courses
   Input: {"query": "CS002", "intent": "PREREQUISITES", "search_strategy": "exact_match"}
👁️  Observation: Found CS002 - Machine Learning Fundamentals...

💭 Thought: I found the course. Prerequisites field is empty - no prerequisites required.

✅ FINISH
================================================================================

📝 Answer:
CS002 (Machine Learning Fundamentals) has no formal prerequisites listed.
```

---

## Project Structure

```
context-engineering-reinvent/
├── src/redis_context_course/     # Core library
│   ├── course_manager.py         # Redis vector search for courses
│   ├── hierarchical_context.py   # Progressive disclosure
│   ├── models.py                 # Pydantic data models
│   └── scripts/                  # Data generation utilities
│
├── progressive_agents/           # 6 agent implementations (learning path)
│   ├── stage1_baseline_rag/
│   ├── stage2_context_engineered/
│   ├── stage3_full_agent_without_memory/
│   ├── stage4_hybrid_search/            # Hybrid search + ReAct
│   ├── stage5_working_memory/           # Session-based memory + ReAct
│   └── stage6_full_memory/              # Working + Long-term memory + ReAct
│
├── notebooks/                    # 11 Jupyter notebooks
│   ├── section-1-context-engineering-foundations/
│   ├── section-2-retrieved-context-engineering/
│   ├── section-3-memory-systems/
│   └── section-4-tools-and-agents/
│
├── tests/                        # Test suite
├── examples/                     # Usage examples
└── docker-compose.yml            # Redis + Agent Memory Server
```

---

## Progressive Agents

The `progressive_agents/` directory contains a learning path from basic RAG to production-ready agents:

```mermaid
graph LR
    S1[Stage 1<br/>Baseline RAG] --> S2[Stage 2<br/>Context Engineering]
    S2 --> S3[Stage 3<br/>Full Agent]
    S3 --> S4[Stage 4<br/>Hybrid Search]
    S4 --> S5[Stage 5<br/>Working Memory]
    S5 --> S6[Stage 6<br/>Full Memory]
```

| Stage | Key Feature | What's New |
|-------|-------------|------------|
| **1** | Baseline RAG | Raw JSON context, ~5000 tokens |
| **2** | Context Engineering | Progressive disclosure, ~1000 tokens |
| **3** | Full Agent | LangGraph, intent classification, quality eval |
| **4** | Hybrid Search | NER + FilterQuery, visible reasoning (ReAct) |
| **5** | Working Memory | Session-based conversation history (1 tool) |
| **6** | Full Memory | Working + long-term memory (3 tools) |

👉 **[See full documentation →](progressive_agents/README.md)**

---

## Notebooks

| Section | Topics | Duration |
|---------|--------|----------|
| **1. Context Engineering Foundations** | What is context engineering, assembly strategies | 2-3 hrs |
| **2. Retrieved Context Engineering** | RAG fundamentals, crafting & optimizing context | 2.5-3 hrs |
| **3. Memory Systems** | Working/long-term memory, compression strategies | 4-5 hrs |
| **4. Tools and Agents** | LangGraph, tool calling, semantic tool selection | 3.5-4.5 hrs |

**Start learning:**
```bash
uv run jupyter notebook notebooks/
```

Open: `section-1-context-engineering-foundations/01_what_is_context_engineering.ipynb`

---

## Key Technologies

| Technology | Purpose |
|------------|---------|
| **Redis Stack** | Vector storage, semantic search, caching |
| **RedisVL** | Vector search library with FilterQuery |
| **LangGraph** | Stateful agent workflows |
| **LangChain** | LLM application framework |
| **Agent Memory Server** | Working and long-term memory management |
| **OpenAI GPT-4o** | Language model for reasoning |

---

## Documentation

| Document | Description |
|----------|-------------|
| [SETUP.md](SETUP.md) | Detailed setup and troubleshooting |
| [workshop/README.md](workshop/README.md) | Intensive workshop guide |
| [progressive_agents/README.md](progressive_agents/README.md) | Agent stages documentation |
| [notebooks/README.md](notebooks/README.md) | Full course notebook guides |

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT License — See [LICENSE](LICENSE) for details.
