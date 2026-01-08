# Progressive Agents: A Context Engineering Journey

## Overview

This guide provides a comprehensive walkthrough of the progressive agent stages, demonstrating **why context engineering matters** through working implementations. Each stage builds on the previous, showing the evolution from naive RAG to production-ready agents.

The Core Thesis: Context engineering is real engineering. It requires the same rigor, analysis, and deliberate decision-making as any other engineering discipline. Context is more than just "data you feed to an LLM". It requires thoughtful preparation, quality assessment, and optimization.

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
- RawContextAssembler retrieves courses and dumps them as-is 
- Every field is included: IDs, timestamps, internal metadata 
- JSON formatting adds overhead (brackets, quotes, indentation)
- The LLM receives thousands of tokens of irrelevant details

**What it demonstrates:**
- ~6,000+ tokens for a simple query
- Slow response times
- Wasted API costs
- The "dump everything" anti-pattern

### The Problems (Why This Matters)

From the workshop notebooks (Section 2, Notebook 2):

> "The goal is not only to give the LLM 'all the data'—it's to give it the *useful* data."

**1. Excessive Token Usage**
- 10 courses ≈ 1,700 tokens
- 100 courses would be ~17,000 tokens
- At $2.50/million tokens, this adds up fast

**2. Raw JSON is Inefficient**
- Includes internal fields (IDs, timestamps, created_at, updated_at)
- Verbose formatting wastes tokens
- Field names repeated for every record

**3. Context Rot and Poisoning**
- **Context rot**: As irrelevant content accumulates, LLM attention degrades non-uniformly across the context window. Important information gets "lost in the middle."
- **Context poisoning**: Noise actively competes for attention weights. Internal IDs, timestamps, and metadata don't just waste tokens—they dilute the signal-to-noise ratio, causing the model to attend to irrelevant patterns.
- The more noise in context, the harder the model works to find relevant information, and the higher the probability of hallucination or missed details.

**4. Poor Response Quality**
- Generic responses ("We have many courses...")
- May miss the most relevant courses
- Can't provide personalized recommendations
- Increased hallucination risk due to context poisoning

**Architecture:**
```
┌─────────────────┐
│   User Query    │
└────────┬────────┘
         ▼
┌─────────────────┐
│    research     │ ← Retrieves ALL matching courses
│   (semantic     │   Returns FULL details for each
│    search)      │   No filtering, no optimization
└────────┬────────┘
         ▼
┌─────────────────┐
│   synthesize    │ ← Receives ~6,000+ tokens
│   (LLM call)    │   Must process everything
└────────┬────────┘
         ▼
┌─────────────────┐
│  Final Answer   │
└─────────────────┘
```
**Key Files:**
- `stage1_baseline_rag/agent/nodes.py` - Uses `RawContextAssembler`
- `stage1_baseline_rag/agent/workflow.py` - Simple 2-node workflow

**Talk Track:**
> "This is what happens when we simply dump everything into the LLM. It works, but it's expensive and slow. 
> The LLM receives thousands of tokens of irrelevant details. We're paying for tokens 
> we don't need and making the model work harder to find the answer."
> > Technically speaking, this demonstrates the baseline—raw context assembly with no optimization. When we execute this query, observe the token count in the metrics output.
>
> *[Run: `python cli.py "What machine learning courses are available?"`]*
>
> The system retrieved 10 courses and serialized them as JSON with all fields intact. Token count: approximately 6,000. At scale—100 courses—that becomes 17,000 tokens per request.
>
> Examine `nodes.py`: the `RawContextAssembler` performs no transformation. It includes `created_at`, `updated_at`, internal IDs—fields that provide zero value for answering the user's question but consume tokens.
>
> In production usecases, this could contain a lot of noise, whch actively degrades response quality through two mechanisms: Context Rot and Poisoning
>
> The fundamental issue isn't that the LLM can't handle this—it can. But we're degrading its performance by forcing it to filter noise that we could have removed upstream. We're also consuming context window space that could be used for conversation history, user preferences, or additional retrieved context.
>
> This establishes our baseline. Stage 2 introduces the context engineering pipeline that addresses these inefficiencies."


---

## The Solution: Context Engineering

### Stage 2: Context-Engineered Agent

Stage 2 introduces the **context engineering pipeline**—a systematic approach to transforming raw data into LLM-optimized context. This is where we apply the engineering mindset: Extract → Clean → Transform → Optimize.

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
> we're removing noise. The LLM gets exactly what it needs to answer the question.
> 
> Observe the token count difference.
>
> *[Run: `python cli.py "What machine learning courses are available?"`]*
>
> Token count: approximately 539. That's a 91% reduction from Stage 1's 6,000 tokens.
>
> Open `context_engineering.py` and examine the three functions. The pipeline is straightforward:
>
> **First, `transform_course_to_text()`** converts JSON to natural language. Instead of `{"course_code": "CS301", "title": "Machine Learning"}`, we get `CS301: Machine Learning`. No brackets, no quotes, no field name repetition.
>
> **Second, `optimize_course_text()`** truncates descriptions. A 500-word course description becomes 100 characters plus ellipsis. For overview queries, this is sufficient. For detail queries, we'd use the full version—that's a decision we'll revisit in Stage 3.
>
> **Third, `format_courses_for_llm()`** structures multiple courses with clear separators. The LLM can parse this efficiently.
>
> The key insight: we're not losing information that matters for answering the query. We're removing noise. The LLM doesn't need `created_at: 2024-01-15T08:30:00Z` to recommend a machine learning course.
>
> This is the beginning of context engineering: deliberate decisions about what to include, what to exclude, and how to format. Every token should earn its place in the context window."

---

## Scaling Up: Full Agent Architecture

### Stage 3: Full Agent (LangGraph Workflow)

Stage 3 transforms the simple pipeline into an agent architecture using LangGraph. It introduces intent classification, query decomposition, hierarchical retrieval, and quality evaluation—the components needed for production-grade agents.

**What changes from Stage 2:**
- Adds intent classification (greeting vs. query)
  - Routes queries to appropriate handlers. Greetings don't need course retrieval.
- Adds query decomposition for complex questions
  - Complex queries like "Compare ML courses and tell me which has the easiest prerequisites" become:
    - Sub-query 1: "What ML courses are available?"
    - Sub-query 2: "What are the prerequisites for each?"
    - Sub-query 3: "Which prerequisites are easiest?"
- Adds hierarchical retrieval (summaries + details)
  - Instead of full details for all courses OR summaries for all courses, we provide:
    - Summaries for ALL matching courses (user sees the full landscape)
    - Details for TOP N courses (user gets depth where it matters)
    - Supplement: the "Lost in the Middle" research finding—LLMs perform better when important information is at the beginning or end of context, not buried in the middle.
- Adds quality evaluation loop
- Full LangGraph workflow with conditional routing

**Key Concepts:**
1. **Progressive Disclosure**: Summaries for all courses, details for top N
2. **Hierarchical Context**: Two-tier retrieval reduces tokens further
3. **Quality Loop**: Re-research if answer quality is low

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
> "Now we have an agent that understands intent, breaks down complex questions,
> and uses hierarchical retrieval. The quality loop ensures we don't give bad answers.
> 
>> This is where we transition from a pipeline to an agent. The difference is decision-making: the system now routes, evaluates, and iterates based on the query and results.
>
> *[Run: `python cli.py "Hello!"`]*
>
> Notice the execution path: `classify_intent → greeting_response → format_response`. No course retrieval—the system recognized this as a greeting and responded appropriately. That's intent classification saving unnecessary work.
>
> *[Run: `python cli.py "What machine learning courses are available and which one is best for beginners?"`]*
>
> Now observe the execution path: `classify_intent → decompose_query → research → synthesize → evaluate_quality → format_response`. The query was decomposed into sub-questions, researched with hierarchical retrieval, and quality-checked before responding.
>
> Open `workflow.py` and examine the conditional edges:
>
> ```python
> workflow.add_conditional_edges(
>     "classify_intent",
>     route_by_intent,
>     {"greeting": "greeting_response", "query": "decompose_query"}
> )
> ```
>
> Advantage of a framework like LangGraph: declarative workflow definition with conditional routing. The graph structure makes the agent's decision logic explicit and debuggable.
>
> The hierarchical retrieval is particularly important. Look at the context structure: summaries for all courses, then detailed information for the top 3. This pattern—progressive disclosure—gives the LLM both breadth and depth without overwhelming the context window.
>
> Research on 'Lost in the Middle' (Liu et al., 2023) shows LLMs struggle with information buried in long contexts. By structuring our context with summaries first and details at the end, we're engineering around this limitation."


---

## Adding Intelligence: Hybrid Search

### Stage 4: Hybrid Search (ReAct Pattern)

Stage 4 introduces **hybrid search**—combining semantic (vector) search with keyword (BM25) search and ReAct Pattern. This addresses a fundamental limitation of pure vector search: it can miss exact matches that keyword search would find.


**What changes from Stage 3:**
- Introduces ReAct pattern (Thought → Action → Observation)
- Adds entity extraction for course codes
- Combines exact match (FilterQuery) + semantic search
- Visible reasoning traces

**Key Concepts:**
1. **ReAct Loop**: Explicit reasoning before each action
2. **Hybrid Search**: Exact match for codes, semantic for concepts
   - Users search by exact identifiers (course codes, instructor names)
   - Domain has specific terminology that embeddings might not capture
   - You need both conceptual similarity AND exact matching
3. **Entity Extraction**: Detect course codes like "CS004"
4. **Stick with vector-only when:**
   - All queries are conceptual/semantic
   - Exact matching isn't important
   - Simplicity is prioritized over recall


**Talk Track:**
> "When a user asks about 'CS004', we don't want fuzzy semantic matching—we want
> exact lookup. Hybrid search gives us the best of both worlds.
> 
> Stage 4 addresses a limitation of pure vector search. Vector embeddings excel at semantic similarity—'machine learning' matches 'neural networks' and 'deep learning'. But they struggle with exact matches.
>
> *[Run: `python cli.py "Tell me about CS301"`]*
>
> With pure vector search, 'CS301' might not rank highest because the embedding doesn't capture that this is an exact course code lookup. The vector for 'CS301' might be similar to other CS courses.
>
> Hybrid search runs both vector AND keyword search in parallel, then fuses the results using Reciprocal Rank Fusion (RRF). If a document ranks high in both searches, it gets a higher combined score. If it ranks high in only one, it still appears but lower.
>
> Open `search.py` and examine the `hybrid_search()` function. Note the RRF constant `k=60`—this is the standard value from the original RRF paper. It controls how much weight is given to ranking position.
>
> The key insight: hybrid search is about coverage. Vector search finds conceptually related results. Keyword search finds exact matches. Together, they cover more query types than either alone.
>
> In production systems, you'd tune the balance between vector and keyword based on your query patterns. Some domains are more keyword-heavy (legal, medical with specific codes), others more semantic (creative, conversational)."


---

## Adding Memory: Conversational Context

### Stage 5: Working Memory (Session Context)

Stage 5 introduces **working memory**—the ability to maintain conversation context across turns. This solves the "grounding problem": resolving references like "it", "that course", "the one you mentioned".

**What changes from Stage 4:**
- Adds session-based working memory via Agent Memory Server
- Enables multi-turn conversations with context
- Tracks conversation history within a session
- Single tool: `search_courses`

**Key Concepts:**
1. **Working Memory**: Short-term, session-scoped conversation history
2. **Agent Memory Server**: External service for memory storage
3. **Session ID**: Groups related conversation turns


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
> 'CS004', then ask 'what are the prerequisites?' — it knows you mean CS004.
> 
> Stage 5 introduces working memory—the conversation history that enables multi-turn interactions. This solves what we call the 'grounding problem'.
>
> *[Run: `python cli.py "What machine learning courses are available?" --session-id demo1`]*
>
> Note the session ID. This creates a working memory session in the Agent Memory Server.
>
> *[Run: `python cli.py "Tell me more about the first one" --session-id demo1`]*
>
> The agent correctly resolves 'the first one' to CS301 because it has access to the previous turn. Without working memory, this query would fail—the agent wouldn't know what 'the first one' refers to.
>
> Open `memory.py` and examine the `load_working_memory()` and `save_working_memory()` functions. The pattern is:
>
> 1. Load working memory at the start of each turn
> 2. Include conversation history in the LLM context
> 3. Save updated working memory at the end of each turn
>
> The Agent Memory Server handles the storage and retrieval. It also handles memory management—truncation, summarization—to prevent unbounded growth.
>
> Every agents needs this. A 50-turn conversation is ~10,000 tokens just for history. At scale, you need strategies to manage this. The Agent Memory Server provides configurable policies: keep last N messages, summarize old messages, or sliding window with summaries.
>
> Working memory is session-scoped—it exists for the duration of a conversation. Stage 6 adds long-term memory that persists across sessions."


---

### Stage 6: Full Memory (Working + Long-term)

Stage 6 adds **long-term memory**—persistent storage of user preferences, facts, and knowledge that survives across sessions. This enables true personalization: the agent remembers that you're interested in AI, that you've completed CS101, that you prefer morning classes.

**What changes from Stage 5:**
- Adds long-term memory (cross-session personalization)
- Adds explicit memory tools for the agent to use
- Three tools: `search_courses`, `search_memories`, `store_memory`

**Key Concepts:**
1. **Long-term Memory**: Persists across sessions (preferences, facts)
2. **Explicit Memory Tools**: Agent decides when to store/retrieve memories
3. **Student ID**: Links memories to a specific user



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
> "Stage 6 completes the memory architecture with long-term memory. This is where personalization happens, 
> the agent now has true personalization. It remembers that you prefer Python courses,
> that you're interested in machine learning, and that you've already taken CS001.
> This persists across sessions. Come back tomorrow and it still knows you.
>
> *[Run: `python cli.py "I'm interested in machine learning and I've completed CS101" --user-id demo_user --session-id session1`]*
>
> The agent stored two facts to long-term memory: interest in ML, completion of CS101. These are now persistent.
>
> *[Start a new session]*
> *[Run: `python cli.py "What courses should I take?" --user-id demo_user --session-id session2`]*
>
> Different session, but same user. The agent retrieves the stored memories and provides personalized recommendations based on the user's stated interests and completed courses.
>
> Open `tools.py` and examine the three memory tools. The LLM decides when to use them—this is active memory management. When the user says 'I'm interested in...', the LLM recognizes this as information worth storing and calls `store_memory`.
>
> The distinction between working and long-term memory is critical:
>
> - **Working memory** is session-scoped. It enables 'Tell me more about the first one' within a conversation.
> - **Long-term memory** is user-scoped. It enables 'Remember I'm interested in ML' across conversations.
>
> Together, they create an agent that maintains both conversation continuity AND persistent personalization. This is the full context engineering stack: system context, user context (from long-term memory), conversation context (from working memory), and retrieved context (from course search).
>
> Each context type serves a purpose. Each is engineered deliberately. That's what separates a production agent from a demo."


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

