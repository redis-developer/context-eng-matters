#!/usr/bin/env python3
"""
Test script for Orchestra API integration.

Usage:
    python test_orchestra.py              # Test with Orchestra API
    python test_orchestra.py --placeholder # Test with OpenAI placeholder
"""

import os
import sys
import argparse
from typing import List

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_header(text: str):
    """Print section header."""
    print(f"\n{BLUE}{'=' * 70}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'=' * 70}{RESET}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{GREEN}✅ {text}{RESET}")


def print_error(text: str):
    """Print error message."""
    print(f"{RED}❌ {text}{RESET}")


def print_warning(text: str):
    """Print warning message."""
    print(f"{YELLOW}⚠️  {text}{RESET}")


def print_info(text: str):
    """Print info message."""
    print(f"ℹ️  {text}")


def test_environment_variables(use_placeholder: bool = False):
    """Test that required environment variables are set."""
    print_header("Test 1: Environment Variables")

    if use_placeholder:
        print_warning("Running in PLACEHOLDER mode - using OpenAI instead of Orchestra")
        print_info("Set OPENAI_API_KEY to test")

        if os.getenv("OPENAI_API_KEY"):
            print_success("OPENAI_API_KEY is set")
            return True
        else:
            print_error("OPENAI_API_KEY not set")
            return False
    else:
        print_info("Checking Orchestra API credentials...")

        api_key = os.getenv("ORCHESTRA_API_KEY")
        if api_key:
            print_success(f"ORCHESTRA_API_KEY is set (length: {len(api_key)})")
        else:
            print_error("ORCHESTRA_API_KEY not set")
            print_info("Add to .env file: ORCHESTRA_API_KEY=your_token_here")
            return False

        # Optional environment variables
        embed_url = os.getenv("ORCHESTRA_EMBED_URL")
        llm_url = os.getenv("ORCHESTRA_LLM_URL")

        if embed_url:
            print_info(f"ORCHESTRA_EMBED_URL: {embed_url}")
        else:
            print_info("ORCHESTRA_EMBED_URL: Using default")

        if llm_url:
            print_info(f"ORCHESTRA_LLM_URL: {llm_url}")
        else:
            print_info("ORCHESTRA_LLM_URL: Using default")

        return True


def test_embeddings_single(use_placeholder: bool = False):
    """Test single text embedding."""
    print_header("Test 2: Single Text Embedding")

    try:
        from orchestra_utils import create_orchestra_embeddings

        # Create vectorizer
        print_info("Creating CustomTextVectorizer...")
        vectorizer = create_orchestra_embeddings(
            model="gpt-4o",
            user="test-user",
            data_privacy="confidential",
            residency="on-prem",
            source_id="test-workshop"
        )

        # Test single embedding
        test_text = "Redis is an in-memory data structure store."
        print_info(f"Embedding text: '{test_text}'")

        embedding = vectorizer.embed(test_text)

        print_success(f"Generated embedding with {len(embedding)} dimensions")
        print_info(f"First 5 values: {embedding[:5]}")

        # Verify it's a valid embedding
        if len(embedding) == 1536:
            print_success("Embedding dimension is correct (1536)")
        else:
            print_warning(f"Unexpected embedding dimension: {len(embedding)}")

        return True

    except Exception as e:
        print_error(f"Failed to generate embedding: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_embeddings_batch(use_placeholder: bool = False):
    """Test batch text embedding."""
    print_header("Test 3: Batch Text Embedding")

    try:
        from orchestra_utils import create_orchestra_embeddings

        # Create vectorizer
        vectorizer = create_orchestra_embeddings(
            model="gpt-4o",
            user="test-user",
            data_privacy="confidential",
            residency="on-prem",
            source_id="test-workshop"
        )

        # Test batch embedding
        test_texts = [
            "Introduction to machine learning",
            "Deep learning with neural networks",
            "Redis vector search capabilities"
        ]
        print_info(f"Embedding {len(test_texts)} texts...")

        embeddings = vectorizer.embed_many(test_texts)

        print_success(f"Generated {len(embeddings)} embeddings")
        for i, emb in enumerate(embeddings):
            print_info(f"  Text {i+1}: {len(emb)} dimensions")

        return True

    except Exception as e:
        print_error(f"Failed to generate batch embeddings: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_langchain_llm(use_placeholder: bool = False):
    """Test LangChain-compatible LLM."""
    print_header("Test 5: LangChain-Compatible LLM")

    try:
        from orchestra_utils import OrchestraLLM
        from langchain_core.messages import HumanMessage, SystemMessage

        # Create LLM instance
        print_info("Creating OrchestraLLM...")
        llm = OrchestraLLM(
            model="gpt-4.1",
            temperature=0,
            use_placeholder=use_placeholder
        )

        # Test invoke
        messages = [
            SystemMessage(content="You are a helpful assistant. Answer in one sentence."),
            HumanMessage(content="What is Redis?")
        ]
        print_info("Testing LLM invoke with question: 'What is Redis?'")

        response = llm.invoke(messages)

        print_success("LLM response received")
        print_info(f"Response: {response.content[:100]}...")

        return True

    except Exception as e:
        print_error(f"Failed LangChain LLM test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_direct_llm_call(use_placeholder: bool = False):
    """Test direct Orchestra LLM API call."""
    print_header("Test 6: Direct LLM API Call")

    if use_placeholder:
        print_warning("Skipping direct API test in placeholder mode")
        return True

    try:
        from orchestra_utils import call_orchestra_llm

        # Test direct API call
        messages = [
            {"role": "system", "content": "You are helpful. Answer in one sentence."},
            {"role": "user", "content": "What is vector search?"}
        ]
        print_info("Testing direct API call...")

        response = call_orchestra_llm(
            messages=messages,
            model="gpt-4.1",
            temperature=0,
            max_tokens=100
        )

        answer = response['choices'][0]['message']['content']
        print_success("Direct API call successful")
        print_info(f"Response: {answer[:100]}...")

        return True

    except Exception as e:
        print_error(f"Failed direct LLM API test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_hierarchical_manager(use_placeholder: bool = False):
    """Test BOA HierarchicalCourseManager."""
    print_header("Test 7: BOA HierarchicalCourseManager")

    try:
        from redis_context_course_boa import HierarchicalCourseManager

        # Create manager
        print_info("Creating HierarchicalCourseManager...")
        manager = HierarchicalCourseManager(use_placeholder=use_placeholder)

        print_success("Manager initialized successfully")
        print_info(f"Summary index: {manager.summary_index_name}")
        print_info(f"Details prefix: {manager.details_prefix}")
        print_info(f"Placeholder mode: {manager.use_placeholder}")

        # Test embedding generation
        print_info("Testing internal embedding generation...")
        test_embedding = manager._generate_embedding("Test text for embedding")
        print_success(f"Generated embedding: {len(test_embedding)} dimensions")

        return True

    except Exception as e:
        print_error(f"Failed HierarchicalCourseManager test: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests(use_placeholder: bool = False):
    """Run all tests and report results."""
    print(f"\n{BLUE}{'=' * 70}{RESET}")
    print(f"{BLUE}Orchestra API Integration Test Suite{RESET}")
    print(f"{BLUE}{'=' * 70}{RESET}")

    if use_placeholder:
        print_warning("Running in PLACEHOLDER mode (using OpenAI)")
    else:
        print_info("Running with Orchestra API")

    results = []

    # Run tests
    results.append(("Environment Variables", test_environment_variables(use_placeholder)))

    if not results[0][1]:
        print_error("\nEnvironment setup failed. Please configure credentials first.")
        print_info("See SETUP_INSTRUCTIONS.md for details")
        return False

    results.append(("Single Text Embedding", test_embeddings_single(use_placeholder)))
    results.append(("Batch Text Embedding", test_embeddings_batch(use_placeholder)))
    results.append(("LangChain Embeddings", test_langchain_embeddings(use_placeholder)))
    results.append(("LangChain LLM", test_langchain_llm(use_placeholder)))
    results.append(("Direct LLM API", test_direct_llm_call(use_placeholder)))
    results.append(("Hierarchical Manager", test_hierarchical_manager(use_placeholder)))

    # Print summary
    print_header("Test Summary")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        if result:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")

    print(f"\n{BLUE}{'=' * 70}{RESET}")
    if passed == total:
        print_success(f"All tests passed! ({passed}/{total})")
        print_info("\nNext steps:")
        print_info("1. Update notebooks by uncommenting #Orchestra change sections")
        print_info("2. Test notebooks one by one")
        print_info("3. See SETUP_INSTRUCTIONS.md for details")
    else:
        print_error(f"Some tests failed ({passed}/{total} passed)")
        print_info("\nTroubleshooting:")
        print_info("1. Check SETUP_INSTRUCTIONS.md")
        print_info("2. Verify ORCHESTRA_API_KEY is correct")
        print_info("3. Check network connectivity to Orchestra API")
        print_info("4. Review error messages above")
    print(f"{BLUE}{'=' * 70}{RESET}\n")

    return passed == total


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Test Orchestra API integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_orchestra.py              # Test with Orchestra API
  python test_orchestra.py --placeholder # Test with OpenAI placeholder
        """
    )
    parser.add_argument(
        "--placeholder",
        action="store_true",
        help="Use OpenAI placeholder instead of Orchestra API"
    )

    args = parser.parse_args()

    success = run_all_tests(use_placeholder=args.placeholder)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()


def test_langchain_embeddings(use_placeholder: bool = False):
    """Test LangChain-compatible embeddings."""
    print_header("Test 4: LangChain-Compatible Embeddings")

    try:
        from orchestra_utils import OrchestraEmbeddings

        # Create embeddings instance
        print_info("Creating OrchestraEmbeddings...")
        embeddings = OrchestraEmbeddings(
            model="gpt-4o",
            use_placeholder=use_placeholder
        )

        # Test embed_query
        query = "What is Redis?"
        print_info(f"Testing embed_query: '{query}'")
        query_emb = embeddings.embed_query(query)
        print_success(f"Query embedding: {len(query_emb)} dimensions")

        # Test embed_documents
        docs = ["Redis is fast", "Redis supports vectors"]
        print_info(f"Testing embed_documents with {len(docs)} documents")
        doc_embs = embeddings.embed_documents(docs)
        print_success(f"Document embeddings: {len(doc_embs)} embeddings")

        return True

    except Exception as e:
        print_error(f"Failed LangChain embeddings test: {e}")
        import traceback
        traceback.print_exc()
        return False
