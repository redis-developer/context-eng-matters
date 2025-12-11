"""
Test Queries for Progressive Agents

This script provides common test scenarios for progressive agents:
1. Linear algebra and programming queries
2. Memory-based conversation queries
3. Hybrid search queries (exact match + semantic)

Run with different stages to see how context engineering improves results.
"""

# ============================================================================
# LINEAR ALGEBRA & PROGRAMMING QUERIES
# ============================================================================

LINEAR_ALGEBRA_PROGRAMMING = {
    "beginner_ml": "What machine learning courses are available for beginners?",
    
    "linear_algebra_focus": "I want to learn linear algebra for machine learning. What courses cover matrix operations and vector spaces?",
    
    "programming_foundations": "What programming courses should I take before starting machine learning?",
    
    "data_structures": "Which courses teach data structures and algorithms needed for AI development?",
    
    "math_prerequisites": "What math prerequisites do I need for deep learning courses?",
    
    "python_ml": "I know Python. What's the best path to learn machine learning implementation?",
    
    "neural_networks": "Which courses cover neural network mathematics and implementation?",
    
    "optimization": "What courses teach optimization algorithms used in machine learning?",
    
    "computational_complexity": "Are there courses on computational complexity for ML algorithms?",
    
    "numerical_methods": "What courses cover numerical methods for scientific computing and ML?",
}

# ============================================================================
# MEMORY-BASED CONVERSATION QUERIES
# ============================================================================

MEMORY_CONVERSATION = {
    "multi_turn_1": [
        "What Redis courses are available for beginners?",
        "What about the one you just mentioned?",  # Tests memory
        "How long will that take?",  # Tests reference resolution
        "What comes after that course?",  # Tests progression understanding
    ],
    
    "multi_turn_2": [
        "I'm interested in vector search",
        "Do I need any prerequisites for that?",  # Tests context retention
        "I've completed RU101. Am I ready?",  # Tests user context + memory
        "Great! Can you remind me what the course covers?",  # Tests memory
    ],
    
    "multi_turn_3": [
        "Tell me about machine learning courses",
        "Which one is best for someone with Python experience?",  # Tests filtering
        "What's the syllabus for that one?",  # Tests detail retrieval
        "How does it compare to the other courses you mentioned?",  # Tests comparison memory
    ],
    
    "preference_tracking": [
        "I prefer online courses",
        "What machine learning courses are available?",  # Should remember preference
        "Show me courses with hands-on projects",  # Adds another preference
        "What do you recommend based on what I told you?",  # Tests preference memory
    ],
}

# ============================================================================
# HYBRID SEARCH QUERIES (Exact Match + Semantic)
# ============================================================================

HYBRID_SEARCH = {
    # Exact course code queries
    "exact_code_1": "Tell me about RU101",
    "exact_code_2": "What are the prerequisites for RU301?",
    "exact_code_3": "Compare RU201 and RU202",
    "exact_code_4": "Is CS301 available online?",
    
    # Course name queries (should use semantic search)
    "course_name_1": "Tell me about Introduction to Redis Data Structures",
    "course_name_2": "What's in the Vector Similarity Search course?",
    
    # Mixed queries (exact + semantic)
    "mixed_1": "I completed RU101. What machine learning courses can I take?",
    "mixed_2": "After CS201, what's the best path for AI development?",
    
    # Department/category filters
    "department_1": "What Redis courses are available?",
    "department_2": "Show me all computer science courses",
    
    # Difficulty level queries
    "difficulty_1": "What beginner courses are available?",
    "difficulty_2": "I want advanced machine learning courses",
    "difficulty_3": "What intermediate Python courses do you have?",
    
    # Format/delivery queries
    "format_1": "Which courses are available online?",
    "format_2": "Do you have any self-paced courses?",
    "format_3": "What courses have hands-on projects?",
}

# ============================================================================
# COMPLEX QUERIES (Testing Progressive Disclosure)
# ============================================================================

COMPLEX_QUERIES = {
    # Overview queries (should return summaries only)
    "overview_1": "What courses do you offer?",
    "overview_2": "Give me an overview of machine learning courses",
    "overview_3": "What are my options for learning Redis?",
    
    # Detail queries (should return full syllabi)
    "detail_1": "What's the complete syllabus for RU301?",
    "detail_2": "Show me all assignments for the machine learning course",
    "detail_3": "What are the learning objectives for RU201?",
    
    # Prerequisite queries (should return prerequisite details)
    "prereq_1": "What do I need to know before taking RU301?",
    "prereq_2": "Can I take advanced ML courses without prerequisites?",
    "prereq_3": "What's the prerequisite chain for deep learning?",
}

# ============================================================================
# EDGE CASES & CHALLENGING QUERIES
# ============================================================================

EDGE_CASES = {
    # Ambiguous queries
    "ambiguous_1": "What's the best course?",
    "ambiguous_2": "Tell me about that course",  # Without context
    "ambiguous_3": "What should I take next?",  # Without user profile
    
    # No results expected
    "no_results_1": "Do you have courses on quantum computing?",
    "no_results_2": "What blockchain courses are available?",
    
    # Comparison queries
    "comparison_1": "What's the difference between RU201 and RU202?",
    "comparison_2": "Compare beginner and advanced ML courses",
    
    # Time/duration queries
    "time_1": "How long does it take to complete RU101?",
    "time_2": "What's the fastest path to learn vector search?",
}


def print_query_categories():
    """Print all query categories for easy reference"""
    print("=" * 80)
    print("TEST QUERY CATEGORIES")
    print("=" * 80)
    
    categories = [
        ("Linear Algebra & Programming", LINEAR_ALGEBRA_PROGRAMMING),
        ("Memory-Based Conversations", MEMORY_CONVERSATION),
        ("Hybrid Search", HYBRID_SEARCH),
        ("Complex Queries", COMPLEX_QUERIES),
        ("Edge Cases", EDGE_CASES),
    ]
    
    for category_name, queries in categories:
        print(f"\n{category_name}:")
        print("-" * 80)
        if isinstance(list(queries.values())[0], list):
            # Multi-turn conversations
            for key, conversation in queries.items():
                print(f"  {key}:")
                for i, turn in enumerate(conversation, 1):
                    print(f"    Turn {i}: {turn}")
        else:
            # Single queries
            for key, query in queries.items():
                print(f"  {key}: {query}")


if __name__ == "__main__":
    print_query_categories()

