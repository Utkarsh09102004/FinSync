#!/usr/bin/env python3
"""
FinSync Interactive Terminal Tester
Real-time testing interface for the CFO Agent with full event streaming
"""

import asyncio
import sys
import os
from datetime import datetime
from typing import Optional

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService

# Import your agent
from agent.cfoAgent.agent import root_agent

class FinSyncTerminalTester:
    def __init__(self):
        self.runner = None
        self.session = None
        self.user_id = "test_user"
        self.session_id = "test_session"
        self.verbose = True  # Show all events
        
    async def initialize(self):
        """Initialize the runner and session"""
        print("🚀 Initializing FinSync Terminal Tester...")
        
        # Create services
        session_service = InMemorySessionService()
        artifact_service = InMemoryArtifactService()
        
        # Create runner with your CFO agent
        self.runner = Runner(
            app_name="finsync_terminal_test",
            agent=root_agent,
            session_service=session_service,
            artifact_service=artifact_service
        )
        
        # Create session
        self.session = await session_service.create_session(
            app_name="finsync_terminal_test",
            user_id=self.user_id,
            session_id=self.session_id,
            state={}
        )
        
        print("✅ FinSync Terminal Tester initialized successfully!")
        print(f"📝 Session ID: {self.session_id}")
        print(f"👤 User ID: {self.user_id}")
        print(f"🤖 Agent: {root_agent.name}")
        print("=" * 80)
        
    async def process_query(self, user_input: str) -> str:
        """Process a single query and return the response"""
        print(f"\n🔄 Processing query: '{user_input}'")
        print("=" * 60)
        
        # Create content
        content = types.Content(role='user', parts=[types.Part(text=user_input)])
        
        final_response = ""
        event_count = 0
        
        try:
            # Process events
            async for event in self.runner.run_async(
                user_id=self.user_id,
                session_id=self.session_id,
                new_message=content
            ):
                event_count += 1
                
                # Show event details if verbose
                if self.verbose:
                    await self._display_event(event, event_count)
                
                # Capture final response
                if event.is_final_response():
                    if event.content and event.content.parts:
                        final_response = event.content.parts[0].text
                    elif hasattr(event, 'actions') and event.actions and hasattr(event.actions, 'escalate'):
                        final_response = f"⚠️ Agent escalated: {getattr(event, 'error_message', 'No specific message')}"
                    break
                    
        except Exception as e:
            final_response = f"❌ Error processing query: {str(e)}"
            print(f"❌ Exception occurred: {e}")
            
        print("=" * 60)
        print(f"📊 Total events processed: {event_count}")
        return final_response
        
    async def _display_event(self, event, event_num: int):
        """Display detailed event information"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        print(f"\n📋 Event #{event_num} [{timestamp}]")
        print(f"   👤 Author: {getattr(event, 'author', 'Unknown')}")
        print(f"   🏷️  Type: {type(event).__name__}")
        print(f"   ✅ Final: {event.is_final_response()}")
        
        # Show content if available
        if hasattr(event, 'content') and event.content:
            if event.content.parts:
                for i, part in enumerate(event.content.parts):
                    if hasattr(part, 'text') and part.text:
                        text_preview = part.text[:100] + "..." if len(part.text) > 100 else part.text
                        print(f"   💬 Text [{i}]: {text_preview}")
                    elif hasattr(part, 'function_call') and part.function_call:
                        print(f"   🔧 Tool Call [{i}]: {part.function_call.name}")
                        if hasattr(part.function_call, 'args') and part.function_call.args:
                            args_preview = str(part.function_call.args)[:100]
                            print(f"   📝 Args: {args_preview}")
                    elif hasattr(part, 'function_response') and part.function_response:
                        print(f"   🔧 Tool Response [{i}]: {part.function_response.name}")
                        if hasattr(part.function_response, 'response') and part.function_response.response:
                            resp_preview = str(part.function_response.response)[:100]
                            print(f"   📤 Response: {resp_preview}")
        
        # Show additional event details
        if hasattr(event, 'turn_complete') and event.turn_complete:
            print(f"   🔄 Turn Complete: {event.turn_complete}")
        if hasattr(event, 'interrupted') and event.interrupted:
            print(f"   ⏸️  Interrupted: {event.interrupted}")
            
    async def run_interactive_session(self):
        """Run the main interactive session"""
        print("\n🎯 FinSync Interactive Testing Session")
        print("Type 'quit' to exit, 'verbose' to toggle detailed logging, 'help' for commands")
        print("=" * 80)
        
        while True:
            try:
                # Get user input
                user_input = input(f"\n💼 FinSync> ").strip()
                
                # Handle special commands
                if not user_input:
                    continue
                elif user_input.lower() == 'quit':
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'verbose':
                    self.verbose = not self.verbose
                    print(f"🔍 Verbose mode: {'ON' if self.verbose else 'OFF'}")
                    continue
                elif user_input.lower() == 'help':
                    self._show_help()
                    continue
                elif user_input.lower() == 'status':
                    await self._show_status()
                    continue
                elif user_input.lower().startswith('test '):
                    await self._run_predefined_test(user_input[5:])
                    continue
                
                # Process the query
                response = await self.process_query(user_input)
                
                # Show final response
                print("\n" + "="*60)
                print("💡 FINAL RESPONSE:")
                print("="*60)
                print(response)
                print("="*60)
                
            except KeyboardInterrupt:
                print("\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                
    def _show_help(self):
        """Show help information"""
        print("\n📚 FINSYNC TERMINAL TESTER COMMANDS:")
        print("=" * 50)
        print("🔹 quit          - Exit the session")
        print("🔹 verbose       - Toggle detailed event logging")
        print("🔹 help          - Show this help message")
        print("🔹 status        - Show session status")
        print("🔹 test <name>   - Run predefined test")
        print("\n📝 SAMPLE QUERIES:")
        print("🔸 What was my revenue last quarter?")
        print("🔸 Show me the cash flow for this month")
        print("🔸 Calculate profit margins for Q2")
        print("🔸 What are my biggest expenses?")
        print("=" * 50)
        
    async def _show_status(self):
        """Show current session status"""
        print("\n📊 SESSION STATUS:")
        print("=" * 40)
        print(f"🎯 Agent: {root_agent.name}")
        print(f"👤 User ID: {self.user_id}")
        print(f"📝 Session ID: {self.session_id}")
        print(f"🔍 Verbose Mode: {'ON' if self.verbose else 'OFF'}")
        
        # Show session state if available
        if self.session and hasattr(self.session, 'state'):
            state_keys = list(self.session.state.keys()) if self.session.state else []
            print(f"💾 State Keys: {state_keys}")
        print("=" * 40)
        
    async def _run_predefined_test(self, test_name: str):
        """Run predefined test cases"""
        tests = {
            "basic": "What was my revenue last month?",
            "cash": "Show me my current cash position",
            "expenses": "What are my top 5 expenses this quarter?",
            "profit": "Calculate my profit margin for last quarter",
            "burn": "What was my cash burn rate last month?"
        }
        
        if test_name in tests:
            print(f"🧪 Running predefined test: {test_name}")
            await self.process_query(tests[test_name])
        else:
            print(f"❌ Unknown test: {test_name}")
            print(f"Available tests: {', '.join(tests.keys())}")

async def main():
    """Main function"""
    tester = FinSyncTerminalTester()
    
    try:
        await tester.initialize()
        await tester.run_interactive_session()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check if we're in an async context (like Jupyter)
    try:
        # Try to get the current event loop
        loop = asyncio.get_running_loop()
        print("⚠️  Running in async context (Jupyter/Colab)")
        print("Use: await main()")
    except RuntimeError:
        # We're in a normal Python script context
        asyncio.run(main())