"""
Redis Context Course BOA - Bank of America Workshop Version

This is a BOA-specific version of redis_context_course that uses Orchestra API
for embeddings and LLM calls. It's designed for the workshop_boa directory.

Key differences from the original:
- Uses Orchestra API instead of OpenAI
- Includes placeholder mode for testing without Orchestra
- Clear TODO markers for configuration
- Non-breaking changes with fallback support

Main Components:
- hierarchical_manager_boa: Course manager with Orchestra embeddings
- hierarchical_models: Data models (same as original)
- hierarchical_context: Context assemblers (same as original)
- redis_config_boa: Redis configuration with Orchestra support

Usage in workshop notebooks:
    # Import BOA version instead of original
    from redis_context_course_boa import HierarchicalCourseManager
    from redis_context_course_boa import CourseSummary, CourseDetails
    from redis_context_course_boa import HierarchicalContextAssembler
"""

# Import models from original package (no changes needed)
from redis_context_course.hierarchical_models import (
    Assignment,
    AssignmentType,
    CourseDetails,
    CourseSummary,
    CourseSyllabus,
    GradingPolicy,
    HierarchicalCourse,
    SyllabusWeek,
)

# Import context assemblers from original package (no changes needed)
from redis_context_course.hierarchical_context import (
    HierarchicalContextAssembler,
    FlatContextAssembler,
)

# Import BOA-specific components
from .hierarchical_manager_boa import HierarchicalCourseManager
from .redis_config_boa import RedisConfig, redis_config

__all__ = [
    # Core classes (BOA versions)
    "HierarchicalCourseManager",
    "RedisConfig",
    "redis_config",
    # Data models (from original)
    "CourseSummary",
    "CourseDetails",
    "HierarchicalCourse",
    "CourseSyllabus",
    "Assignment",
    "AssignmentType",
    "GradingPolicy",
    "SyllabusWeek",
    # Context assemblers (from original)
    "HierarchicalContextAssembler",
    "FlatContextAssembler",
]

