# Workshop BOA - Orchestra API Integration

This directory contains Bank of America-specific versions of the Context Engineering workshop materials with Orchestra API integration.

## 📁 Directory Structure

```
workshop_boa/
├── 01_introduction_to_context_engineering.ipynb  # No changes needed
├── 02_rag_essentials.ipynb                       # ✅ Updated with #Orchestra change markers
├── 03_data_engineering_theory.ipynb              # ✅ Updated with #Orchestra change markers
├── 04_memory_systems.ipynb                       # ✅ Updated with #Orchestra change markers
├── orchestra_utils.py                            # Orchestra API utilities
├── redis_context_course_boa/                     # BOA-specific package
│   ├── __init__.py
│   ├── hierarchical_manager_boa.py               # Uses CustomTextVectorizer
│   └── redis_config_boa.py                       # BOA Redis config
├── ORCHESTRA_INTEGRATION.md                      # Complete integration guide
└── README.md                                     # This file
```

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Add to your .env file
ORCHESTRA_API_KEY=your_bearer_token_here
```

### 2. Test with Placeholder Mode (No Orchestra API Required)

All notebooks can run in **placeholder mode** which uses OpenAI as a fallback while testing the Orchestra integration:

```python
# In any notebook, look for lines marked with:
#Orchestra change: Alternative using Orchestra API (uncomment when ready)

# Uncomment those lines and set use_placeholder=True
from orchestra_utils import OrchestraLLM, OrchestraEmbeddings
llm = OrchestraLLM(model="gpt-4.1", temperature=0, use_placeholder=True)
embeddings = OrchestraEmbeddings(model="gpt-4o", use_placeholder=True)
```

### 3. Switch to Orchestra API

```python
# Just remove the use_placeholder parameter
llm = OrchestraLLM(model="gpt-4.1", temperature=0)
embeddings = OrchestraEmbeddings(model="gpt-4o")
```

## 🔧 Components

### 1. `orchestra_utils.py`

Provides three integration patterns:

#### A. **CustomTextVectorizer** (RedisVL-compatible)
```python
from orchestra_utils import create_orchestra_embeddings

vectorizer = create_orchestra_embeddings(model="gpt-4o")
embedding = vectorizer.embed("single text")
embeddings = vectorizer.embed_many(["text1", "text2"])
```

#### B. **OrchestraEmbeddings** (LangChain-compatible)
```python
from orchestra_utils import OrchestraEmbeddings

embeddings = OrchestraEmbeddings(model="gpt-4o")
query_emb = embeddings.embed_query("search query")
doc_embs = embeddings.embed_documents(["doc1", "doc2"])
```

#### C. **OrchestraLLM** (LangChain-compatible)
```python
from orchestra_utils import OrchestraLLM

llm = OrchestraLLM(model="gpt-4.1", temperature=0)
response = llm.invoke(messages)
```

### 2. `redis_context_course_boa/`

BOA-specific version of the redis_context_course package:

```python
from redis_context_course_boa import HierarchicalCourseManager

# Test with placeholder mode
manager = HierarchicalCourseManager(use_placeholder=True)

# Use Orchestra API
manager = HierarchicalCourseManager(use_placeholder=False)
```

**Key Features:**
- ✅ Uses `CustomTextVectorizer` for RedisVL compatibility
- ✅ Supports placeholder mode for testing
- ✅ Clear TODO markers for configuration
- ✅ Non-breaking - original package still works

## 📝 Notebook Changes

All notebooks have been updated with `#Orchestra change` markers showing where Orchestra integration can be enabled.

### Notebook 02: RAG Essentials
- **Line 186**: LLM and embeddings initialization
- **Line 358**: Direct embedding API call
- **Line 674**: Query embedding (no changes needed)
- **Line 1205**: LLM for RAG pipeline

### Notebook 03: Data Engineering Theory
- **Line 117**: LLM and manager initialization

### Notebook 04: Memory Systems
- **Line 467**: LLM initialization

### Notebook 01: Introduction
- No changes needed (doesn't use OpenAI directly)

## 🔍 Key Differences from Original

| Feature | Original | BOA Version |
|---------|----------|-------------|
| **Embeddings** | OpenAI API | Orchestra API via CustomTextVectorizer |
| **LLM** | ChatOpenAI | OrchestraLLM |
| **Package** | `redis_context_course` | `redis_context_course_boa` |
| **Testing** | Requires OpenAI key | Supports placeholder mode |
| **RedisVL** | Uses OpenAIEmbeddings | Uses CustomTextVectorizer |

## 📋 Configuration Parameters

When switching to Orchestra API, update these parameters:

```python
# In orchestra_utils.py or when calling functions
create_orchestra_embeddings(
    model="gpt-4o",              # TODO Orchestra: Update model name
    user="workshop-user",        # TODO Orchestra: Update user identifier
    data_privacy="confidential", # TODO Orchestra: Update privacy level
    residency="on-prem",         # TODO Orchestra: Update residency
    source_id="workshop-boa"     # TODO Orchestra: Update source ID
)
```

## 🧪 Testing Strategy

### Phase 1: Current State ✅
- All notebooks work with existing OpenAI code
- `#Orchestra change` markers added
- No breaking changes

### Phase 2: Test with Placeholders
1. Uncomment Orchestra imports in notebooks
2. Set `use_placeholder=True`
3. Run notebooks - should work identically (uses OpenAI backend)

### Phase 3: Switch to Orchestra
1. Set `ORCHESTRA_API_KEY` environment variable
2. Update configuration parameters (model, user, data_privacy, etc.)
3. Change `use_placeholder=False` or remove parameter
4. Run notebooks - now using Orchestra API

## 📚 Documentation

- **`ORCHESTRA_INTEGRATION.md`** - Complete integration guide with examples
- **`orchestra_utils.py`** - Inline documentation for all functions
- **`redis_context_course_boa/`** - TODO markers in code for configuration

## 🔐 Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ORCHESTRA_API_KEY` | ✅ Yes | - | Bearer token for Orchestra API |
| `ORCHESTRA_EMBED_URL` | No | BOA default | Custom embedding endpoint |
| `ORCHESTRA_LLM_URL` | No | BOA default | Custom LLM endpoint |
| `REDIS_URL` | No | `redis://localhost:6379` | Redis connection URL |

## ✅ What's Complete

- ✅ `orchestra_utils.py` with CustomTextVectorizer support
- ✅ `redis_context_course_boa/` package with placeholder mode
- ✅ All notebooks updated with `#Orchestra change` markers
- ✅ Non-breaking integration (original code still works)
- ✅ Comprehensive documentation
- ✅ Testing strategy with placeholder mode

## 🎯 Next Steps

1. Review `#Orchestra change` markers in notebooks
2. Test in placeholder mode to verify integration works
3. Configure Orchestra API credentials
4. Update configuration parameters (model, user, data_privacy, etc.)
5. Switch to Orchestra API by removing `use_placeholder` parameter

## 📞 Support

For questions or issues:
1. Check `ORCHESTRA_INTEGRATION.md` for detailed examples
2. Review TODO markers in code for configuration requirements
3. Test with placeholder mode first to isolate issues
4. Verify `ORCHESTRA_API_KEY` is set correctly

