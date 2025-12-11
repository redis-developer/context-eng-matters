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
| **OpenAI API Key** | For GPT-4o access (or Orchestra API key for BOA workshop) |
| **Agent Memory Server** | For memory stages (5+) |
| **Docker** | For running Redis and Agent Memory Server |

> **🏦 For BOA:** Use `ORCHESTRA_API_KEY` instead of `OPENAI_API_KEY`. See [workshop_boa/](workshop_boa/) for details.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/redis-developer/context-eng-matters.git
cd context-eng-matters
```

### 2. Create Virtual Environment

<details>
<summary><b>🐧 Linux / macOS</b></summary>

```bash
# Using UV (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync

# Or using pip
python -m venv .venv
source .venv/bin/activate
pip install -e .
```
</details>

<details>
<summary><b>🪟 Windows</b></summary>

```powershell
# Using UV (recommended) - PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv sync

# Or using pip - PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .

# Or using pip - Command Prompt
python -m venv .venv
.venv\Scripts\activate.bat
pip install -e .
```

**Note:** If you get an execution policy error, run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
</details>

### 3. Set Environment Variables

<details>
<summary><b>🐧 Linux / macOS</b></summary>

```bash
# Create .env file from example
cp .env.example .env

# Edit .env and add your OpenAI API key
# Use your preferred editor: nano, vim, or code
nano .env
```
</details>

<details>
<summary><b>🪟 Windows</b></summary>

```powershell
# PowerShell
Copy-Item .env.example .env

# Edit .env and add your OpenAI API key
notepad .env

# Or use VS Code
code .env
```

```cmd
# Command Prompt
copy .env.example .env

# Edit .env and add your OpenAI API key
notepad .env
```
</details>

**Environment Variables:**

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | - | Your OpenAI API key for embeddings and LLM |
| `REDIS_URL` | No | `redis://localhost:6379` | Redis connection URL |
| `AGENT_MEMORY_SERVER_URL` | No | `http://localhost:8088` | Agent Memory Server URL |
| `REDIS_INDEX_NAME` | No | `course_catalog` | Redis index name for course data |
| `OPENAI_MODEL` | No | `gpt-4o` | OpenAI model to use |
| `ORCHESTRA_API_KEY` | No | - | 🏦 **BOA Only:** Bearer token for Orchestra API |

> **🏦 For BOA Workshop:** See [`workshop_boa/QUICKSTART.md`](workshop_boa/QUICKSTART.md) for Orchestra API setup instructions.

### 4. Start Services

<details>
<summary><b>🐧 Linux / macOS</b></summary>

```bash
# Start Redis and Agent Memory Server
docker-compose up -d

# Verify services are running
docker ps
```
</details>

<details>
<summary><b>🪟 Windows</b></summary>

```powershell
# PowerShell or Command Prompt
docker-compose up -d

# Verify services are running
docker ps
```

**Note:** Ensure Docker Desktop is installed and running on Windows.
- Download from: https://www.docker.com/products/docker-desktop/
- WSL 2 backend is recommended for better performance
</details>

### 5. Load Course Data into Redis

The notebooks and progressive agents require course data in Redis. Load the hierarchical course data:

<details>
<summary><b>🐧 Linux / macOS</b></summary>

```bash
# Load hierarchical courses into Redis (recommended)
uv run python -m redis_context_course.scripts.load_hierarchical_courses \
  -i src/redis_context_course/data/hierarchical/hierarchical_courses.json \
  --force
```
</details>

<details>
<summary><b>🪟 Windows</b></summary>

```powershell
# PowerShell (use backtick for line continuation)
uv run python -m redis_context_course.scripts.load_hierarchical_courses `
  -i src/redis_context_course/data/hierarchical/hierarchical_courses.json `
  --force
```

```cmd
# Command Prompt (use caret for line continuation)
uv run python -m redis_context_course.scripts.load_hierarchical_courses ^
  -i src/redis_context_course/data/hierarchical/hierarchical_courses.json ^
  --force
```

**Or as a single line:**
```powershell
uv run python -m redis_context_course.scripts.load_hierarchical_courses -i src/redis_context_course/data/hierarchical/hierarchical_courses.json --force
```
</details>

**Options:**
- `--force` / `-f`: Clear existing data before loading (use when reloading after data changes)
- `--summary-index` / `-s`: Custom index name (default: `course_summaries`)
- `--details-prefix` / `-d`: Custom details prefix (default: `course_details`)

> **Alternative:** For backward compatibility with flat course format:
> ```bash
> uv run python -m redis_context_course.scripts.ingest_courses \
>   --catalog src/redis_context_course/data/courses.json \
>   --index-name hierarchical_courses \
>   --clear
> ```

> **Note:** If you regenerate the course catalog, always use `--force` to reload Redis data.

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
👁️  Observation: Found CS002 - Data Structures and Algorithms...

💭 Thought: I found the course. Prerequisites: CS001 (Introduction to Programming).

✅ FINISH
================================================================================

📝 Answer:
CS002 (Data Structures and Algorithms) requires CS001 (Introduction to Programming) as a prerequisite.
```

---

## 🏦 BOA Workshop

The `workshop_boa/` directory contains a specialized version of the workshop with **Orchestra API integration** for BOA internal use.

### Key Features

- ✅ **Orchestra API Integration** - Uses BOA's internal Orchestra API instead of OpenAI
- ✅ **CustomTextVectorizer** - RedisVL-compatible embedding function
- ✅ **Placeholder Mode** - Test integration without Orchestra API (uses OpenAI fallback)
- ✅ **Non-Breaking** - All existing code continues to work
- ✅ **Clear Markers** - All changes marked with `#Orchestra change` comments

### Quick Start (BOA)

```bash
# 1. Add Orchestra API key to .env
echo "ORCHESTRA_API_KEY=your_bearer_token" >> .env

# 2. Run test script
python workshop_boa/test_orchestra.py

# 3. If tests pass, update notebooks
# (Uncomment #Orchestra change sections in notebooks)
```

### Documentation

- **[QUICKSTART.md](workshop_boa/QUICKSTART.md)** - Simple 3-step setup guide
- **[SETUP_INSTRUCTIONS.md](workshop_boa/SETUP_INSTRUCTIONS.md)** - Detailed setup instructions
- **[ORCHESTRA_INTEGRATION.md](workshop_boa/ORCHESTRA_INTEGRATION.md)** - Complete technical reference
- **[README.md](workshop_boa/README.md)** - Workshop overview

### What's Included

```
workshop_boa/
├── 01-04_*.ipynb             # Workshop notebooks with Orchestra integration
├── orchestra_utils.py        # Orchestra API utilities
├── redis_context_course_boa/ # BOA-specific package
├── test_orchestra.py         # Comprehensive test suite (7 tests)
└── *.md                      # Complete documentation
```

**See [`workshop_boa/QUICKSTART.md`](workshop_boa/QUICKSTART.md) for complete setup instructions.**

---

## Project Structure

```
context-eng-matters/
├── src/redis_context_course/     # Core library
│   ├── course_manager.py         # CourseManager - basic Redis vector search
│   ├── hierarchical_course_manager.py  # HierarchicalCourseManager - two-tier retrieval
│   ├── hierarchical_context.py   # HierarchicalContextAssembler - progressive disclosure
│   ├── models.py                 # Pydantic data models
│   └── scripts/                  # Data generation utilities
│
├── workshop/                     # Comprehensive workshop (6 notebooks, ~5,210 lines)
│   ├── 01_introduction_to_context_engineering.ipynb  # Context types, token budgeting
│   ├── 02_rag_essentials.ipynb                       # Vector embeddings, semantic search (~1,000 lines)
│   ├── 03_data_engineering.ipynb                     # Data pipelines, chunking strategies (~960 lines)
│   ├── 04_memory_systems.ipynb                       # Working + long-term memory (~2,000 lines)
│   ├── 05_building_agents.ipynb                      # LangGraph, tool calling
│   └── 06_capstone_comparison.ipynb                  # Stage 4 vs 6 comparison
│
├── workshop_boa/                 # 🏦 BOA-specific workshop with Orchestra API integration
│   ├── 01-04_*.ipynb             # Workshop notebooks with #Orchestra change markers
│   ├── orchestra_utils.py        # Orchestra API utilities (CustomTextVectorizer)
│   ├── redis_context_course_boa/ # BOA-specific package with Orchestra embeddings
│   ├── test_orchestra.py         # Comprehensive test suite
│   ├── QUICKSTART.md             # Quick start guide for Orchestra integration
│   ├── SETUP_INSTRUCTIONS.md     # Detailed setup instructions
│   └── ORCHESTRA_INTEGRATION.md  # Complete technical reference
│
├── progressive_agents/           # 6 agent implementations (learning path)
│   ├── stage1_baseline_rag/
│   ├── stage2_context_engineered/
│   ├── stage3_full_agent_without_memory/
│   ├── stage4_hybrid_search/            # Hybrid search + ReAct
│   ├── stage5_working_memory/           # Session-based memory + ReAct
│   └── stage6_full_memory/              # Working + Long-term memory + ReAct
│
├── notebooks/                    # Full course (11 Jupyter notebooks)
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

| Stage | Key Feature | What's New | Reasoning |
|-------|-------------|------------|-----------|
| **1** | Baseline RAG | Information overload (~6,000 tokens) | Hidden |
| **2** | Context Engineering | Progressive disclosure (~539 tokens) | Hidden |
| **3** | Full Agent | LangGraph, intent classification, hierarchical retrieval | Hidden |
| **4** | Hybrid Search | Hybrid search + ReAct pattern | **Visible** |
| **5** | Working Memory | Session-based memory (1 tool) | **Visible** |
| **6** | Full Memory | Working + long-term memory (3 tools) | **Visible** |

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
