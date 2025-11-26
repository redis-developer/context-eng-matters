# Stage 4 ReAct: Hybrid Search with ReAct Loop

## 📍 Position in Learning Path

| Previous | Current | Next |
|----------|---------|------|
| [Stage 4: Hybrid Search](../stage4_hybrid_search_with_ner/) | **Stage 4 ReAct** | [Stage 5: Memory](../stage5_memory_augmented/) or [Stage 5 ReAct](../stage5_react_memory/) |

This stage combines the hybrid search capabilities of Stage 4 with an explicit **ReAct** (Reasoning + Acting) loop for transparent reasoning.

---

## 🎯 Purpose

The ReAct pattern makes the agent's decision-making process **visible and debuggable**. Instead of opaque tool-calling, you see:
- **Thought**: What the agent is thinking
- **Action**: What tool it decides to use
- **Observation**: What results it receives

**Key Learning**: "Transparent reasoning improves debugging, trust, and understanding of agent behavior."

---

## 📚 Related Notebooks

| Notebook | Concepts Applied | Implementation in This Stage |
|----------|-----------------|------------------------------|
| [Section 4: Tools and LangGraph Fundamentals](../../notebooks/section-4-tools-and-agents/01_tools_and_langgraph_fundamentals.ipynb) | ReAct pattern, agent loops | `react_agent.py` - ReAct loop implementation |
| [Section 2: Crafting and Optimizing Context](../../notebooks/section-2-retrieved-context-engineering/02_crafting_and_optimizing_context.ipynb) | Hybrid search, progressive disclosure | `tools.py: search_courses_sync()` |

### Key Notebook Concepts Demonstrated

**From Section 4, Notebook 1 - "Tools and LangGraph Fundamentals":**
- **ReAct Pattern**: Thought → Action → Observation loop
- **Iterative Reasoning**: Multiple iterations until task complete
- **Explicit Termination**: FINISH action to end loop

**Study Path**: Read Section 4, Notebook 1's ReAct section, then examine `react_agent.py` and `react_prompts.py` to see the implementation.

---

## 🔄 What Changed from Stage 4

| Feature | Stage 4 | Stage 4 ReAct |
|---------|---------|---------------|
| **Reasoning** | Hidden (tool-calling) | **Visible** (Thought → Action → Observation) |
| **Decision Process** | Opaque LLM | **Transparent** reasoning trace |
| **Debugging** | Harder | **Easier** with `--show-reasoning` |
| **Iterations** | 1 | 2-3 (explicit loop) |

---

## 🏗️ Architecture

```mermaid
graph TD
    Q[Query] --> RA[ReAct Agent]

    subgraph ReAct Loop
        RA --> T1[💭 Thought: Analyze query]
        T1 --> A1[🔧 Action: search_courses]
        A1 --> O1[👁️ Observation: Results]
        O1 --> T2[💭 Thought: Evaluate]
        T2 --> |Need more| A1
        T2 --> |Done| F[✅ FINISH]
    end

    F --> R[Response + Reasoning Trace]
```

## 🚀 Usage

```bash
cd progressive_agents/stage4_react_hybrid_search

# Single query
python cli.py "What are the prerequisites for CS002?"

# Show reasoning trace
python cli.py --show-reasoning "What are the prerequisites for CS009?"

# Interactive mode
python cli.py

# Debug mode
python cli.py --debug "What's the syllabus for CS006?"
```

## 📁 File Structure

```
stage4_react_hybrid_search/
├── cli.py                    # Interactive CLI with --show-reasoning
├── README.md                 # This file
└── agent/
    ├── __init__.py          # Module exports
    ├── react_agent.py       # ReAct loop implementation
    ├── react_parser.py      # Output parsing (max_length=8000)
    ├── react_prompts.py     # System prompt with examples
    ├── tools.py             # search_courses tool with FilterQuery
    ├── state.py             # WorkflowState with reasoning_trace
    ├── setup.py             # CourseManager initialization
    └── workflow.py          # LangGraph workflow
```

## Key Fixes Applied

1. **Hierarchical Path**: Uses correct path `parent.parent.parent.parent / "src"`
2. **FilterQuery**: Exact course code matching instead of semantic search
3. **Observation Length**: 8000 chars to prevent syllabus truncation
4. **Empty Data Handling**: Prompt guidance for empty prerequisites

## Test Results

| Query | Time | Iterations | Result |
|-------|------|------------|--------|
| CS002 prerequisites (empty) | 5.1s | 2 | ✅ "no formal prerequisites" |
| CS009 prerequisites (has CS002) | 3.3s | 2 | ✅ "requires CS002" |
| CS006 syllabus | 7.3s | 2 | ✅ Full syllabus returned |

## Comparison with Other Stages

| Feature | Stage 4 | Stage 4 ReAct | Stage 7 |
|---------|---------|---------------|---------|
| Search | Hybrid | Hybrid | Hybrid |
| Reasoning | Hidden | **Visible** | Visible |
| Memory | None | None | Long-term |
| Iterations | 1 | 2 | 2-3 |

## Example Reasoning Trace

```
🧠 Reasoning Trace:
================================================================================
💭 Thought: The user is asking about prerequisites. I'll use exact match.

🔧 Action: search_courses
   Input: {"query": "CS002", "intent": "PREREQUISITES", "search_strategy": "exact_match", ...}
👁️  Observation: Found CS002 - Machine Learning Fundamentals...

💭 Thought: I found the course info. Prerequisites field is empty - this means no prerequisites required.

✅ FINISH
================================================================================
```

## 🔗 Related Resources

### Learning Path Navigation
- **Previous**: [Stage 4: Hybrid Search](../stage4_hybrid_search_with_ner/) - Same features without visible reasoning
- **Next Options**:
  - [Stage 5: Memory](../stage5_memory_augmented/) - Add working memory (hidden reasoning)
  - [Stage 5 ReAct](../stage5_react_memory/) - Add working memory with visible reasoning

### Notebooks to Study
- **[Section 4: Tools and LangGraph Fundamentals](../../notebooks/section-4-tools-and-agents/01_tools_and_langgraph_fundamentals.ipynb)**: ReAct pattern fundamentals
- **[Section 3: Working and Long-term Memory](../../notebooks/section-3-memory-systems/01_working_and_longterm_memory.ipynb)**: Prepare for Stage 5

