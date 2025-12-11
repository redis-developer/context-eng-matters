# Orchestra API Setup Instructions

Follow these steps to configure and test Orchestra API integration.

## Step 1: Add Orchestra API Key to Environment

### Option A: Using .env file (Recommended)

```bash
# Navigate to project root
cd /Users/nitin.kanukolanu/workspace/context-eng-matters

# Add to your .env file
echo "ORCHESTRA_API_KEY=your_actual_bearer_token_here" >> .env

# Optional: Customize API endpoints if needed
echo "ORCHESTRA_EMBED_URL=https://api-orchestra-dev.bankofamerica.com/api/v1/embed" >> .env
echo "ORCHESTRA_LLM_URL=https://api-orchestra-dev.bankofamerica.com/api/v1/chat/completions" >> .env
```

### Option B: Export in terminal session

```bash
export ORCHESTRA_API_KEY="your_actual_bearer_token_here"
export ORCHESTRA_EMBED_URL="https://api-orchestra-dev.bankofamerica.com/api/v1/embed"
export ORCHESTRA_LLM_URL="https://api-orchestra-dev.bankofamerica.com/api/v1/chat/completions"
```

## Step 2: Update Configuration Parameters

Edit `workshop_boa/orchestra_utils.py` if you need to change default parameters:

```python
# Find these lines and update as needed:
def create_orchestra_embeddings(
    model: str = "gpt-4o",              # TODO Orchestra: Update model name
    user: str = "user-123",             # TODO Orchestra: Update user identifier
    data_privacy: str = "confidential", # TODO Orchestra: Update privacy level
    residency: str = "on-prem",         # TODO Orchestra: Update residency
    source_id: str = "workshop-boa"     # TODO Orchestra: Update source ID
)
```

**Common updates needed:**
- `model`: Confirm correct model name with BOA team
- `user`: Use your BOA user identifier
- `data_privacy`: Confirm privacy classification
- `residency`: Confirm data residency requirements
- `source_id`: Use appropriate source identifier

## Step 3: Run Test Script

```bash
# Navigate to workshop_boa directory
cd workshop_boa

# Run the test script
python test_orchestra.py
```

The test script will:
1. ✅ Verify environment variables are set
2. ✅ Test embedding generation (single and batch)
3. ✅ Test LLM calls
4. ✅ Test CustomTextVectorizer (RedisVL compatibility)
5. ✅ Test LangChain compatibility
6. ✅ Show detailed results

## Step 4: Update Notebooks (When Tests Pass)

Once the test script passes, update notebooks by uncommenting the `#Orchestra change` sections:

### Example: Notebook 02 (Line 186)

**Before:**
```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

#Orchestra change: Alternative using Orchestra API (uncomment when ready)
# from orchestra_utils import OrchestraLLM, OrchestraEmbeddings
# llm = OrchestraLLM(model="gpt-4.1", temperature=0, use_placeholder=True)
# embeddings = OrchestraEmbeddings(model="gpt-4o", use_placeholder=True)
```

**After:**
```python
# Original OpenAI code (commented out)
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
# embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

#Orchestra change: Now using Orchestra API
from orchestra_utils import OrchestraLLM, OrchestraEmbeddings
llm = OrchestraLLM(model="gpt-4.1", temperature=0)
embeddings = OrchestraEmbeddings(model="gpt-4o")
```

## Step 5: Test Notebooks

Run each notebook to verify Orchestra integration works:

```bash
# Start Jupyter
jupyter notebook

# Or use VS Code notebook interface
```

Test in this order:
1. ✅ `02_rag_essentials.ipynb` - Tests embeddings and LLM
2. ✅ `03_data_engineering_theory.ipynb` - Tests hierarchical manager
3. ✅ `04_memory_systems.ipynb` - Tests LLM with memory

## Troubleshooting

### Error: "ORCHESTRA_API_KEY not set"
```bash
# Check if environment variable is set
echo $ORCHESTRA_API_KEY

# If empty, add to .env file or export it
export ORCHESTRA_API_KEY="your_token_here"
```

### Error: "401 Unauthorized"
- Verify your API key is correct
- Check if key has expired
- Confirm you have access to Orchestra API

### Error: "Invalid model name"
- Check with BOA team for correct model names
- Update `model` parameter in configuration

### Error: "Missing required metadata"
- Verify `data_privacy`, `residency`, `source_id` are set correctly
- Check Orchestra API documentation for required fields

### Error: "Connection refused"
- Verify API endpoint URLs are correct
- Check network connectivity to Orchestra API
- Confirm you're on BOA network/VPN if required

## Quick Reference

### Environment Variables
```bash
ORCHESTRA_API_KEY=your_bearer_token_here
ORCHESTRA_EMBED_URL=https://api-orchestra-dev.bankofamerica.com/api/v1/embed
ORCHESTRA_LLM_URL=https://api-orchestra-dev.bankofamerica.com/api/v1/chat/completions
```

### Test Commands
```bash
# Test Orchestra integration
python workshop_boa/test_orchestra.py

# Test with placeholder mode (uses OpenAI)
python workshop_boa/test_orchestra.py --placeholder

# Run notebooks
jupyter notebook workshop_boa/
```

### Files to Update
1. ✅ `.env` - Add ORCHESTRA_API_KEY
2. ✅ `workshop_boa/orchestra_utils.py` - Update default parameters (optional)
3. ✅ Notebooks - Uncomment `#Orchestra change` sections

## Next Steps After Setup

1. Run test script to verify configuration
2. Update one notebook at a time
3. Test each notebook thoroughly
4. Update configuration parameters as needed
5. Document any BOA-specific requirements

## Support

If you encounter issues:
1. Check `ORCHESTRA_INTEGRATION.md` for detailed examples
2. Review test script output for specific errors
3. Verify all configuration parameters are correct
4. Contact BOA Orchestra API support team

