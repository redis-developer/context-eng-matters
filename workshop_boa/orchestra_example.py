"""
Example: Non-Breaking Orchestra Integration Pattern

This file demonstrates how to add Orchestra API support alongside existing code
without breaking anything. Copy these patterns into your notebooks.
"""
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from openai import OpenAI
# ============================================================================
# EXAMPLE 1: Embeddings - Side-by-side comparison
# ============================================================================

def example_embeddings_integration():
    """Shows how to add Orchestra embeddings without breaking existing code."""
    
    # ===== CURRENT CODE (KEEP THIS - IT WORKS) =====

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    query_embedding = embeddings.embed_query("machine learning courses")
    doc_embeddings = embeddings.embed_documents(["doc1", "doc2", "doc3"])
    
    print("✅ Current OpenAI embeddings working")
    
    # ===== TODO Orchestra: ALTERNATIVE (ADD AS COMMENTED CODE) =====
    """
    # Uncomment when ready to test Orchestra
    from orchestra_utils import OrchestraEmbeddings
    
    # Phase 1: Test with placeholder (uses OpenAI backend)
    embeddings = OrchestraEmbeddings(model="gpt-4o", use_placeholder=True)
    
    # Phase 2: Switch to real Orchestra API (when ready)
    # embeddings = OrchestraEmbeddings(model="gpt-4o")
    
    # Same interface - no other code changes needed!
    query_embedding = embeddings.embed_query("machine learning courses")
    doc_embeddings = embeddings.embed_documents(["doc1", "doc2", "doc3"])
    
    print("✅ Orchestra embeddings working")
    """


# ============================================================================
# EXAMPLE 2: LLM - Side-by-side comparison
# ============================================================================

def example_llm_integration():
    """Shows how to add Orchestra LLM without breaking existing code."""
    
    # ===== CURRENT CODE (KEEP THIS - IT WORKS) =====

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="What is Redis?")
    ]
    
    response = llm.invoke(messages)
    print(f"✅ Current OpenAI LLM response: {response.content[:50]}...")
    
    # ===== TODO Orchestra: ALTERNATIVE (ADD AS COMMENTED CODE) =====
    """
    # Uncomment when ready to test Orchestra
    from orchestra_utils import OrchestraLLM
    from langchain_core.messages import HumanMessage, SystemMessage
    
    # Phase 1: Test with placeholder (uses OpenAI backend)
    llm = OrchestraLLM(model="gpt-4.1", temperature=0, use_placeholder=True)
    
    # Phase 2: Switch to real Orchestra API (when ready)
    # llm = OrchestraLLM(model="gpt-4.1", temperature=0)
    
    # Same interface - no other code changes needed!
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="What is Redis?")
    ]
    
    response = llm.invoke(messages)
    print(f"✅ Orchestra LLM response: {response.content[:50]}...")
    """


# ============================================================================
# EXAMPLE 3: Direct API calls (for demos/examples)
# ============================================================================

def example_direct_api_integration():
    """Shows how to add Orchestra for direct API calls."""
    
    # ===== CURRENT CODE (KEEP THIS - IT WORKS) =====

    
    client = OpenAI()
    
    # Generate embeddings
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=["text1", "text2", "text3"]
    )
    embeddings_list = [item.embedding for item in response.data]
    
    print(f"✅ Current OpenAI direct API: {len(embeddings_list)} embeddings")
    
    # ===== TODO Orchestra: ALTERNATIVE (ADD AS COMMENTED CODE) =====
    """
    # Uncomment when ready to test Orchestra
    from orchestra_utils import create_orchestra_embeddings
    
    # Create Orchestra vectorizer
    vectorizer = create_orchestra_embeddings(model="gpt-4o")
    
    # Generate embeddings (same result, different API)
    embeddings_list = vectorizer.embed_many(["text1", "text2", "text3"])
    
    print(f"✅ Orchestra direct API: {len(embeddings_list)} embeddings")
    """


# ============================================================================
# EXAMPLE 4: Complete notebook cell pattern
# ============================================================================

def example_complete_cell_pattern():
    """
    Complete example showing how a notebook cell should look with TODO markers.
    
    This is the pattern to copy into notebooks:
    1. Keep existing working code
    2. Add commented Orchestra alternative below it
    3. Add clear TODO Orchestra marker
    4. Include both placeholder and production modes
    """
    
    print("""
# ============================================================================
# Notebook Cell: Initialize LLM and Embeddings
# ============================================================================

# Current working code (DO NOT MODIFY)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

print("✅ Initialized OpenAI LLM and embeddings")

# TODO Orchestra: Alternative implementation using Orchestra API
# Uncomment the section below when ready to test Orchestra integration
# This provides a drop-in replacement with the same interface
'''
from orchestra_utils import OrchestraLLM, OrchestraEmbeddings

# TESTING MODE: Use placeholder=True to test without Orchestra API
# This uses OpenAI backend but tests the Orchestra wrapper interface
llm = OrchestraLLM(model="gpt-4.1", temperature=0, use_placeholder=True)
embeddings = OrchestraEmbeddings(model="gpt-4o", use_placeholder=True)

# PRODUCTION MODE: Remove use_placeholder when ready for real Orchestra API
# Make sure ORCHESTRA_API_KEY environment variable is set
# llm = OrchestraLLM(model="gpt-4.1", temperature=0)
# embeddings = OrchestraEmbeddings(model="gpt-4o")

print("✅ Initialized Orchestra LLM and embeddings")
'''

# ============================================================================
# Rest of the notebook cell continues normally
# No other changes needed - the interface is identical!
# ============================================================================
    """)


# ============================================================================
# EXAMPLE 5: Environment setup
# ============================================================================

def example_environment_setup():
    """Shows how to set up environment for Orchestra."""
    
    print("""
# Add to your .env file (when ready for Orchestra):
ORCHESTRA_API_KEY=your_bearer_token_here

# Keep existing OpenAI key for fallback/testing:
OPENAI_API_KEY=your_openai_key_here

# In notebook, load both:
from dotenv import load_dotenv
load_dotenv()

# Now you can switch between OpenAI and Orchestra by changing use_placeholder flag
    """)


# ============================================================================
# Run examples
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("Orchestra Integration Examples - Non-Breaking Pattern")
    print("=" * 80)
    print("\nThese examples show how to add Orchestra support without breaking existing code.")
    print("Copy these patterns into your notebooks.\n")
    
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Embeddings Integration")
    print("=" * 80)
    example_embeddings_integration()
    
    print("\n" + "=" * 80)
    print("EXAMPLE 2: LLM Integration")
    print("=" * 80)
    example_llm_integration()
    
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Direct API Integration")
    print("=" * 80)
    example_direct_api_integration()
    
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Complete Cell Pattern")
    print("=" * 80)
    example_complete_cell_pattern()
    
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Environment Setup")
    print("=" * 80)
    example_environment_setup()

