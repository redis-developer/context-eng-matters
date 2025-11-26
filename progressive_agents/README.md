# Progressive Agents - Context Engineering Learning Path

A progressive learning experience teaching students how to evolve from basic RAG to production-ready agents with memory, using LangGraph-based architecture.

## 🎯 Learning Objectives

Students will learn:

1. **RAG Fundamentals** - Build retrieval-augmented generation systems
2. **Context Engineering** - Optimize token efficiency with progressive disclosure
3. **LangGraph Workflows** - Create observable, stateful agent architectures
4. **Hybrid Search** - Combine semantic and exact-match retrieval
5. **Memory Systems** - Add working and long-term memory for personalization
6. **ReAct Pattern** - Implement explicit reasoning with Thought → Action → Observation loops

## 📚 Stage Overview

```mermaid
graph LR
    S1[Stage 1<br/>Baseline RAG] --> S2[Stage 2<br/>Context Engineering]
    S2 --> S3[Stage 3<br/>Full Agent]
    S3 --> S4[Stage 4<br/>Hybrid Search + NER]
    S4 --> S4R[Stage 4 ReAct<br/>+Visible Reasoning]
    S4 --> S5M[Stage 5<br/>Working Memory]
    S5M --> S5R[Stage 5 ReAct<br/>+Visible Reasoning]
    S5M --> S6[Stage 6<br/>Long-term Memory]
    S6 --> S7[Stage 7 ReAct<br/>Full Memory + ReAct]
```

| Stage | Directory | Key Feature | Reasoning |
|-------|-----------|-------------|-----------|
| 1 | `stage1_baseline_rag/` | Basic RAG | Hidden |
| 2 | `stage2_context_engineered/` | Progressive disclosure | Hidden |
| 3 | `stage3_full_agent_without_memory/` | LangGraph + quality eval | Hidden |
| 4 | `stage4_hybrid_search_with_ner/` | Exact match + semantic search | Hidden |
| 4R | `stage4_react_hybrid_search/` | Hybrid search | **Visible (ReAct)** |
| 5M | `stage5_memory_augmented/` | Working memory | Hidden |
| 5R | `stage5_react_memory/` | Working memory | **Visible (ReAct)** |
| 6 | `stage6_longterm_memory/` | Long-term memory tools | Hidden |
| 7 | `stage7_react_loop/` | Full memory + ReAct | **Visible (ReAct)** |

## 🔬 Stage Details

### Stage 1: Baseline RAG
**Problem**: Show that basic retrieval works but is inefficient

```
┌─────────┐     ┌─────────┐     ┌──────────┐
│  Query  │ ──▶ │ Search  │ ──▶ │ Response │
└─────────┘     └─────────┘     └──────────┘
```

**Features**: Raw JSON context, no optimization, ~5000 tokens per query

### Stage 2: Context-Engineered RAG
**Solution**: Apply context engineering from notebooks Section 2

```
┌─────────┐     ┌───────────┐     ┌────────────┐     ┌──────────┐
│  Query  │ ──▶ │  Search   │ ──▶ │ Transform  │ ──▶ │ Response │
└─────────┘     └───────────┘     └────────────┘     └──────────┘
                                         │
                                  Progressive
                                  Disclosure
```

**What's New**: Context transformation, token optimization (~1000 tokens)

### Stage 3: Full Agent
**Enhancement**: Add LangGraph structure, intent classification, quality evaluation

```mermaid
graph TD
    Q[Query] --> IC[Classify Intent]
    IC -->|GREETING| HG[Handle Greeting]
    IC -->|Other| DQ[Decompose Query]
    DQ --> R[Research]
    R --> EQ[Evaluate Quality]
    EQ -->|Poor| R
    EQ -->|Good| S[Synthesize]
    HG --> END
    S --> END
```

**What's New**: Intent routing, query decomposition, iterative quality improvement

### Stage 4: Hybrid Search with NER
**Enhancement**: Named Entity Recognition for precise course code matching

```mermaid
graph TD
    Q[Query] --> IC[Classify Intent]
    IC --> EE[Extract Entities]
    EE -->|Course codes| EM[Exact Match]
    EE -->|Topics| SS[Semantic Search]
    EM --> M[Merge Results]
    SS --> M
    M --> PD[Progressive Disclosure]
    PD --> S[Synthesize]
```

**What's New**:
- FilterQuery for exact course code matching
- Hierarchical context assembly
- Progressive disclosure based on intent

### Stage 4 ReAct: Hybrid Search with Visible Reasoning
**Enhancement**: Same as Stage 4, but with explicit ReAct loop

```
┌────────────┐     ┌──────────────┐     ┌──────────────┐
│   Query    │ ──▶ │ ReAct Agent  │ ──▶ │   Response   │
└────────────┘     │  Thought→    │     └──────────────┘
                   │  Action→     │
                   │  Observation │
                   └──────────────┘
```

**What's New**: Visible reasoning trace, `--show-reasoning` CLI flag

### Stage 5: Working Memory (Tool-Calling)
**Enhancement**: Add working memory for multi-turn conversations

```mermaid
graph TD
    Q[Query] --> LM[Load Memory]
    LM --> IC[Classify Intent]
    IC --> A[Agent + Tools]
    A --> SM[Save Memory]
    SM --> END
```

**What's New**:
- Agent Memory Server integration
- Session-based conversation history
- Pronoun resolution ("Tell me more about it")

### Stage 5 ReAct: Working Memory with Visible Reasoning
**Enhancement**: Stage 5 with ReAct pattern

**What's New**: ReAct loop + working memory, reasoning trace visible

### Stage 6: Long-term Memory (Tool-Calling)
**Enhancement**: Add long-term memory tools for personalization

```mermaid
graph TD
    Q[Query] --> LM[Load Working Memory]
    LM --> IC[Classify Intent]
    IC --> A[Agent]
    A -->|search_courses| SC[Course Search]
    A -->|remember_user_info| RM[Remember Info]
    A -->|recall_user_info| RC[Recall Info]
    A --> SM[Save Working Memory]
    SM --> END
```

**What's New**:
- `remember_user_info` tool for storing preferences
- `recall_user_info` tool for retrieving preferences
- Personalized recommendations

### Stage 7: Full Memory with ReAct
**Final Stage**: Complete implementation with all features

```
User Query
    ↓
┌─────────────────────────────────────────────────────┐
│                   ReAct Loop                         │
│  ┌───────────────────────────────────────────────┐  │
│  │ Thought: Analyze query, plan approach         │  │
│  │ Action: search_courses / remember / recall    │  │
│  │ Observation: Tool results                     │  │
│  └───────────────────────────────────────────────┘  │
│                   ↓ (repeat)                         │
│  ┌───────────────────────────────────────────────┐  │
│  │ Thought: I have enough information            │  │
│  │ Action: FINISH                                │  │
│  │ Action Input: [Final Answer]                  │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
    ↓
Final Response + Reasoning Trace
```

**Features**: All previous + visible reasoning, `--show-reasoning` flag

## 🚀 Quick Start

### Prerequisites

```bash
# Install dependencies
pip install -e .

# Set environment variables
export OPENAI_API_KEY="your-api-key"
export REDIS_URL="redis://localhost:6379"
export AGENT_MEMORY_URL="http://localhost:8088"  # For stages 5+
```

### Running Each Stage

```bash
# Stage 3: Basic agent
cd progressive_agents/stage3_full_agent_without_memory
python cli.py "What courses teach machine learning?"

# Stage 4: Hybrid search
cd progressive_agents/stage4_hybrid_search_with_ner
python cli.py "What are the prerequisites for CS002?"

# Stage 4 ReAct: With visible reasoning
cd progressive_agents/stage4_react_hybrid_search
python cli.py --show-reasoning "What's the syllabus for CS006?"

# Stage 5: Working memory (start Agent Memory Server first)
cd progressive_agents/stage5_react_memory
python cli.py --student-id alice --session-id s1 "What is CS004?"
python cli.py --student-id alice --session-id s1 "Tell me more about it"

# Stage 7 ReAct: Full features
cd progressive_agents/stage7_react_loop
python cli.py --student-id alice --show-reasoning "What CS courses are good for beginners?"
```

## 📖 Notebook Concepts Demonstrated

| Stage | Notebook Concepts |
|-------|-------------------|
| 1-2 | **Section 2**: RAG fundamentals, context crafting |
| 3 | **Section 4**: LangGraph, tool calling, agent architecture |
| 4 | **Section 2**: Progressive disclosure, hierarchical context |
| 5 | **Section 3**: Working memory, conversation history |
| 6-7 | **Section 3**: Long-term memory, memory extraction |

### Notebook References

- **Section 1**: Context Engineering Foundations
  - `01_what_is_context_engineering.ipynb`
  - `02_context_assembly_strategies.ipynb`

- **Section 2**: Retrieved Context Engineering
  - `01_rag_fundamentals_and_implementation.ipynb` → Stages 1-2
  - `02_crafting_and_optimizing_context.ipynb` → Stages 2-4

- **Section 3**: Memory Systems
  - `01_working_and_longterm_memory.ipynb` → Stages 5-7
  - `02_combining_memory_with_retrieved_context.ipynb` → Stages 5-7

- **Section 4**: Tools and Agents
  - `01_tools_and_langgraph_fundamentals.ipynb` → All stages
  - `02_building_course_advisor_agent.ipynb` → Stages 3+

## 📊 Feature Comparison

| Feature | S1 | S2 | S3 | S4 | S4R | S5 | S5R | S6 | S7 |
|---------|----|----|----|----|-----|----|----|----|----|
| **Context Engineering** | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Intent Classification** | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Hybrid Search (NER)** | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Working Memory** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Long-term Memory** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **ReAct (Visible Reasoning)** | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ |
| **Progressive Disclosure** | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

*S1=Stage 1, S2=Stage 2, etc. S4R=Stage 4 ReAct, S5R=Stage 5 ReAct*

## 🔧 Technical Details

### Key Components

| Component | Description | Used In |
|-----------|-------------|---------|
| `CourseManager` | Redis vector search for courses | All stages |
| `HierarchicalContextAssembler` | Progressive disclosure | Stages 4+ |
| `FilterQuery` | Exact course code matching | Stages 4+ |
| `Agent Memory Server` | Working/long-term memory | Stages 5+ |
| `ReActAgent` | Visible reasoning loop | ReAct stages |

### Architecture Patterns

1. **Tool-Calling Pattern** (Stages 3-6): LLM decides when to call tools via `bind_tools()`
2. **ReAct Pattern** (Stages 4R, 5R, 7): Explicit Thought → Action → Observation loop

## 🎓 Learning Outcomes

By completing this progressive path, students will:

1. ✅ **Build RAG systems** from basic to advanced
2. ✅ **Apply context engineering** for token efficiency
3. ✅ **Use LangGraph** for observable agent workflows
4. ✅ **Implement hybrid search** combining NER + semantic search
5. ✅ **Integrate memory systems** for multi-turn conversations
6. ✅ **Understand ReAct** for transparent reasoning

## 📚 Resources

- **Notebooks**: `notebooks/section-1-4/`
- **CourseManager**: `src/redis_context_course/`
- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/

## 📄 License

MIT License

