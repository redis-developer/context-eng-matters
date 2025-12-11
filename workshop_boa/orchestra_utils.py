"""
Orchestra API Utilities for Bank of America Workshop

This module provides NON-BREAKING placeholder utilities for Orchestra API integration.
All functions are designed to be drop-in replacements that can be imported alongside
existing code without modifying working implementations.

Features:
1. Custom RedisVL-compatible embedding function using CustomTextVectorizer
2. LLM helper function for making calls to the Orchestra API
3. LangChain-compatible wrapper classes for seamless integration
4. Placeholder/passthrough mode for gradual migration

Usage in notebooks:
    # Option 1: Direct usage (when ready to switch)
    from orchestra_utils import create_orchestra_embeddings, call_orchestra_llm

    # Option 2: LangChain-compatible wrappers (drop-in replacement)
    from orchestra_utils import OrchestraEmbeddings, OrchestraLLM

    # Option 3: Placeholder mode (for testing without Orchestra API)
    from orchestra_utils import OrchestraEmbeddings
    embeddings = OrchestraEmbeddings(use_placeholder=True)  # Falls back to OpenAI
"""

import os
import requests
import json
from typing import List, Dict, Any, Optional, Union

try:
    from redisvl.utils.vectorize import CustomTextVectorizer
    REDISVL_AVAILABLE = True
except ImportError:
    REDISVL_AVAILABLE = False
    CustomTextVectorizer = None

try:
    from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
    from langchain_openai import OpenAIEmbeddings as LangChainOpenAIEmbeddings
    from langchain_openai import ChatOpenAI as LangChainChatOpenAI
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False


def create_orchestra_embeddings(
    model: str = "gpt-4o",
    authorization: Optional[str] = None,
    user: str = "user-123",
    data_privacy: str = "confidential",
    residency: str = "on-prem",
    source_id: str = "workshop-boa"
) -> CustomTextVectorizer:
    """
    Create a RedisVL-compatible embedding function using the Orchestra API.

    This function returns a CustomTextVectorizer that wraps the Orchestra API
    for generating embeddings. It can be used anywhere RedisVL expects an
    embedding function.

    The CustomTextVectorizer is RedisVL's standard interface for custom embeddings.
    It provides two methods:
    - embed(text: str) -> List[float]: Embed a single text
    - embed_many(texts: List[str]) -> List[List[float]]: Embed multiple texts

    Args:
        model: The embedding model to use (default: "gpt-4o")
               TODO Orchestra: Update this to match your Orchestra model name
        authorization: Bearer token for Orchestra API. If None, reads from
                      ORCHESTRA_API_KEY environment variable
                      TODO Orchestra: Set ORCHESTRA_API_KEY in your environment
        user: User identifier for the API call
              TODO Orchestra: Update to your user identifier
        data_privacy: Data privacy level (e.g., "confidential")
                     TODO Orchestra: Update to match your requirements
        residency: Data residency requirement (e.g., "on-prem")
                  TODO Orchestra: Update to match your requirements
        source_id: Source identifier for tracking
                  TODO Orchestra: Update to identify your application

    Returns:
        CustomTextVectorizer: A RedisVL-compatible vectorizer with embed() and embed_many() methods

    Example:
        # Create the vectorizer
        embeddings = create_orchestra_embeddings()

        # Use with RedisVL - single embedding
        embedding = embeddings.embed("Hello, world!")

        # Batch processing
        embeddings_list = embeddings.embed_many(
            ["Text 1", "Text 2", "Text 3"],
            batch_size=10
        )
    """
    if not REDISVL_AVAILABLE:
        raise ImportError(
            "RedisVL not available. Install with: pip install redisvl"
        )

    # TODO Orchestra: Get authorization token from parameter or environment
    # Set ORCHESTRA_API_KEY environment variable with your Bearer token
    auth_token = authorization or os.getenv("ORCHESTRA_API_KEY")
    if not auth_token:
        raise ValueError(
            "Authorization token required. Provide via 'authorization' parameter "
            "or set ORCHESTRA_API_KEY environment variable."
        )

    # TODO Orchestra: Update this URL to match your Orchestra API endpoint
    # Default: https://api-orchestra-dev.bankofamerica.com/api/v1/embed
    url = os.getenv("ORCHESTRA_EMBED_URL", "https://api-orchestra-dev.bankofamerica.com/api/v1/embed")
    
    def embed_single(text: str) -> List[float]:
        """Embed a single text string."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}",
        }
        payload = {
            "model": model,
            "input": [text],
            "user": user,
            "meta": {
                "data_privacy": data_privacy,
                "residency": residency,
                "source_id": source_id
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        # Assuming the API returns embeddings in a similar format to OpenAI
        # Adjust this based on actual Orchestra API response format
        return result['data'][0]['embedding']
    
    def embed_batch(texts: List[str]) -> List[List[float]]:
        """Embed a batch of text strings."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}",
        }
        payload = {
            "model": model,
            "input": texts,
            "user": user,
            "meta": {
                "data_privacy": data_privacy,
                "residency": residency,
                "source_id": source_id
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        # Extract embeddings from response
        return [item['embedding'] for item in result['data']]
    
    # Create and return CustomTextVectorizer
    return CustomTextVectorizer(
        embed=embed_single,
        embed_many=embed_batch
    )


def call_orchestra_llm(
    messages: List[Dict[str, Any]],
    tools: Optional[List[Dict[str, Any]]] = None,
    authorization: Optional[str] = None,
    temperature: float = 0.0,
    max_tokens: int = 1024,
    response_format: Optional[Dict[str, Any]] = None,
    node: str = '',
    model: str = 'gpt-4.1',
    caller: Optional[str] = None,
    redis_path: Optional[str] = None
) -> Union[Dict[str, Any], str]:
    """
    Make LLM calls to the Bank of America Orchestra API.

    This is a reusable helper function for making LLM calls to the Orchestra API
    with support for tools, structured outputs, and various parameters.

    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
        tools: Optional list of tool definitions for function calling
        authorization: Bearer token for Orchestra API. If None, reads from
                      ORCHESTRA_API_KEY environment variable
        temperature: Sampling temperature (0.0 to 2.0)
        max_tokens: Maximum tokens in the response
        response_format: Optional response format specification (e.g., {"type": "json_object"})
        node: Node identifier for routing
        model: Model to use (default: 'gpt-4.1')
        caller: Caller identifier for tracking
        redis_path: Optional Redis path for caching/storage

    Returns:
        Union[Dict[str, Any], str]: Full API response dict or just the content string

    Example:
        # Basic usage
        response = call_orchestra_llm(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is Redis?"}
            ],
            model="gpt-4o"
        )

        # With tools
        tools = [{
            "type": "function",
            "function": {
                "name": "search_courses",
                "description": "Search for courses",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"}
                    }
                }
            }
        }]
        response = call_orchestra_llm(
            messages=messages,
            tools=tools,
            temperature=0.0
        )
    """
    # Get authorization token from parameter or environment
    auth_token = authorization or os.getenv("ORCHESTRA_API_KEY")
    if not auth_token:
        raise ValueError(
            "Authorization token required. Provide via 'authorization' parameter "
            "or set ORCHESTRA_API_KEY environment variable."
        )

    url = "https://api-orchestra-dev.bankofamerica.com/api/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}",
    }

    # Build the payload
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    # Add optional parameters if provided
    if tools:
        payload["tools"] = tools

    if response_format:
        payload["response_format"] = response_format

    if node:
        payload["node"] = node

    if caller:
        payload["caller"] = caller

    if redis_path:
        payload["redis_path"] = redis_path

    # Make the API call
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()

    # Return the full response
    # Users can extract result['choices'][0]['message']['content'] if needed
    return result


# ============================================================================
# LangChain-Compatible Wrapper Classes (Non-Breaking Drop-In Replacements)
# ============================================================================

class OrchestraEmbeddings:
    """
    LangChain-compatible wrapper for Orchestra embeddings.

    This is a DROP-IN REPLACEMENT for langchain_openai.OpenAIEmbeddings.
    It has the same interface, so you can swap it without changing other code.

    Features:
    - Compatible with LangChain's embedding interface
    - Supports placeholder mode (falls back to OpenAI for testing)
    - Can be used anywhere OpenAIEmbeddings is used

    Usage:
        # TODO Orchestra: Replace OpenAIEmbeddings with OrchestraEmbeddings
        # from langchain_openai import OpenAIEmbeddings
        from orchestra_utils import OrchestraEmbeddings

        # Drop-in replacement - same interface
        embeddings = OrchestraEmbeddings(model="gpt-4o")
        query_embedding = embeddings.embed_query("search query")
        doc_embeddings = embeddings.embed_documents(["doc1", "doc2"])
    """

    def __init__(
        self,
        model: str = "gpt-4o",
        use_placeholder: bool = False,
        authorization: Optional[str] = None,
        user: str = "user-123",
        data_privacy: str = "confidential",
        residency: str = "on-prem",
        source_id: str = "workshop-boa",
        **kwargs
    ):
        """
        Initialize Orchestra embeddings wrapper.

        Args:
            model: Model to use for embeddings
            use_placeholder: If True, falls back to OpenAI (for testing without Orchestra)
            authorization: Bearer token (or set ORCHESTRA_API_KEY env var)
            user: User identifier
            data_privacy: Data privacy level
            residency: Data residency requirement
            source_id: Source identifier
            **kwargs: Additional arguments (for compatibility)
        """
        self.model = model
        self.use_placeholder = use_placeholder
        self.authorization = authorization
        self.user = user
        self.data_privacy = data_privacy
        self.residency = residency
        self.source_id = source_id

        # Initialize the appropriate backend
        if use_placeholder:
            if not LANGCHAIN_AVAILABLE:
                raise ImportError(
                    "LangChain not available. Install with: pip install langchain-openai"
                )
            # Use OpenAI as placeholder
            self._backend = LangChainOpenAIEmbeddings(model="text-embedding-3-small", **kwargs)
            print("⚠️  Using OpenAI embeddings as placeholder (use_placeholder=True)")
        else:
            # Use Orchestra
            if not REDISVL_AVAILABLE:
                raise ImportError(
                    "RedisVL not available. Install with: pip install redisvl"
                )
            self._vectorizer = create_orchestra_embeddings(
                model=model,
                authorization=authorization,
                user=user,
                data_privacy=data_privacy,
                residency=residency,
                source_id=source_id
            )

    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query text.

        This matches LangChain's OpenAIEmbeddings.embed_query() interface.
        """
        if self.use_placeholder:
            return self._backend.embed_query(text)
        return self._vectorizer.embed(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of documents.

        This matches LangChain's OpenAIEmbeddings.embed_documents() interface.
        """
        if self.use_placeholder:
            return self._backend.embed_documents(texts)
        return self._vectorizer.embed_many(texts)


class OrchestraLLM:
    """
    LangChain-compatible wrapper for Orchestra LLM.

    This is a DROP-IN REPLACEMENT for langchain_openai.ChatOpenAI.
    It has the same interface, so you can swap it without changing other code.

    Features:
    - Compatible with LangChain's ChatModel interface
    - Supports placeholder mode (falls back to OpenAI for testing)
    - Can be used anywhere ChatOpenAI is used

    Usage:
        # TODO Orchestra: Replace ChatOpenAI with OrchestraLLM
        # from langchain_openai import ChatOpenAI
        from orchestra_utils import OrchestraLLM

        # Drop-in replacement - same interface
        llm = OrchestraLLM(model="gpt-4.1", temperature=0.0)
        response = llm.invoke(messages)
    """

    def __init__(
        self,
        model: str = "gpt-4.1",
        temperature: float = 0.0,
        max_tokens: int = 1024,
        use_placeholder: bool = False,
        authorization: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize Orchestra LLM wrapper.

        Args:
            model: Model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            use_placeholder: If True, falls back to OpenAI (for testing without Orchestra)
            authorization: Bearer token (or set ORCHESTRA_API_KEY env var)
            **kwargs: Additional arguments (for compatibility)
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.use_placeholder = use_placeholder
        self.authorization = authorization
        self.kwargs = kwargs

        # Initialize the appropriate backend
        if use_placeholder:
            if not LANGCHAIN_AVAILABLE:
                raise ImportError(
                    "LangChain not available. Install with: pip install langchain-openai"
                )
            # Use OpenAI as placeholder
            openai_model = "gpt-4o-mini" if "gpt-4" in model else model
            self._backend = LangChainChatOpenAI(
                model=openai_model,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            print(f"⚠️  Using OpenAI {openai_model} as placeholder (use_placeholder=True)")

    def invoke(self, messages: Union[List[BaseMessage], List[Dict[str, Any]]]) -> AIMessage:
        """
        Invoke the LLM with messages.

        This matches LangChain's ChatOpenAI.invoke() interface.

        Args:
            messages: List of LangChain messages or dict messages

        Returns:
            AIMessage with the response
        """
        if self.use_placeholder:
            return self._backend.invoke(messages)

        # Convert LangChain messages to dict format for Orchestra API
        if messages and isinstance(messages[0], BaseMessage):
            messages_dict = [
                {
                    "role": self._convert_role(msg.type),
                    "content": msg.content
                }
                for msg in messages
            ]
        else:
            messages_dict = messages

        # Call Orchestra API
        response = call_orchestra_llm(
            messages=messages_dict,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            authorization=self.authorization,
            **self.kwargs
        )

        # Extract content and return as AIMessage
        content = response['choices'][0]['message']['content']
        return AIMessage(content=content)

    async def ainvoke(self, messages: Union[List[BaseMessage], List[Dict[str, Any]]]) -> AIMessage:
        """
        Async invoke (currently just calls sync version).

        TODO: Implement true async when Orchestra API supports it.
        """
        if self.use_placeholder:
            return await self._backend.ainvoke(messages)
        return self.invoke(messages)

    def _convert_role(self, langchain_role: str) -> str:
        """Convert LangChain message type to OpenAI role."""
        role_mapping = {
            "human": "user",
            "ai": "assistant",
            "system": "system",
            "function": "function",
        }
        return role_mapping.get(langchain_role, langchain_role)

