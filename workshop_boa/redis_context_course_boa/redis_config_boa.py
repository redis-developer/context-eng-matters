"""
Redis configuration and connection management - BOA VERSION

This is a BOA-specific version that uses Orchestra API for embeddings.

Key changes from original:
- Uses Orchestra embeddings instead of OpenAI
- Supports placeholder mode for testing
- Clear TODO markers for configuration
"""

import os
from typing import Optional

import redis
from redisvl.index import SearchIndex
from redisvl.schema import IndexSchema


class RedisConfig:
    """Redis configuration management - BOA VERSION."""

    def __init__(
        self,
        redis_url: Optional[str] = None,
        vector_index_name: str = "course_catalog",
        checkpoint_namespace: str = "class_agent",
        use_placeholder: bool = False,
    ):
        """
        Initialize Redis configuration.
        
        Args:
            redis_url: Redis connection URL
            vector_index_name: Name for vector index
            checkpoint_namespace: Namespace for checkpoints
            use_placeholder: If True, uses OpenAI instead of Orchestra (for testing)
        """
        # TODO Orchestra: Update Redis URL if needed
        # Default: redis://localhost:6379
        # For BOA: Update to your Redis instance
        self.redis_url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379")
        
        # Allow override via environment variable for progressive agents
        self.vector_index_name = os.getenv("COURSE_INDEX_NAME", vector_index_name)
        self.checkpoint_namespace = checkpoint_namespace
        self.use_placeholder = use_placeholder

        # Initialize connections
        self._redis_client = None
        self._vector_index = None
        self._embeddings = None

    @property
    def redis_client(self) -> redis.Redis:
        """Get or create Redis client."""
        if self._redis_client is None:
            self._redis_client = redis.from_url(
                self.redis_url, decode_responses=False
            )
        return self._redis_client

    @property
    def embeddings(self):
        """Get or create embeddings function."""
        if self._embeddings is None:
            if self.use_placeholder:
                # TODO Orchestra: Using OpenAI as placeholder for testing
                print("⚠️  RedisConfig: Using OpenAI embeddings as placeholder")
                from langchain_openai import OpenAIEmbeddings
                self._embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            else:
                # TODO Orchestra: Use Orchestra embeddings
                # Import Orchestra utilities
                import sys
                sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
                from orchestra_utils import OrchestraEmbeddings
                
                # TODO Orchestra: Update these parameters as needed
                self._embeddings = OrchestraEmbeddings(
                    model="gpt-4o",  # TODO Orchestra: Update model name
                    user="workshop-user",  # TODO Orchestra: Update user identifier
                    data_privacy="confidential",  # TODO Orchestra: Update privacy level
                    residency="on-prem",  # TODO Orchestra: Update residency
                    source_id="workshop-boa"  # TODO Orchestra: Update source ID
                )
                print("✅ RedisConfig: Using Orchestra embeddings")
        
        return self._embeddings

    @property
    def vector_index(self) -> SearchIndex:
        """Get or create vector search index."""
        if self._vector_index is None:
            # Define schema for course catalog
            schema = IndexSchema.from_dict(
                {
                    "index": {
                        "name": self.vector_index_name,
                        "prefix": f"{self.vector_index_name}:",
                        "storage_type": "hash",
                    },
                    "fields": [
                        {"name": "id", "type": "tag"},
                        {"name": "course_code", "type": "tag"},
                        {"name": "title", "type": "text"},
                        {"name": "description", "type": "text"},
                        {"name": "department", "type": "tag"},
                        {"name": "major", "type": "tag"},
                        {"name": "difficulty_level", "type": "tag"},
                        {"name": "format", "type": "tag"},
                        {"name": "semester", "type": "tag"},
                        {"name": "year", "type": "numeric"},
                        {"name": "credits", "type": "numeric"},
                        {"name": "tags", "type": "tag"},
                        {
                            "name": "content_vector",
                            "type": "vector",
                            "attrs": {
                                "dims": 1536,
                                "distance_metric": "cosine",
                                "algorithm": "hnsw",
                                "datatype": "float32",
                            },
                        },
                    ],
                }
            )

            self._vector_index = SearchIndex(schema=schema)
            self._vector_index.set_client(self.redis_client)

        return self._vector_index

    def create_index(self, overwrite: bool = False):
        """Create the vector index in Redis."""
        try:
            self.vector_index.create(overwrite=overwrite)
            print(f"✅ Created vector index: {self.vector_index_name}")
        except Exception as e:
            if "Index already exists" in str(e):
                print(f"ℹ️  Vector index already exists: {self.vector_index_name}")
            else:
                raise


# Global instance for convenience
# TODO Orchestra: Set use_placeholder=False when ready for Orchestra API
redis_config = RedisConfig(use_placeholder=True)

