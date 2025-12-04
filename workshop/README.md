# Context Engineering Workshop

![Redis](https://redis.io/wp-content/uploads/2024/04/Logotype.svg?auto=webp&quality=85,75&width=120)

## 🎯 Workshop Overview

This condensed workshop covers the essential concepts of context engineering for AI agents. You'll learn how to build intelligent agents that remember, retrieve, and reason with context.

**What You'll Build:** A course advisor agent that can:
- Search courses using semantic RAG
- Remember student preferences across sessions
- Make transparent reasoning decisions
- Achieve 91% token reduction through context engineering

## 🧠 Workshop Philosophy

This workshop follows a deliberate learning progression:

1. **Foundations First** — Understand the "why" (context types, constraints) before the "how"
2. **Data Engineering Before RAG** — Learn to prepare data properly before implementing retrieval
3. **Chunking is a Design Choice** — For structured data like course catalogs, "don't chunk" is often best
4. **Progressive Disclosure** — The key pattern: summaries for all, details for top matches
5. **Build Up to Agents** — Each module adds capabilities until you have a full agent

## ⏱️ Schedule

| Module | Time | Notebook | Key Concepts |
|--------|------|----------|--------------|
| **1. Introduction** | 45 min | `01_introduction_to_context_engineering.ipynb` | Four context types, context failures, token budgeting |
| **2. Data Engineering** | 20 min | `02_data_engineering.ipynb` | Data pipeline, chunking decisions, 91% token reduction demo |
| **3. RAG Essentials** | 55 min | `03_rag_essentials.ipynb` | Vector embeddings, semantic search, progressive disclosure |
| **4. Memory Systems** | 45 min | `04_memory_systems.ipynb` | Working memory, long-term memory, Agent Memory Server |
| **5. Building Agents** | 60 min | `05_building_agents.ipynb` | LangGraph, tool calling, memory tools |
| **6. Capstone** | 30 min | `06_capstone_comparison.ipynb` | Stage 4 vs 6 comparison, production patterns |

## 🔧 Prerequisites

### Required Software
- Python 3.9+
- Docker (for Redis and Agent Memory Server)
- Jupyter Lab or VS Code with Jupyter extension

### API Keys
- OpenAI API key (for embeddings and LLM)

## 🚀 Quick Setup

### 1. Clone and Install

```bash
# Navigate to workshop directory
cd workshop

# Install the package (from repository root)
cd ..
pip install -e .
cd workshop
```

### 2. Environment Variables

Create a `.env` file in the repository root:

```bash
# Copy the example file
cp .env.example .env

# Edit and add your OpenAI API key
```

Your `.env` file should contain:

```bash
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional (defaults provided)
REDIS_URL=redis://localhost:6379
AGENT_MEMORY_SERVER_URL=http://localhost:8088
REDIS_INDEX_NAME=course_catalog
```

### 3. Start Services

```bash
# From the repository root, start all services
docker-compose up -d
```

### 4. Verify Setup

```bash
# Check Redis
docker exec redis redis-cli ping
# Expected: PONG

# Check Agent Memory Server
curl http://localhost:8088/v1/health
# Expected: {"now":<timestamp>}
```

## 📚 Notebooks Overview

### Module 1: Introduction to Context Engineering (45 min)

**The "Why" of Context Engineering** *(Source: Redis Training)*

- **The Problem**: The "clerk behind glass" narrative — why AI agents fail without context
- **Four Context Types**: System, User, Conversation, Retrieved (with Olivia Jansen example)
- **Live Code**: Build complete context and call OpenAI API
- **Token Analysis**: Measure token usage across context types with `estimate_tokens()` and `analyze_context_usage()`
- **Strategy Comparison**: Compare minimal vs. with_user vs. with_retrieval approaches side-by-side
- **Token Economics**: Understanding context window limits and budgeting
- **Context Failures**: Poisoning, Distraction, Confusion, Clash
- **Context Rot**: Why longer context ≠ better context
- **Best Practices**: 5 essential practices for production context engineering

### Module 2: Data Engineering for Context (20 min)

**Preparing Data for LLM Consumption**

- **Data Pipeline**: Extract → Clean → Transform → Optimize → Store
- **Chunking as a Design Choice**: Depends on data type and retrieval needs
  - ❌ Don't chunk: Structured records with natural boundaries (courses, products, FAQs)
  - ✅ Consider chunking: Long-form content with multiple distinct topics
  - 📚 Research context: "Lost in the Middle" (Stanford) and "Context Rot" (Chroma) explain why this matters
  - 💡 For our course catalog: whole-record embedding works best
- **Live Demo**: Stage 1 (6,133 tokens) → Stage 2 (539 tokens) = **91% reduction**

### Module 3: RAG Essentials (55 min)

**Building on Clean, Prepared Data**

- **Vector Embeddings**: How semantic search captures meaning
- **RAG Pipeline**: Query → Embed → Search → Retrieve → Assemble → Generate
- **Progressive Disclosure**: The key pattern
  - Summaries for ALL matches (lightweight, ~60 tokens each)
  - Full details for TOP N only (on-demand, ~200+ tokens each)
- **Hands-on**: Build course search with Redis Vector

### Module 4: Memory Systems (45 min)

**Adding Persistence to Your Agent**

- **Working Memory**: Session-based conversation continuity
- **Long-term Memory**: Cross-session knowledge persistence
- **Agent Memory Server**: Automatic compression and semantic extraction
- **Hands-on**: Multi-turn conversation with context

### Module 5: Building Agents (60 min)

**Putting It All Together**

- **LangGraph Fundamentals**: Nodes, edges, state management
- **Memory Tools**: store_memory, search_memories, search_courses
- **Tool Calling**: LLM decides when to use tools
- **Hands-on**: Build a complete course advisor agent

### Module 6: Capstone Comparison (30 min)

**Seeing the Full Impact**

- **Side-by-Side**: Stage 4 (ReAct) vs Stage 6 (Full Memory)
- **Key Metrics**: Token usage, response quality, reasoning visibility
- **Production Patterns**: When to use what
- **Next Steps**: Advanced topics and resources

## 🗂️ Data

This workshop uses **hierarchical course data** for progressive disclosure:

- **CourseSummary**: Lightweight overview (~60 tokens each)
- **CourseDetails**: Full syllabus and assignments (~200+ tokens each)

Data location: `src/redis_context_course/data/hierarchical/hierarchical_courses.json`

## 📖 Related Resources

### Full Course (15-20 hours)
- `notebooks/` - Complete 11-notebook curriculum
- `progressive_agents/` - 6-stage agent progression

### Reference Implementation
- `src/redis_context_course/` - Production-ready code

### Documentation
- [Redis Vector Search](https://redis.io/docs/stack/search/reference/vectors/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [Agent Memory Server](https://github.com/redis/agent-memory-server)

---

**Ready to start?** Open `01_introduction_to_context_engineering.ipynb` and let's build some context-aware agents! 🚀

