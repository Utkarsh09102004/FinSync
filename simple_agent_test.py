#!/usr/bin/env python3
"""
Simple FinSync Agent Tester
Quick and clean testing interface for CFO Agent
"""

import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

# Import your agent
from agent.cfoAgent.agent import root_agent

async def test_agent(query: str):
    """Test the agent with a single query"""
    print(f"\n🔍 Testing: {query}")
    print("=" * 60)
    
    # Setup
    session_service = InMemorySessionService()
    runner = Runner(
        app_name="finsync_test",
        agent=root_agent,
        session_service=session_service
    )
    
    session = await session_service.create_session(
        app_name="finsync_test",
        user_id="test_user",
        session_id="test_session"
    )
    
    # Create message
    content = types.Content(role='user', parts=[types.Part(text=query)])
    
    print("🤖 Agent Response:")
    print("-" * 40)
    
    # Process events
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.session_id,
        new_message=content
    ):
        # Print any text content
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, 'text') and part.text:
                    print(part.text, end="")
                elif hasattr(part, 'function_call') and part.function_call:
                    print(f"\n🔧 [Tool Call: {part.function_call.name}]")
                elif hasattr(part, 'function_response') and part.function_response:
                    print(f"\n📤 [Tool Response: {part.function_response.name}]")
        
        if event.is_final_response():
            print("\n" + "=" * 60)
            break

async def interactive_mode():
    """Simple interactive mode"""
    print("🚀 FinSync Simple Agent Tester")
    print("Type your questions or 'quit' to exit")
    print("=" * 50)
    
    # Setup once
    session_service = InMemorySessionService()
    runner = Runner(
        app_name="finsync_interactive",
        agent=root_agent,
        session_service=session_service
    )
    
    session = await session_service.create_session(
        app_name="finsync_interactive",
        user_id="interactive_user",
        session_id="interactive_session"
    )
    
    while True:
        try:
            user_input = input("\n💼 > ").strip()
            
            if not user_input:
                continue
            if user_input.lower() == 'quit':
                print("👋 Goodbye!")
                break
                
            # Process query
            content = types.Content(role='user', parts=[types.Part(text=user_input)])
            
            print("\n🤖 Agent:")
            async for event in runner.run_async(
                user_id=session.user_id,
                session_id=session.session_id,
                new_message=content
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            print(part.text, end="")
                        elif hasattr(part, 'function_call') and part.function_call:
                            print(f"\n🔧 Calling: {part.function_call.name}")
                
                if event.is_final_response():
                    print("\n")
                    break
                    
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

# Test cases
TEST_QUERIES = [
    "What was my revenue last quarter?",
    "Show me my cash flow for this month", 
    "What are my biggest expenses?",
    "Calculate my profit margins",
    "How is my cash burn rate?"
]

async def run_test_suite():
    """Run all test queries"""
    print("🧪 Running FinSync Test Suite")
    print("=" * 50)
    
    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"\n📝 Test {i}/{len(TEST_QUERIES)}")
        await test_agent(query)
        
        if i < len(TEST_QUERIES):
            input("\nPress Enter to continue...")

def main():
    """Main menu"""
    print("🎯 FinSync Agent Testing Tool")
    print("=" * 40)
    print("1. Interactive Mode")
    print("2. Run Test Suite") 
    print("3. Single Query Test")
    print("4. Exit")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        asyncio.run(interactive_mode())
    elif choice == "2":
        asyncio.run(run_test_suite())
    elif choice == "3":
        query = input("Enter your query: ").strip()
        if query:
            asyncio.run(test_agent(query))
    elif choice == "4":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()