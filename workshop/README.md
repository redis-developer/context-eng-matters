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

| Module | Time | Notebook | Lines | Key Concepts |
|--------|------|----------|-------|--------------|
| **1. Introduction** | 45 min | `01_introduction_to_context_engineering.ipynb` | ~600 | Four context types, context failures, token budgeting |
| **2. RAG Essentials** | 60 min | `02_rag_essentials.ipynb` | ~1,000 | Vector embeddings, semantic search, HierarchicalCourseManager |
| **3. Data Engineering** | 75 min | `03_data_engineering.ipynb` | ~960 | Data pipeline, chunking strategies, real PDF examples |
| **4. Memory Systems** | 90 min | `04_memory_systems.ipynb` | ~2,000 | Working memory, long-term memory, memory-enhanced RAG |
| **5. Building Agents** | 60 min | `05_building_agents.ipynb` | ~350 | LangGraph, tool calling, memory tools |
| **6. Capstone** | 30 min | `06_capstone_comparison.ipynb` | ~300 | Stage 4 vs 6 comparison, production patterns |

**Total:** ~6 hours | ~5,210 lines of comprehensive content

## 🔧 Prerequisites

### Required Software
- Python 3.11+
- Docker (for Redis and Agent Memory Server)
- Jupyter Lab or VS Code with Jupyter extension

### API Keys
- OpenAI API key (for embeddings and LLM)

### Services Required
- **Redis** (port 6379) - Required for all modules
- **Agent Memory Server** (port 8088) - Required for Module 4 (Memory Systems)
  - Must be started with `OPENAI_API_KEY` environment variable for long-term memory features

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

### Module 2: RAG Essentials (60 min) - ~1,000 lines

**Understanding Retrieval-Augmented Generation** *(Comprehensive content from Section 2)*

- **Vector Embeddings**: How semantic search captures meaning (with live similarity matrix demo)
- **RAG Pipeline**: Query → Embed → Search → Retrieve → Assemble → Generate
- **HierarchicalCourseManager**: Two-tier retrieval system
  - Tier 1: Vector index of course summaries (for search)
  - Tier 2: Hash storage of full course details (for deep dives)
- **HierarchicalContextAssembler**: Progressive disclosure pattern
  - `assemble_summary_only_context()` - Lightweight overview
  - `assemble_hierarchical_context()` - Full details for top matches
  - `assemble_with_budget()` - Token-aware assembly
- **Hands-on**: Build course search with Redis Vector, compare search strategies

### Module 3: Data Engineering for Context (75 min) - ~960 lines

**Preparing Data for RAG** *(Comprehensive content from Section 2)*

- **Data Pipeline**: Extract → Clean → Transform → Optimize → Store
- **Three Engineering Approaches**:
  - RAG (Semantic Search) - Dynamic retrieval
  - Structured Views (Pre-Computed) - Static summaries
  - Hybrid - Best of both worlds
- **Chunking Strategies** (with LangChain):
  - Document-Based (Structure-Aware)
  - Fixed-Size (Token-Based with RecursiveCharacterTextSplitter)
  - Semantic (Meaning-Based with SemanticChunker)
  - When NOT to chunk: Structured records like courses
- **Real-World Examples**:
  - Uses actual arXiv research paper (arxiv_2504_02268.pdf)
  - Multimodal content handling: tables, formulas, figures
  - Working code for PDF extraction and chunking
- **Production Pipelines**: Request-Time, Batch, Event-Driven architectures
- **Quality Metrics**: Relevance, Completeness, Efficiency, Accuracy

### Module 4: Memory Systems (90 min) - ~2,000 lines

**Adding Persistence to Your Agent** *(Comprehensive content from Section 3)*

- **The Grounding Problem**: Why agents need memory for reference resolution
- **Working Memory**: Session-based conversation continuity
  - Multi-turn conversation demos (Turn 1, 2, 3)
  - Pronoun resolution ("it", "the first one", "those prerequisites")
- **Long-term Memory**: Cross-session knowledge persistence
  - Semantic memories (facts) vs Episodic memories (events)
  - Topics and filtering
  - Cross-session persistence verification
- **Memory-Enhanced RAG**: All four context types working together
  - System + User + Conversation + Retrieved
- **Agent Memory Server**: Automatic compression and semantic extraction
- **Hands-on**: Complete memory-enhanced course advisor

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

## 🏃 Executing the Notebooks

All workshop notebooks have been tested and execute successfully. To run them:

```bash
# From the repository root
cd workshop

# Execute a specific notebook
jupyter execute 02_rag_essentials.ipynb --inplace

# Or run all notebooks
for nb in 02_rag_essentials.ipynb 03_data_engineering.ipynb 04_memory_systems.ipynb; do
  jupyter execute $nb --inplace
done
```

**Note for Module 4 (Memory Systems):**
The Agent Memory Server must be running with the `OPENAI_API_KEY` environment variable set:

```bash
# Restart Agent Memory Server with API key (from repository root)
source .env
docker stop agent-memory-server 2>/dev/null
docker rm agent-memory-server 2>/dev/null
docker run -d --name agent-memory-server \
  -p 8088:8000 \
  -e REDIS_URL=redis://host.docker.internal:6379 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e LOG_LEVEL=INFO \
  ghcr.io/redis/agent-memory-server:0.12.3 \
  agent-memory api --host 0.0.0.0 --port 8000 --no-worker
```

## 🗂️ Data

This workshop uses **hierarchical course data** for progressive disclosure:

- **CourseSummary**: Lightweight overview (~60 tokens each)
- **CourseDetails**: Full syllabus and assignments (~200+ tokens each)

Data location: `src/redis_context_course/data/hierarchical/hierarchical_courses.json`

## 🔧 Technical Notes

### HierarchicalCourseManager vs CourseManager

All workshop modules use `HierarchicalCourseManager` for consistency:

- **HierarchicalCourseManager**: Two-tier retrieval (summaries + details)
  - `search_summaries()` - Search course summaries
  - `fetch_details()` - Get full course details
  - `hierarchical_search()` - Combined search with progressive disclosure
- **CourseManager**: Basic single-tier retrieval (used in source notebooks)

### File Paths

Workshop notebooks use relative paths from the `workshop/` directory:
- `../reference-agent` - Reference agent code
- `../src/redis_context_course` - Core library

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

