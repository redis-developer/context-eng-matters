# Context Engineering Course

**A comprehensive, hands-on course teaching practical context engineering patterns for AI agents using Redis, Agent Memory Server, LangChain, and LangGraph.**

[![Redis](https://img.shields.io/badge/Redis-8.0+-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-1C3C3C?logo=chainlink&logoColor=white)](https://python.langchain.com/)
[![UV](https://img.shields.io/badge/UV-Package%20Manager-blueviolet)](https://docs.astral.sh/uv/)

---

## What is Context Engineering?

**Context Engineering** is the practice of designing, implementing, and optimizing context management systems for AI agents. It's the difference between a chatbot that forgets everything and an intelligent assistant that understands your needs.

### The Four Context Types

1. **System Context** - What the AI should know about its role, capabilities, and environment
2. **User Context** - Information about the user, their preferences, and history
3. **Retrieved Context** - Dynamically fetched information from databases, APIs, or vector stores
4. **Conversation Context** - The ongoing dialogue and task-focused working memory

---

## Course Overview

| | |
|---|---|
| **Format** | Self-paced, hands-on notebooks |
| **Level** | Intermediate to Advanced |
| **Duration** | 14-20 hours |
| **Prerequisites** | Python, basic AI/ML understanding, familiarity with LLMs |

### What You'll Build

A complete **Redis University Course Advisor Agent** that:
- Helps students find courses using semantic search
- Remembers student preferences and goals across sessions
- Provides personalized recommendations
- Uses intelligent tool selection with LangGraph
- Demonstrates practical context optimization patterns

---

## Quick Start (5 Minutes)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd context-engineering-reinvent

# Install UV if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync
```

### 2. Set Environment Variables

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Start Services

```bash
docker-compose up -d
```

### 4. Start Learning

```bash
uv run jupyter notebook notebooks/
```

Open: `section-1-context-engineering-foundations/01_what_is_context_engineering.ipynb`

---

## Project Structure

```
context-engineering-reinvent/
├── pyproject.toml              # UV project configuration
├── README.md                   # This file
├── SETUP.md                    # Detailed setup guide
├── COURSE_SUMMARY.md           # Complete syllabus
├── docker-compose.yml          # Redis + Agent Memory Server
│
├── notebooks/                  # Course notebooks (11 total)
│   ├── section-1-context-engineering-foundations/  (2 notebooks)
│   ├── section-2-retrieved-context-engineering/    (2 notebooks)
│   ├── section-3-memory-systems/                   (3 notebooks)
│   └── section-4-tools-and-agents/                 (4 notebooks)
│
├── src/redis_context_course/   # Reference agent package
│   ├── agent.py               # LangGraph agent implementation
│   ├── course_manager.py      # Course storage and search
│   ├── models.py              # Data models
│   └── scripts/               # Data generation utilities
│
├── progressive_agents/         # 7 progressive agent implementations
│   ├── stage1_baseline_rag/
│   ├── stage2_context_engineered/
│   ├── stage3_full_agent_without_memory/
│   ├── stage4_hybrid_search_with_ner/
│   ├── stage5_memory_augmented/
│   ├── stage6_longterm_memory/
│   └── stage7_react_loop/
│
├── tests/                      # Test suite
├── examples/                   # Usage examples
└── docs/                       # Additional documentation
```

---

## Course Sections

### Section 1: Context Engineering Foundations (2-3 hours)
- What is Context Engineering?
- Context Assembly Strategies

### Section 2: Retrieved Context Engineering (2.5-3 hours)
- RAG Fundamentals and Implementation
- Crafting and Optimizing Context

### Section 3: Memory Systems (4-5 hours)
- Working and Long-term Memory
- Combining Memory with Retrieved Context
- Managing Long Conversations with Compression

### Section 4: Tools and Agents (3.5-4.5 hours)
- Tools and LangGraph Fundamentals
- Building Course Advisor Agent
- Agent with Memory Compression
- Semantic Tool Selection

---

## Progressive Agents

The `progressive_agents/` directory contains 7 stages of agent implementations that progressively add features:

| Stage | Features Added |
|-------|---------------|
| Stage 1 | Baseline RAG with raw JSON context |
| Stage 2 | Context engineering optimizations |
| Stage 3 | Intent classification, quality evaluation |
| Stage 4 | Named Entity Recognition, hybrid search |
| Stage 5 | Working memory, conversation history |
| Stage 6 | Long-term memory integration |
| Stage 7 | Full ReAct loop pattern |

---

## Technologies

- **Python 3.10+** - Primary language
- **UV** - Fast Python package manager
- **Redis 8.0+** - Vector storage and caching
- **LangChain/LangGraph** - LLM application framework
- **Agent Memory Server** - Memory management
- **OpenAI GPT-4** - Language model
- **RedisVL** - Vector search library

---

## Documentation

- **[SETUP.md](SETUP.md)** - Detailed setup instructions
- **[COURSE_SUMMARY.md](COURSE_SUMMARY.md)** - Complete syllabus
- **[notebooks/README.md](notebooks/README.md)** - Notebook documentation
- **[progressive_agents/README.md](progressive_agents/README.md)** - Progressive agents guide

---

## License

MIT License - See LICENSE file for details
