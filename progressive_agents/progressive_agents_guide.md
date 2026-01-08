# Progressive Agents: A Context Engineering Journey

## Overview

This guide provides a comprehensive walkthrough of the progressive agent stages, demonstrating **why context engineering matters** through working implementations. Each stage builds on the previous, showing the evolution from naive RAG to production-ready agents.

**Learning Path:**
```
Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6
Baseline   Context    Full      Hybrid    Working   Full
RAG        Engineered Agent     Search    Memory    Memory
```

---

## The Problem: Information Overload

Before diving into solutions, understand the problem Stage 1 demonstrates:

### Stage 1: Baseline RAG (The Anti-Pattern)

**What it does:**
- Retrieves ALL matching courses from Redis
- Returns FULL course details (every field, every description)
- Sends everything to the LLM in one massive context

**What it demonstrates:**
- ~6,000+ tokens for a simple query
- Slow response times
- Wasted API costs
- The "dump everything" anti-pattern

**Key Files:**
- `stage1_baseline_rag/agent/nodes.py` - Uses `RawContextAssembler`
- `stage1_baseline_rag/agent/workflow.py` - Simple 2-node workflow

**Talk Track:**
> "This is how most developers start with RAG. It works, but it's expensive and slow. 
> The LLM receives thousands of tokens of irrelevant details. We're paying for tokens 
> we don't need and making the model work harder to find the answer."

---

## The Solution: Context Engineering

### Stage 2: Context-Engineered Agent

**What changes from Stage 1:**
- Adds context transformation pipeline
- Removes noise fields (internal IDs, metadata)
- Converts JSON to natural language
- Optimizes text for LLM consumption

**Token Reduction:** ~6,000 → ~539 tokens (91% reduction)

**Key Techniques:**
1. **Cleaning**: Remove fields the LLM doesn't need
2. **Transformation**: Convert structured data to readable text
3. **Optimization**: Compress without losing meaning

**Key Files:**
- `stage2_context_engineered/agent/context_engineering.py` - Three-function pipeline

**Architecture Transition:**
```
Stage 1:                    Stage 2:
┌─────────┐                ┌─────────┐
│ research│                │ research│
└────┬────┘                └────┬────┘
     │ raw context              │ raw context
     ▼                          ▼
┌──────────┐               ┌─────────────────────┐
│synthesize│               │ context_engineering │
└──────────┘               │  • clean            │
                           │  • transform        │
                           │  • optimize         │
                           └──────────┬──────────┘
                                      │ optimized context
                                      ▼
                           ┌──────────┐
                           │synthesize│
                           └──────────┘
```

**Talk Track:**
> "Same query, same courses, but 91% fewer tokens. We're not losing information—
> we're removing noise. The LLM gets exactly what it needs to answer the question."

---

## Scaling Up: Full Agent Architecture

### Stage 3: Full Agent (LangGraph Workflow)

**What changes from Stage 2:**
- Adds intent classification (greeting vs. query)
- Adds query decomposition for complex questions
- Adds hierarchical retrieval (summaries + details)
- Adds quality evaluation loop
- Full LangGraph workflow with conditional routing

**Key Concepts:**
1. **Progressive Disclosure**: Summaries for all courses, details for top N
2. **Hierarchical Context**: Two-tier retrieval reduces tokens further
3. **Quality Loop**: Re-research if answer quality is low

**Key Files:**
- `stage3_full_agent_without_memory/agent/workflow.py` - Complex LangGraph workflow
- `stage3_full_agent_without_memory/agent/state.py` - Rich `WorkflowState`

**Architecture:**
```
                    ┌─────────────────┐
                    │  classify_intent│
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                              ▼
       ┌────────────┐                 ┌─────────────┐
       │  greeting  │                 │decompose_   │
       │  response  │                 │query        │
       └────────────┘                 └──────┬──────┘
                                             ▼
                                      ┌─────────────┐
                                      │  research   │◄──────┐
                                      └──────┬──────┘       │
                                             ▼              │
                                      ┌─────────────┐       │
                                      │ synthesize  │       │
                                      └──────┬──────┘       │
                                             ▼              │
                                      ┌─────────────┐       │
                                      │  evaluate   │───────┘
                                      │  quality    │ (if low)
                                      └──────┬──────┘
                                             ▼
                                      ┌─────────────┐
                                      │   format    │
                                      │  response   │
                                      └─────────────┘
```

**Talk Track:**
> "Now we have a real agent. It understands intent, breaks down complex questions,
> and uses hierarchical retrieval. The quality loop ensures we don't give bad answers."

---

## Adding Intelligence: Hybrid Search

### Stage 4: Hybrid Search (ReAct Pattern)

**What changes from Stage 3:**
- Introduces ReAct pattern (Thought → Action → Observation)
- Adds entity extraction for course codes
- Combines exact match (FilterQuery) + semantic search
- Visible reasoning traces

**Key Concepts:**
1. **ReAct Loop**: Explicit reasoning before each action
2. **Hybrid Search**: Exact match for codes, semantic for concepts
3. **Entity Extraction**: Detect course codes like "CS004"

**Key Files:**
- `stage4_hybrid_search/agent/state.py` - Adds `reasoning_trace`, `extracted_entities`
- `stage4_hybrid_search/agent/tools.py` - `FilterQuery` for exact matching

**Talk Track:**
> "When a user asks about 'CS004', we don't want fuzzy semantic matching—we want
> exact lookup. Hybrid search gives us the best of both worlds."

---

## Adding Memory: Conversational Context

### Stage 5: Working Memory (Session Context)

**What changes from Stage 4:**
- Adds session-based working memory via Agent Memory Server
- Enables multi-turn conversations with context
- Tracks conversation history within a session
- Single tool: `search_courses`

**Key Concepts:**
1. **Working Memory**: Short-term, session-scoped conversation history
2. **Agent Memory Server**: External service for memory storage
3. **Session ID**: Groups related conversation turns

**Key Files:**
- `stage5_working_memory/agent/state.py` - Adds `session_id`, `conversation_history`
- `stage5_working_memory/agent/nodes.py` - Memory load/save nodes

**Architecture Addition:**
```
┌──────────────────────────────────────────────────────────┐
│                   Agent Memory Server                     │
│  ┌─────────────────┐    ┌─────────────────┐              │
│  │ Working Memory  │    │  Session Store  │              │
│  │ (conversation)  │    │  (by session_id)│              │
│  └─────────────────┘    └─────────────────┘              │
└──────────────────────────────────────────────────────────┘
         ▲                         │
         │ save                    │ load
         │                         ▼
┌────────┴─────────────────────────┴────────┐
│              LangGraph Workflow            │
│  load_memory → [agent nodes] → save_memory │
└────────────────────────────────────────────┘
```

**Talk Track:**
> "Now the agent remembers what you said earlier in the conversation. Ask about
> 'CS004', then ask 'what are the prerequisites?' — it knows you mean CS004."

---

### Stage 6: Full Memory (Working + Long-term)

**What changes from Stage 5:**
- Adds long-term memory (cross-session personalization)
- Adds explicit memory tools for the agent to use
- Three tools: `search_courses`, `search_memories`, `store_memory`

**Key Concepts:**
1. **Long-term Memory**: Persists across sessions (preferences, facts)
2. **Explicit Memory Tools**: Agent decides when to store/retrieve memories
3. **Student ID**: Links memories to a specific user

**Key Files:**
- `stage6_full_memory/agent/tools.py` - Three tool implementations
- `stage6_full_memory/agent/nodes.py` - Enhanced memory management

**Architecture Addition:**
```
┌──────────────────────────────────────────────────────────┐
│                   Agent Memory Server                     │
│  ┌─────────────────┐    ┌─────────────────┐              │
│  │ Working Memory  │    │ Long-term Memory│              │
│  │ (session-scoped)│    │ (student-scoped)│              │
│  └─────────────────┘    └─────────────────┘              │
└──────────────────────────────────────────────────────────┘
         ▲         ▲               │         │
         │ save    │ store_memory  │ load    │ search_memories
         │         │               ▼         ▼
┌────────┴─────────┴───────────────┴─────────┴──────────────┐
│                    LangGraph Workflow                      │
│  ┌─────────────────────────────────────────────────────┐  │
│  │                    ReAct Loop                        │  │
│  │  Thought → Action (tool call) → Observation → ...   │  │
│  │                                                      │  │
│  │  Tools:                                              │  │
│  │  • search_courses (hybrid search)                    │  │
│  │  • search_memories (retrieve past preferences)       │  │
│  │  • store_memory (save important facts)               │  │
│  └─────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
```

**Talk Track:**
> "The agent now has true personalization. It remembers that you prefer Python courses,
> that you're interested in machine learning, and that you've already taken CS001.
> This persists across sessions — come back tomorrow and it still knows you."

---

## Stage Comparison Matrix

| Feature | Stage 1 | Stage 2 | Stage 3 | Stage 4 | Stage 5 | Stage 6 |
|---------|---------|---------|---------|---------|---------|---------|
| **Context Engineering** | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Hierarchical Retrieval** | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Intent Classification** | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Quality Evaluation** | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **ReAct Pattern** | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| **Hybrid Search** | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| **Working Memory** | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Long-term Memory** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Estimated Tokens** | ~6000 | ~539 | ~400 | ~400 | ~450 | ~500 |

---

## Key Transitions Explained

### Stage 1 → Stage 2: "The 91% Reduction"

**Problem:** Raw context wastes tokens on noise
**Solution:** Three-step context engineering pipeline
**Impact:** 91% token reduction, faster responses, lower costs

**What to look for in code:**
```python
# Stage 1: Raw context
context = raw_context_assembler.assemble(courses)

# Stage 2: Engineered context
cleaned = transform_course_to_text(course)
optimized = optimize_course_text(cleaned)
context = format_courses_for_llm(optimized_courses)
```

### Stage 2 → Stage 3: "From Pipeline to Agent"

**Problem:** Simple pipeline can't handle complex queries
**Solution:** LangGraph workflow with conditional routing
**Impact:** Handles greetings, complex questions, quality issues

**What to look for in code:**
```python
# Stage 2: Linear flow
workflow.add_edge("research", "synthesize")

# Stage 3: Conditional routing
workflow.add_conditional_edges(
    "classify_intent",
    route_by_intent,
    {"greeting": "greeting_response", "query": "decompose_query"}
)
```

### Stage 3 → Stage 4: "Visible Reasoning"

**Problem:** Agent decisions are opaque
**Solution:** ReAct pattern with explicit reasoning traces
**Impact:** Debuggable, explainable agent behavior

**What to look for in code:**
```python
# Stage 4: Reasoning trace
state["reasoning_trace"].append({
    "type": "thought",
    "content": "User is asking about a specific course code..."
})
state["reasoning_trace"].append({
    "type": "action",
    "action": "search_courses",
    "input": {"query": "CS004", "filter": {"code": "CS004"}}
})
```

### Stage 4 → Stage 5: "Remembering Context"

**Problem:** Each query is independent, no conversation flow
**Solution:** Working memory via Agent Memory Server
**Impact:** Multi-turn conversations with context

**What to look for in code:**
```python
# Stage 5: Load conversation history
history = await memory_client.get_session_messages(session_id)
state["conversation_history"] = history
```

### Stage 5 → Stage 6: "True Personalization"

**Problem:** Memory resets between sessions
**Solution:** Long-term memory with explicit tools
**Impact:** Cross-session personalization, user preferences

**What to look for in code:**
```python
# Stage 6: Memory tools
tools = [
    search_courses_tool,    # Find courses
    search_memories_tool,   # Retrieve past preferences
    store_memory_tool       # Save important facts
]
```

---

## Notebook References

Each stage connects to concepts taught in the workshop notebooks:

| Stage | Primary Notebook References |
|-------|----------------------------|
| Stage 1 | Section 1: What is Context Engineering |
| Stage 2 | Section 2, Notebook 2: Crafting and Optimizing Context |
| Stage 3 | Section 2, Notebook 2: Progressive Disclosure; Section 4, Notebook 1: LangGraph |
| Stage 4 | Section 4, Notebook 2: Building Course Advisor Agent |
| Stage 5 | Section 3, Notebook 1: Working and Long-term Memory |
| Stage 6 | Section 3, Notebook 2: Combining Memory with Retrieved Context |

---

## Automatic Features (Infrastructure-Handled)

The following concepts from notebooks are **automatically handled** by underlying libraries:

### Agent Memory Server (Stages 5-6)
- **Sliding Window**: Configurable via `WINDOW_SIZE` environment variable
- **LLM Summarization**: Automatic when thresholds exceeded
- **Long-term Extraction**: Automatic promotion of important facts
- **Memory Deduplication**: Automatic compaction

### HierarchicalContextAssembler (Stages 3+)
- **Progressive Disclosure**: Summaries for all, details for top N
- **Token Budget Management**: `assemble_with_budget()` method
- **"Lost in the Middle" Mitigation**: Structure places key info at start/end

### redis_context_course Package
- **Keyword Tool Selection**: `select_tools_by_keywords()` function
- **Semantic Tool Selection**: `SemanticToolSelector` class
- **Hybrid Retrieval**: `hybrid_retrieval()` function

---

## Running the Agents

### Prerequisites
```bash
# Environment variables required
export OPENAI_API_KEY="your-key"
export REDIS_URL="redis://localhost:6379"
export AGENT_MEMORY_URL="http://localhost:8088"  # Stages 5-6
```

### Quick Start Commands

```bash
# Stage 1: Baseline RAG
cd progressive_agents/stage1_baseline_rag
python cli.py "What machine learning courses are available?"

# Stage 2: Context Engineered
cd progressive_agents/stage2_context_engineered
python cli.py "What machine learning courses are available?"

# Stage 3: Full Agent
cd progressive_agents/stage3_full_agent_without_memory
python cli.py "What machine learning courses are available?"

# Stage 4: Hybrid Search
cd progressive_agents/stage4_hybrid_search
python cli.py "Tell me about CS004"

# Stage 5: Working Memory
cd progressive_agents/stage5_working_memory
python cli.py --student-id alice "What is CS004?"
# Then: "What are the prerequisites?"

# Stage 6: Full Memory
cd progressive_agents/stage6_full_memory
python cli.py --student-id alice "Remember that I prefer Python courses"
# New session: "What courses would you recommend?"
```

### Simulation Mode
Each stage supports `--simulate` for demo queries:
```bash
python cli.py --simulate
```

---

## Summary: Why Context Engineering Matters

| Without Context Engineering | With Context Engineering |
|----------------------------|-------------------------|
| ~6,000 tokens per query | ~400-500 tokens per query |
| Slow responses | Fast responses |
| High API costs | Low API costs |
| Information overload | Focused, relevant context |
| No conversation memory | Multi-turn conversations |
| No personalization | Cross-session preferences |

**The progression demonstrates:**
1. **Stage 1**: The problem (information overload)
2. **Stage 2**: The core solution (context engineering)
3. **Stage 3**: Scaling up (agent architecture)
4. **Stage 4**: Adding intelligence (hybrid search, reasoning)
5. **Stage 5**: Adding memory (session context)
6. **Stage 6**: Full personalization (long-term memory)

Each stage is a working implementation you can run, modify, and learn from.

---

## Next Steps

After completing this learning path:

1. **Explore the notebooks** for deeper theory and research references
2. **Modify the agents** to add new features or tools
3. **Apply the patterns** to your own domain and use cases
4. **Review the gap analysis** (`CONTENT_COVERAGE_GAP_ANALYSIS.md`) for advanced techniques

---

*This guide was generated from a comprehensive review of all progressive agent implementations and their README files.*

