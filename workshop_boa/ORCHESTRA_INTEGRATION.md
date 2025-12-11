# Orchestra API Integration Guide

This guide explains how to integrate Bank of America's Orchestra API into the workshop notebooks.

## Overview

The workshop now includes **non-breaking** Orchestra API support through:

1. **`orchestra_utils.py`** - Utility functions for Orchestra API
2. **`redis_context_course_boa/`** - BOA-specific version of redis_context_course package
3. **Placeholder mode** - Test integration without Orchestra API (uses OpenAI as fallback)

## Key Features

✅ **Non-Breaking**: All existing code continues to work  
✅ **Placeholder Mode**: Test without Orchestra API configured  
✅ **RedisVL Compatible**: Uses `CustomTextVectorizer` for RedisVL integration  
✅ **LangChain Compatible**: Drop-in replacements for `OpenAIEmbeddings` and `ChatOpenAI`  
✅ **Clear Markers**: All Orchestra changes marked with `#Orchestra change`

---

## Quick Start

### 1. Environment Setup

```bash
# Add to your .env file
ORCHESTRA_API_KEY=your_bearer_token_here

# Optional: Customize Orchestra API URL
ORCHESTRA_EMBED_URL=https://api-orchestra-dev.bankofamerica.com/api/v1/embed
ORCHESTRA_LLM_URL=https://api-orchestra-dev.bankofamerica.com/api/v1/chat/completions
```

### 2. Test with Placeholder Mode (No Orchestra API Required)

```python
# In any notebook cell
from orchestra_utils import OrchestraEmbeddings, OrchestraLLM

# Use placeholder mode - falls back to OpenAI
embeddings = OrchestraEmbeddings(model="gpt-4o", use_placeholder=True)
llm = OrchestraLLM(model="gpt-4.1", temperature=0, use_placeholder=True)

# Test it works
test_embedding = embeddings.embed_query("test query")
print(f"✅ Embedding dimension: {len(test_embedding)}")
```

### 3. Switch to Orchestra API (When Ready)

```python
# Just remove use_placeholder parameter
embeddings = OrchestraEmbeddings(model="gpt-4o")
llm = OrchestraLLM(model="gpt-4.1", temperature=0)
```

---

## Components

### 1. `orchestra_utils.py`

Three main components:

#### A. `create_orchestra_embeddings()` - RedisVL Compatible

Returns a `CustomTextVectorizer` for use with RedisVL:

```python
from orchestra_utils import create_orchestra_embeddings

# Create RedisVL-compatible vectorizer
vectorizer = create_orchestra_embeddings(
    model="gpt-4o",
    user="workshop-user",
    data_privacy="confidential",  # TODO Orchestra: Update as needed
    residency="on-prem",          # TODO Orchestra: Update as needed
    source_id="workshop-boa"      # TODO Orchestra: Update as needed
)

# Use with RedisVL
embedding = vectorizer.embed("single text")
embeddings = vectorizer.embed_many(["text1", "text2", "text3"])
```

#### B. `OrchestraEmbeddings` - LangChain Compatible

Drop-in replacement for `langchain_openai.OpenAIEmbeddings`:

```python
from orchestra_utils import OrchestraEmbeddings

# Same interface as OpenAIEmbeddings
embeddings = OrchestraEmbeddings(model="gpt-4o")
query_emb = embeddings.embed_query("search query")
doc_embs = embeddings.embed_documents(["doc1", "doc2"])
```

#### C. `OrchestraLLM` - LangChain Compatible

Drop-in replacement for `langchain_openai.ChatOpenAI`:

```python
from orchestra_utils import OrchestraLLM
from langchain_core.messages import HumanMessage, SystemMessage

# Same interface as ChatOpenAI
llm = OrchestraLLM(model="gpt-4.1", temperature=0)
response = llm.invoke([
    SystemMessage(content="You are helpful."),
    HumanMessage(content="What is Redis?")
])
```

#### D. `call_orchestra_llm()` - Direct API Access

For direct Orchestra API calls:

```python
from orchestra_utils import call_orchestra_llm

response = call_orchestra_llm(
    messages=[
        {"role": "system", "content": "You are helpful."},
        {"role": "user", "content": "What is Redis?"}
    ],
    model="gpt-4.1",
    temperature=0.0,
    max_tokens=1024
)

answer = response['choices'][0]['message']['content']
```

### 2. `redis_context_course_boa/` Package

BOA-specific version of the redis_context_course package:

```python
# Import BOA version instead of original
from redis_context_course_boa import HierarchicalCourseManager
from redis_context_course_boa import CourseSummary, CourseDetails
from redis_context_course_boa import HierarchicalContextAssembler

# Initialize with placeholder mode for testing
manager = HierarchicalCourseManager(use_placeholder=True)

# Or use Orchestra API (when ready)
manager = HierarchicalCourseManager(use_placeholder=False)
```

---

## Notebook Integration

All notebooks have been updated with `#Orchestra change` markers showing where Orchestra integration can be enabled.

### Pattern 1: Embeddings

```python
# Current code (keep this - it works)
from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

#Orchestra change: Alternative using Orchestra API (uncomment when ready)
# from orchestra_utils import OrchestraEmbeddings
# embeddings = OrchestraEmbeddings(model="gpt-4o", use_placeholder=True)  # Test mode
# embeddings = OrchestraEmbeddings(model="gpt-4o")  # Production mode
```

### Pattern 2: LLM

```python
# Current code (keep this - it works)
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

#Orchestra change: Alternative using Orchestra API (uncomment when ready)
# from orchestra_utils import OrchestraLLM
# llm = OrchestraLLM(model="gpt-4.1", temperature=0, use_placeholder=True)  # Test mode
# llm = OrchestraLLM(model="gpt-4.1", temperature=0)  # Production mode
```

### Pattern 3: Direct API Calls

```python
# Current code (keep this - it works)
from openai import OpenAI
client = OpenAI()
response = client.embeddings.create(model="text-embedding-3-small", input=texts)

#Orchestra change: Alternative using Orchestra API (uncomment when ready)
# from orchestra_utils import create_orchestra_embeddings
# vectorizer = create_orchestra_embeddings(model="gpt-4o")
# embeddings = vectorizer.embed_many(texts)
```

---

## Configuration Parameters

### TODO Orchestra: Update These Parameters

When switching to Orchestra API, update these parameters in your code:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `model` | `"gpt-4o"` | Model name for embeddings |
| `user` | `"workshop-user"` | User identifier |
| `data_privacy` | `"confidential"` | Data privacy level |
| `residency` | `"on-prem"` | Data residency requirement |
| `source_id` | `"workshop-boa"` | Source identifier |

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ORCHESTRA_API_KEY` | ✅ Yes | Bearer token for Orchestra API |
| `ORCHESTRA_EMBED_URL` | No | Custom embedding endpoint URL |
| `ORCHESTRA_LLM_URL` | No | Custom LLM endpoint URL |

---

## Testing Strategy

### Phase 1: Add Markers (Current State)
- All notebooks have `#Orchestra change` markers
- Existing code still works
- No changes needed

### Phase 2: Test with Placeholders
- Uncomment Orchestra imports
- Set `use_placeholder=True`
- Verify everything works (uses OpenAI backend)

### Phase 3: Switch to Orchestra
- Set `ORCHESTRA_API_KEY` environment variable
- Change `use_placeholder=False`
- Now using real Orchestra API

---

## Example: Complete Migration

```python
# ============================================================================
# BEFORE: Using OpenAI
# ============================================================================
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# ============================================================================
# AFTER: Using Orchestra (with placeholder mode for testing)
# ============================================================================
from orchestra_utils import OrchestraLLM, OrchestraEmbeddings

# Phase 1: Test with placeholder (uses OpenAI backend)
llm = OrchestraLLM(model="gpt-4.1", temperature=0, use_placeholder=True)
embeddings = OrchestraEmbeddings(model="gpt-4o", use_placeholder=True)

# Phase 2: Switch to Orchestra (when ready)
# llm = OrchestraLLM(model="gpt-4.1", temperature=0)
# embeddings = OrchestraEmbeddings(model="gpt-4o")

# ============================================================================
# Rest of code stays the same - same interface!
# ============================================================================
response = llm.invoke(messages)
query_embedding = embeddings.embed_query("search query")
```

---

## Support

For issues or questions:
1. Check that `ORCHESTRA_API_KEY` is set correctly
2. Try placeholder mode first to verify integration works
3. Check Orchestra API documentation for parameter requirements
4. Review `orchestra_utils.py` for implementation details

