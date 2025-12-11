# Workshop BOA Setup - Pip Only (Windows + Python 3.13)

## Prerequisites

✅ **Python 3.13** (already installed)
✅ **Docker Desktop** running
✅ **OpenAI API key** (for testing/placeholder mode)
✅ **Orchestra API key** (for production BOA use)

---

## Complete Setup Instructions

### Step 1: Navigate to Project Directory

```powershell
cd C:\path\to\context-eng-matters
```

### Step 2: Create Virtual Environment

```powershell
# Create virtual environment
python -m venv .venv

# Activate it (PowerShell)
.venv\Scripts\Activate.ps1

# Or Command Prompt
.venv\Scripts\activate.bat
```

**If you get execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Dependencies (Python 3.13 Compatible)

```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install all other dependencies (skip pypdf)
pip install -r requirements.txt

# Install the package itself
pip install -e .
```

### Step 4: Configure Environment Variables

```powershell
# Copy example environment file
Copy-Item .env.example .env

# Edit .env file
notepad .env
```

**Add these to `.env`:**
```
# Required for testing/placeholder mode
OPENAI_API_KEY=your_openai_key_here

# Required for Orchestra API (BOA production)
ORCHESTRA_API_KEY=your_orchestra_bearer_token_here

# Redis and services
REDIS_URL=redis://localhost:6379
AGENT_MEMORY_SERVER_URL=http://localhost:8088
```

### Step 5: Start Docker Services

```powershell
# Start Redis and Agent Memory Server
docker-compose up -d

# Verify services are running
docker ps
```

You should see:
- `redis-stack` on port 6379
- `agent-memory-server` on port 8088

### Step 6: Load Course Data

```powershell
# Make sure virtual environment is activated (.venv in prompt)
python -m redis_context_course.scripts.load_hierarchical_courses -i src/redis_context_course/data/hierarchical/hierarchical_courses.json --force
```

### Step 7: Test Orchestra Integration

```powershell
# Test with placeholder mode (uses OpenAI - no Orchestra API needed)
python workshop_boa\test_orchestra.py --placeholder

# Test with Orchestra API (requires ORCHESTRA_API_KEY)
python workshop_boa\test_orchestra.py
```

**Expected output (7 tests):**
```
✅ Environment Variables
✅ Single Text Embedding
✅ Batch Text Embedding
✅ LangChain Embeddings
✅ LangChain LLM
✅ Direct LLM API
✅ Hierarchical Manager

✅ All tests passed! (7/7)
```

### Step 8: Run Workshop BOA Notebooks

**Open notebooks in order:**
1. `01_introduction_to_context_engineering.ipynb` - No changes needed
2. `02_rag_essentials.ipynb` - Has `#Orchestra change` markers
3. `03_data_engineering_theory.ipynb` - Has `#Orchestra change` markers
4. `04_memory_systems.ipynb` - Has `#Orchestra change` markers

---

## Using Orchestra API in Notebooks

### Option 1: Test with Placeholder Mode (Uses OpenAI)

Look for sections marked with `#Orchestra change` and uncomment them:

```python
# Comment out OpenAI code
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
# embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

#Orchestra change: Testing with placeholder mode
from orchestra_utils import OrchestraLLM, OrchestraEmbeddings
llm = OrchestraLLM(model="gpt-4.1", temperature=0, use_placeholder=True)
embeddings = OrchestraEmbeddings(model="gpt-4o", use_placeholder=True)
```

### Option 2: Use Real Orchestra API

```python
#Orchestra change: Using Orchestra API
from orchestra_utils import OrchestraLLM, OrchestraEmbeddings
llm = OrchestraLLM(model="gpt-4.1", temperature=0)
embeddings = OrchestraEmbeddings(model="gpt-4o")
```

---

## Notebooks with Orchestra Changes

| Notebook | Line | What to Change |
|----------|------|----------------|
| `02_rag_essentials.ipynb` | 186 | LLM and embeddings initialization |
| `02_rag_essentials.ipynb` | 358 | Direct embedding API call |
| `02_rag_essentials.ipynb` | 1205 | LLM for RAG pipeline |
| `03_data_engineering_theory.ipynb` | 117 | LLM and manager initialization |
| `04_memory_systems.ipynb` | 467 | LLM initialization |
| `01_introduction_to_context_engineering.ipynb` | - | No changes needed |

---

## Quick Test Commands

```powershell
# Activate virtual environment
.venv\Scripts\Activate.ps1

# Test Orchestra integration
python workshop_boa\test_orchestra.py

# Run a quick agent test
cd progressive_agents\stage4_hybrid_search
python cli.py --show-reasoning "What are the prerequisites for CS002?"

# Start Jupyter for notebooks
cd workshop_boa
jupyter notebook
```

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'redis_context_course'`

**Solution:**
```powershell
pip install -e .
```

### Issue: Docker services won't start

**Solution:**
```powershell
# Check if ports are in use
netstat -ano | findstr :6379
netstat -ano | findstr :8088

# Restart Docker Desktop
# Then:
docker-compose down
docker-compose up -d
```

### Issue: `ORCHESTRA_API_KEY not set`

**Solution:**
```powershell
# Check .env file
notepad .env

# Or set temporarily
$env:ORCHESTRA_API_KEY="your_token_here"
```

### Issue: Jupyter kernel crashes

**Solution:**
```powershell
pip install --upgrade ipykernel
python -m ipykernel install --user
```

---

## Summary - Copy/Paste Commands

```powershell
# 1. Setup
cd C:\path\to\context-eng-matters
python -m venv .venv
.venv\Scripts\Activate.ps1

# 2. Install (Python 3.13 compatible)
python -m pip install --upgrade pip
pip install "numpy>=2.1.0"
pip install langchain langchain-openai langchain-core langchain-community langchain-experimental langchain-text-splitters langgraph langgraph-checkpoint langgraph-checkpoint-redis redis redisvl openai agent-memory-client pydantic python-dotenv click rich tiktoken python-ulid faker pandas jupyter ipykernel sentence-transformers langchain-huggingface
pip install -e .

# 3. Configure
Copy-Item .env.example .env
notepad .env  # Add OPENAI_API_KEY and ORCHESTRA_API_KEY

# 4. Start services
docker-compose up -d

# 5. Load data
python -m redis_context_course.scripts.load_hierarchical_courses -i src/redis_context_course/data/hierarchical/hierarchical_courses.json --force

# 6. Test
python workshop_boa\test_orchestra.py --placeholder

# 7. Run notebooks
cd workshop_boa
jupyter notebook
```

---

## Documentation Files

- **`workshop_boa/QUICKSTART.md`** - Quick start guide
- **`workshop_boa/SETUP_INSTRUCTIONS.md`** - Detailed setup
- **`workshop_boa/ORCHESTRA_INTEGRATION.md`** - Complete integration reference
- **`workshop_boa/README.md`** - Workshop overview

---

## Python 3.13 Compatibility Notes

**Key Change:** NumPy 2.1.0+ is required for Python 3.13 support. Older versions (1.x, 2.0.x) do not support Python 3.13.

**Skipped Package:** `pypdf>=6.4.1` is not available for Python 3.13 yet. This package is only used for PDF processing and is not required for the workshop notebooks.

---

That's it! You're ready to run the BOA workshop with pip only on Python 3.13! 🎉

