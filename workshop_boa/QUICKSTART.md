# Orchestra API - Quick Start Guide

## 🚀 When You Get Your Orchestra API Keys

Follow these 3 simple steps:

### Step 1: Add API Key to .env File

<details>
<summary><b>🐧 Linux / macOS</b></summary>

```bash
# Navigate to project root
cd /path/to/context-eng-matters

# Add your Orchestra API key
echo "ORCHESTRA_API_KEY=your_actual_bearer_token_here" >> .env
```
</details>

<details>
<summary><b>🪟 Windows</b></summary>

```powershell
# PowerShell - Navigate to project root
cd C:\path\to\context-eng-matters

# Add your Orchestra API key
Add-Content .env "ORCHESTRA_API_KEY=your_actual_bearer_token_here"

# Or edit manually
notepad .env
# Add this line: ORCHESTRA_API_KEY=your_actual_bearer_token_here
```

```cmd
# Command Prompt - Navigate to project root
cd C:\path\to\context-eng-matters

# Add your Orchestra API key
echo ORCHESTRA_API_KEY=your_actual_bearer_token_here >> .env

# Or edit manually
notepad .env
```
</details>

### Step 2: Run Test Script

<details>
<summary><b>🐧 Linux / macOS</b></summary>

```bash
# Test with Orchestra API
python workshop_boa/test_orchestra.py

# Or test with placeholder mode first (uses OpenAI)
python workshop_boa/test_orchestra.py --placeholder
```
</details>

<details>
<summary><b>🪟 Windows</b></summary>

```powershell
# PowerShell or Command Prompt
# Test with Orchestra API
python workshop_boa\test_orchestra.py

# Or test with placeholder mode first (uses OpenAI)
python workshop_boa\test_orchestra.py --placeholder
```

**Note:** Use backslashes (`\`) for paths on Windows.
</details>

**Expected output:**
```
======================================================================
Orchestra API Integration Test Suite
======================================================================

======================================================================
Test 1: Environment Variables
======================================================================

✅ ORCHESTRA_API_KEY is set (length: 64)

======================================================================
Test 2: Single Text Embedding
======================================================================

✅ Generated embedding with 1536 dimensions
✅ Embedding dimension is correct (1536)

... (more tests)

======================================================================
Test Summary
======================================================================

✅ Environment Variables
✅ Single Text Embedding
✅ Batch Text Embedding
✅ LangChain Embeddings
✅ LangChain LLM
✅ Direct LLM API
✅ Hierarchical Manager

======================================================================
✅ All tests passed! (7/7)
======================================================================
```

### Step 3: Update Notebooks

Once tests pass, update notebooks by uncommenting `#Orchestra change` sections:

**Example - In `02_rag_essentials.ipynb` around line 186:**

```python
# Comment out OpenAI code
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
# embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

#Orchestra change: Now using Orchestra API
from orchestra_utils import OrchestraLLM, OrchestraEmbeddings
llm = OrchestraLLM(model="gpt-4.1", temperature=0)
embeddings = OrchestraEmbeddings(model="gpt-4o")
```

---

## 📋 Configuration Parameters to Update

If needed, update these in `workshop_boa/orchestra_utils.py`:

```python
def create_orchestra_embeddings(
    model: str = "gpt-4o",              # ← Confirm with BOA team
    user: str = "user-123",             # ← Your BOA user ID
    data_privacy: str = "confidential", # ← Privacy classification
    residency: str = "on-prem",         # ← Data residency
    source_id: str = "workshop-boa"     # ← Source identifier
)
```

**Ask your BOA team:**
- ✅ Correct model names for embeddings and LLM
- ✅ Your user identifier
- ✅ Required data_privacy classification
- ✅ Required residency setting
- ✅ Appropriate source_id

---

## 🧪 Testing Strategy

### Phase 1: Test with Placeholder Mode ✅
```bash
# Uses OpenAI backend to verify integration works
python workshop_boa/test_orchestra.py --placeholder
```

### Phase 2: Test with Orchestra API ✅
```bash
# Uses real Orchestra API
python workshop_boa/test_orchestra.py
```

### Phase 3: Update Notebooks ✅
- Uncomment `#Orchestra change` sections
- Run notebooks one by one
- Verify everything works

---

## 🔍 What Gets Tested

The test script verifies:

1. ✅ **Environment Variables** - ORCHESTRA_API_KEY is set
2. ✅ **Single Text Embedding** - Generate embedding for one text
3. ✅ **Batch Text Embedding** - Generate embeddings for multiple texts
4. ✅ **LangChain Embeddings** - OrchestraEmbeddings compatibility
5. ✅ **LangChain LLM** - OrchestraLLM compatibility
6. ✅ **Direct LLM API** - call_orchestra_llm() function
7. ✅ **Hierarchical Manager** - BOA package integration

---

## 🔧 Troubleshooting

### "ORCHESTRA_API_KEY not set"
```bash
# Check if set
echo $ORCHESTRA_API_KEY

# Add to .env file
echo "ORCHESTRA_API_KEY=your_token" >> .env

# Or export directly
export ORCHESTRA_API_KEY="your_token"
```

### "401 Unauthorized"
- Verify API key is correct
- Check if key has expired
- Confirm you have Orchestra API access

### "Invalid model name"
- Check with BOA team for correct model names
- Update `model` parameter in configuration

### "Connection refused"
- Verify you're on BOA network/VPN
- Check API endpoint URLs are correct
- Test network connectivity

---

## 📁 Files Modified

When you uncomment `#Orchestra change` sections:

- ✅ `02_rag_essentials.ipynb` - Lines 186, 369, 1205
- ✅ `03_data_engineering_theory.ipynb` - Line 117
- ✅ `04_memory_systems.ipynb` - Line 467
- ✅ `01_introduction_to_context_engineering.ipynb` - No changes needed

---

## 📚 Documentation

- **`SETUP_INSTRUCTIONS.md`** - Detailed setup guide
- **`ORCHESTRA_INTEGRATION.md`** - Complete integration reference
- **`README.md`** - Workshop overview
- **`test_orchestra.py`** - Test script (this is what you run)

---

## ✅ Checklist

Before running notebooks with Orchestra API:

- [ ] Added `ORCHESTRA_API_KEY` to `.env` file
- [ ] Ran `python workshop_boa/test_orchestra.py` successfully
- [ ] All 7 tests passed
- [ ] Updated configuration parameters if needed
- [ ] Uncommented `#Orchestra change` sections in notebooks
- [ ] Tested notebooks one by one

---

## 🎯 Summary

**3 commands to get started:**

```bash
# 1. Add API key
echo "ORCHESTRA_API_KEY=your_token" >> .env

# 2. Run tests
python workshop_boa/test_orchestra.py

# 3. Update notebooks (uncomment #Orchestra change sections)
```

That's it! 🎉

For detailed instructions, see `SETUP_INSTRUCTIONS.md`

