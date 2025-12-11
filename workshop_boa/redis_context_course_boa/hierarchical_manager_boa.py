"""
Hierarchical course manager for two-tier retrieval - BOA VERSION

This is a BOA-specific version that uses Orchestra API for embeddings.
It implements progressive disclosure:
1. Search summaries (lightweight, fast)
2. Fetch details for top matches (comprehensive, on-demand)

Key changes from original:
- Uses Orchestra API for embeddings instead of OpenAI
- Supports placeholder mode for testing
- Clear TODO markers for configuration
"""

import json
import logging
import os
from typing import List, Optional, Tuple

import numpy as np
from redis import Redis
from redisvl.index import SearchIndex
from redisvl.query import VectorQuery
from redisvl.query.filter import Tag

# Import models from original package
from redis_context_course.hierarchical_models import (
    CourseDetails,
    CourseSummary,
    HierarchicalCourse,
)

from .redis_config_boa import redis_config

logger = logging.getLogger(__name__)


class HierarchicalCourseManager:
    """
    Manages two-tier course retrieval for progressive disclosure - BOA VERSION.

    Architecture:
    - Tier 1: Vector index of course summaries (for search)
    - Tier 2: Hash storage of full course details (for deep dives)

    This enables:
    - Fast initial search across all courses
    - Detailed information only for relevant courses
    - Efficient context budget management

    BOA-specific features:
    - Uses Orchestra API for embeddings
    - Supports placeholder mode (falls back to OpenAI for testing)
    - Clear TODO markers for configuration
    """

    def __init__(
        self,
        redis_client: Optional[Redis] = None,
        summary_index_name: str = "course_summaries",
        details_prefix: str = "course_details",
        use_placeholder: bool = False,
    ):
        """
        Initialize hierarchical course manager.

        Args:
            redis_client: Redis client (uses default if None)
            summary_index_name: Name for summary vector index
            details_prefix: Prefix for details hash keys
            use_placeholder: If True, uses OpenAI instead of Orchestra (for testing)
        """
        self.redis = redis_client or redis_config.redis_client
        self.summary_index_name = summary_index_name
        self.details_prefix = details_prefix
        self.use_placeholder = use_placeholder

        # Will be initialized when needed
        self._summary_index: Optional[SearchIndex] = None

        # Initialize embedding function
        self._init_embeddings()

    def _init_embeddings(self):
        """Initialize embedding function based on mode."""
        if self.use_placeholder:
            # TODO Orchestra: Using OpenAI as placeholder for testing
            # This allows testing without Orchestra API configured
            print("⚠️  HierarchicalCourseManager: Using OpenAI embeddings as placeholder")
            from openai import OpenAI
            self._openai_client = OpenAI()
            self._embedding_model = "text-embedding-ada-002"
            self._vectorizer = None  # Not using CustomTextVectorizer in placeholder mode
        else:
            # TODO Orchestra: Configure Orchestra API for embeddings
            # Set these environment variables:
            #   ORCHESTRA_API_KEY=your_bearer_token_here
            #   ORCHESTRA_EMBED_URL=https://api-orchestra-dev.bankofamerica.com/api/v1/embed

            # Import Orchestra utilities
            import sys
            sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
            from orchestra_utils import create_orchestra_embeddings

            # Create Orchestra CustomTextVectorizer (RedisVL-compatible)
            # TODO Orchestra: Update these parameters as needed
            self._vectorizer = create_orchestra_embeddings(
                model="gpt-4o",  # TODO Orchestra: Update model name if needed
                user="workshop-user",  # TODO Orchestra: Update user identifier
                data_privacy="confidential",  # TODO Orchestra: Update privacy level
                residency="on-prem",  # TODO Orchestra: Update residency requirement
                source_id="workshop-boa"  # TODO Orchestra: Update source identifier
            )
            self._openai_client = None
            print("✅ HierarchicalCourseManager: Using Orchestra CustomTextVectorizer")

    def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using configured backend.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        if self.use_placeholder:
            # Use OpenAI direct API
            response = self._openai_client.embeddings.create(
                model=self._embedding_model,
                input=text
            )
            return response.data[0].embedding
        else:
            # Use Orchestra CustomTextVectorizer (RedisVL-compatible)
            # CustomTextVectorizer has .embed() method for single text
            return self._vectorizer.embed(text)

    def _get_summary_index(self) -> SearchIndex:
        """Get or create summary vector index."""
        if self._summary_index is None:
            # Define index schema for summaries
            schema = {
                "index": {
                    "name": self.summary_index_name,
                    "prefix": f"{self.summary_index_name}:",
                    "storage_type": "hash",
                },
                "fields": [
                    {"name": "course_code", "type": "tag"},
                    {"name": "title", "type": "text"},
                    {"name": "department", "type": "tag"},
                    {"name": "difficulty_level", "type": "tag"},
                    {"name": "tags", "type": "tag"},
                    {"name": "embedding_text", "type": "text"},
                    {
                        "name": "embedding",
                        "type": "vector",
                        "attrs": {
                            "dims": 1536,  # OpenAI ada-002 dimensions
                            "algorithm": "hnsw",
                            "distance_metric": "cosine",
                        },
                    },
                ],
            }

            # Create index
            self._summary_index = SearchIndex.from_dict(schema)
            self._summary_index.set_client(self.redis)

            # Create index if it doesn't exist
            try:
                self._summary_index.create(overwrite=False)
            except Exception as e:
                logger.debug(f"Index already exists or error creating: {e}")

        return self._summary_index

    async def add_course(self, course: HierarchicalCourse) -> bool:
        """
        Add a hierarchical course to storage.

        Args:
            course: HierarchicalCourse with summary and details

        Returns:
            True if successful
        """
        try:
            # Store summary in vector index
            await self._store_summary(course.summary, course.id)

            # Store details in hash
            await self._store_details(course.details, course.id)

            logger.info(f"Added course: {course.summary.course_code}")
            return True

        except Exception as e:
            logger.error(f"Error adding course {course.summary.course_code}: {e}")
            return False

    async def _store_summary(self, summary: CourseSummary, course_id: str):
        """Store course summary in vector index."""
        # Generate embedding text if not present
        if not summary.embedding_text:
            summary.generate_embedding_text()

        # TODO Orchestra: Generate embedding using configured backend
        embedding = self._generate_embedding(summary.embedding_text)

        # Convert embedding to binary float32 for Redis vector search
        embedding_bytes = np.array(embedding, dtype=np.float32).tobytes()

        # Prepare data for storage
        data = {
            "id": course_id,
            "course_code": summary.course_code,
            "title": summary.title,
            "department": summary.department,
            "credits": str(summary.credits),
            "difficulty_level": summary.difficulty_level.value,
            "format": summary.format.value,
            "instructor": summary.instructor,
            "short_description": summary.short_description,
            "prerequisite_codes": "|".join(summary.prerequisite_codes),
            "tags": "|".join(summary.tags),
            "embedding_text": summary.embedding_text,
            "embedding": embedding_bytes,  # Binary float32 data
        }

        # Store in Redis
        key = f"{self.summary_index_name}:{course_id}"
        self.redis.hset(key, mapping=data)

        logger.debug(f"Stored summary for {summary.course_code}")

    async def _store_details(self, details: CourseDetails, course_id: str):
        """Store full course details in hash."""
        # Serialize details to JSON
        details_json = details.model_dump_json()

        # Store in Redis hash
        key = f"{self.details_prefix}:{course_id}"
        self.redis.set(key, details_json)

        logger.debug(f"Stored details for {details.course_code}")

    async def search_summaries(
        self,
        query: str,
        limit: int = 5,
        department: Optional[str] = None,
        difficulty: Optional[str] = None,
    ) -> List[CourseSummary]:
        """
        Search course summaries using vector similarity.

        Args:
            query: Search query
            limit: Maximum number of results
            department: Filter by department
            difficulty: Filter by difficulty level

        Returns:
            List of course summaries
        """
        # TODO Orchestra: Get embedding for query using configured backend
        query_embedding = self._generate_embedding(query)

        # Create vector query
        index = self._get_summary_index()
        vector_query = VectorQuery(
            vector=query_embedding,
            vector_field_name="embedding",
            return_fields=[
                "id",
                "course_code",
                "title",
                "department",
                "credits",
                "difficulty_level",
                "format",
                "instructor",
                "short_description",
                "prerequisite_codes",
                "tags",
            ],
            num_results=limit,
        )

        # Add filters if specified
        if department:
            vector_query.set_filter(Tag("department") == department)
        if difficulty:
            vector_query.set_filter(Tag("difficulty_level") == difficulty)


        # Execute search
        results = index.query(vector_query)

        # Convert results to CourseSummary objects
        summaries = []
        for result in results:
            try:
                from redis_context_course.models import DifficultyLevel, CourseFormat

                summary = CourseSummary(
                    course_code=result["course_code"],
                    title=result["title"],
                    department=result["department"],
                    credits=int(result["credits"]),
                    difficulty_level=DifficultyLevel(result["difficulty_level"]),
                    format=CourseFormat(result["format"]),
                    instructor=result["instructor"],
                    short_description=result["short_description"],
                    prerequisite_codes=result["prerequisite_codes"].split("|")
                    if result.get("prerequisite_codes")
                    else [],
                    tags=result["tags"].split("|") if result.get("tags") else [],
                )
                summaries.append(summary)
            except Exception as e:
                logger.warning(f"Error parsing summary result: {e}")
                continue

        logger.info(f"Found {len(summaries)} course summaries for query: '{query}'")
        return summaries

    async def _get_course_id(self, course_code: str) -> Optional[str]:
        """Get course ID from course code."""
        # Search for course by code
        index = self._get_summary_index()

        # Use tag filter to find exact match
        from redisvl.query import FilterQuery
        filter_query = FilterQuery(
            filter_expression=Tag("course_code") == course_code,
            return_fields=["id"],
            num_results=1,
        )

        results = index.query(filter_query)
        if results:
            return results[0]["id"]
        return None

    async def get_details(self, course_codes: List[str]) -> List[CourseDetails]:
        """
        Fetch full details for specific courses.

        Args:
            course_codes: List of course codes to fetch

        Returns:
            List of course details
        """
        details_list = []

        for course_code in course_codes:
            # Find course ID from summary index
            course_id = await self._get_course_id(course_code)
            if not course_id:
                logger.warning(f"Course not found: {course_code}")
                continue

            # Fetch details from hash
            key = f"{self.details_prefix}:{course_id}"
            details_json = self.redis.get(key)

            if details_json:
                details = CourseDetails.model_validate_json(details_json)
                details_list.append(details)
                logger.debug(f"Fetched details for {course_code}")
            else:
                logger.warning(f"Details not found for {course_code}")

        logger.info(f"Fetched {len(details_list)} course details")
        return details_list

    async def hierarchical_search(
        self, query: str, summary_limit: int = 5, detail_limit: int = 2, **filters
    ) -> Tuple[List[CourseSummary], List[CourseDetails]]:
        """
        Two-stage hierarchical retrieval.

        High-level workflow:
        1. Search summaries (lightweight, fast)
        2. Fetch details for top matches (comprehensive, on-demand)

        Args:
            query: Search query
            summary_limit: Number of summaries to return
            detail_limit: Number of detailed courses to fetch
            **filters: Additional filters (department, difficulty)

        Returns:
            Tuple of (summaries, details)
        """
        logger.info(
            f"Hierarchical search: '{query}' (summaries={summary_limit}, details={detail_limit})"
        )

        # Stage 1: Search summaries
        summaries = await self.search_summaries(
            query, limit=summary_limit, **filters
        )

        # Stage 2: Fetch details for top N courses
        if summaries and detail_limit > 0:
            top_course_codes = [s.course_code for s in summaries[:detail_limit]]
            details = await self.get_details(top_course_codes)
        else:
            details = []

        logger.info(
            f"Retrieved {len(summaries)} summaries and {len(details)} detailed courses"
        )
        return summaries, details


