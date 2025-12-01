#!/usr/bin/env python3
"""
Interactive CLI for the Stage 4 ReAct Course Q&A Agent.

Usage:
    python cli.py "your question"                    # Single query mode
    python cli.py --show-reasoning "your question"   # Show reasoning trace
    python cli.py --simulate                         # Simulate with example queries
"""

import asyncio
import atexit
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
env_path = Path(__file__).parent.parent / "src" / ".env"
load_dotenv(env_path)

# Add agent module to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agent import create_workflow, run_agent_async, setup_agent
from agent.setup import cleanup_courses


class ReActCLI:
    """Interactive CLI for Stage 4 ReAct Course Q&A Agent."""

    def __init__(
        self,
        cleanup_on_exit: bool = False,
        debug: bool = False,
        show_reasoning: bool = False,
    ):
        self.agent = None
        self.course_manager = None
        self.cleanup_on_exit = cleanup_on_exit
        self.debug = debug
        self.show_reasoning = show_reasoning

        if cleanup_on_exit:
            atexit.register(self._cleanup)

    def _cleanup(self):
        """Cleanup handler called on exit."""
        if self.course_manager and self.cleanup_on_exit:
            print("\n🧹 Cleaning up courses from Redis...")
            try:
                asyncio.run(cleanup_courses(self.course_manager))
                print("✅ Cleanup complete")
            except Exception as e:
                print(f"⚠️  Cleanup failed: {e}")

    async def initialize(self):
        """Initialize the agent and load course data."""
        print("=" * 80)
        print("Stage 4 ReAct Course Q&A Agent (Hybrid Search + ReAct Loop)")
        print("=" * 80)
        print()

        if not os.getenv("OPENAI_API_KEY"):
            print("❌ Error: OPENAI_API_KEY environment variable not set")
            sys.exit(1)

        try:
            print("🔧 Initializing Stage 4 ReAct Course Q&A Agent...")
            print("📦 Loading courses into Redis (if not already loaded)...")
            self.course_manager, _ = await setup_agent(auto_load_courses=True)
            print()

            print("🔧 Creating LangGraph workflow with ReAct loop...")
            self.agent = create_workflow(self.course_manager)
            print("✅ Workflow created successfully")
            print()

            if self.cleanup_on_exit:
                print("🧹 Courses will be cleaned up on exit")
            else:
                print("💾 Courses will persist in Redis after exit")
            print()

        except Exception as e:
            print(f"\n❌ Initialization failed: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()
            sys.exit(1)

    async def ask_question(self, query: str, show_details: bool = True):
        """Ask a question and get a response."""
        print("=" * 80)
        print(f"❓ Question: {query}")
        print("=" * 80)
        print()

        result = await run_agent_async(self.agent, query, enable_caching=False)

        # Show reasoning trace if enabled
        if self.show_reasoning and result.get("reasoning_trace"):
            print("🧠 Reasoning Trace:")
            print("=" * 80)
            for step in result["reasoning_trace"]:
                if step["type"] == "thought":
                    print(f"💭 Thought: {step['content']}")
                elif step["type"] == "action":
                    print(f"🔧 Action: {step['action']}")
                    print(f"   Input: {step['input']}")
                    obs_preview = step['observation'][:200] if len(step['observation']) > 200 else step['observation']
                    print(f"👁️  Observation: {obs_preview}...")
                elif step["type"] == "finish":
                    print(f"✅ FINISH")
                print()
            print("=" * 80)
            print()

        # Print the response
        print("📝 Answer:")
        print("-" * 80)
        print(result["final_response"])
        print("-" * 80)
        print()

        if show_details:
            metrics = result["metrics"]
            print("📊 Performance:")
            print(f"   Total Time: {metrics['total_latency']:.2f}ms")
            print(f"   ReAct Iterations: {result.get('react_iterations', 0)}")
            print(f"   Reasoning Steps: {len(result.get('reasoning_trace', []))}")
            print(f"   Execution: {metrics['execution_path']}")
            print()

        return result

    async def interactive_mode(self):
        """Run in interactive mode."""
        print("=" * 80)
        print("Interactive Mode - Ask questions about courses")
        print("Commands: 'quit' or 'exit' to stop, 'help' for help")
        print("=" * 80)
        print()

        while True:
            try:
                query = input("❓ Your question: ").strip()
                if not query:
                    continue
                if query.lower() in ["quit", "exit", "q"]:
                    print("\n👋 Goodbye!")
                    break
                print()
                await self.ask_question(query, show_details=True)
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                if self.debug:
                    import traceback
                    traceback.print_exc()


async def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Stage 4 ReAct Agent - Hybrid Search with ReAct Loop"
    )
    parser.add_argument("query", nargs="?", help="Question to ask")
    parser.add_argument("--simulate", action="store_true", help="Run simulation mode")
    parser.add_argument("--cleanup", action="store_true", help="Remove courses on exit")
    parser.add_argument("--debug", action="store_true", help="Show detailed errors")
    parser.add_argument("--show-reasoning", action="store_true", help="Show reasoning trace")

    args = parser.parse_args()

    cli = ReActCLI(
        cleanup_on_exit=args.cleanup,
        debug=args.debug,
        show_reasoning=args.show_reasoning,
    )
    await cli.initialize()

    if args.query:
        await cli.ask_question(args.query, show_details=True)
    else:
        await cli.interactive_mode()


if __name__ == "__main__":
    asyncio.run(main())

