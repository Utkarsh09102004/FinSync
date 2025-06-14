#!/usr/bin/env python3
"""
Interactive Terminal Session for FinSync CFO Agent
Allows manual testing with prompts and additional context
"""

import asyncio
import sys
import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

# Import ADK components
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.genai import types

# Import our agent
from agent.cfoAgent.agent import cfo_agent

class InteractiveCFOSession:
    """Interactive session for testing CFO Agent"""
    
    def __init__(self):
        self.APP_NAME = "finsync_interactive"
        self.USER_ID = "interactive_user"
        self.SESSION_ID = f"session_{int(time.time())}"
        
        # Initialize services
        self.session_service = InMemorySessionService()
        self.artifact_service = InMemoryArtifactService()
        
        # Create runner
        self.runner = Runner(
            agent=cfo_agent,
            app_name=self.APP_NAME,
            session_service=self.session_service,
            artifact_service=self.artifact_service
        )
        
        self.conversation_history = []
        self.prompt_count = 0
        self.max_prompts = 5
    
    async def setup_session(self):
        """Initialize the session"""
        try:
            session = await self.session_service.create_session(
                app_name=self.APP_NAME,
                user_id=self.USER_ID,
                session_id=self.SESSION_ID
            )
            print(f"✅ Session initialized: {session.id}")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize session: {e}")
            return False
    
    def print_banner(self):
        """Print the welcome banner"""
        print("=" * 80)
        print("🏦 FINSYNC CFO AGENT - INTERACTIVE TESTING SESSION")
        print("=" * 80)
        print("Welcome to the FinSync CFO Agent interactive testing environment!")
        print(f"You can test up to {self.max_prompts} prompts in this session.")
        print()
        print("Commands:")
        print("  • Type your financial question normally")
        print("  • Type 'help' for agent capabilities")
        print("  • Type 'history' to see conversation history")
        print("  • Type 'clear' to clear the screen")
        print("  • Type 'quit' or 'exit' to end the session")
        print("=" * 80)
        print()
    
    def print_prompt_header(self, prompt_num):
        """Print header for each prompt"""
        print(f"\n{'='*60}")
        print(f"💬 PROMPT {prompt_num}/{self.max_prompts}")
        print(f"{'='*60}")
    
    async def send_message(self, message: str):
        """Send a message to the CFO agent and get response"""
        print(f"\n🤔 Thinking...")
        
        start_time = time.time()
        response_parts = []
        events_collected = []
        
        try:
            # Prepare the user message
            content = types.Content(role='user', parts=[types.Part(text=message)])
            
            # Run the agent and collect events
            print("🔄 Processing with CFO Agent...")
            
            async for event in self.runner.run_async(
                user_id=self.USER_ID,
                session_id=self.SESSION_ID,
                new_message=content
            ):
                # Collect events for analysis
                events_collected.append({
                    'author': event.author,
                    'timestamp': event.timestamp,
                    'is_final': event.is_final_response()
                })
                
                # Show progress for non-final events
                if not event.is_final_response() and event.content:
                    if hasattr(event.content, 'parts') and event.content.parts:
                        for part in event.content.parts:
                            if hasattr(part, 'function_call') and part.function_call:
                                print(f"🔧 Using tool: {part.function_call.name}")
                            elif hasattr(part, 'function_response') and part.function_response:
                                print(f"✅ Tool response received")
                
                # Collect final response
                if event.is_final_response():
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if part.text:
                                response_parts.append(part.text)
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # Combine response parts
            full_response = "".join(response_parts)
            
            if full_response:
                print(f"\n🤖 CFO Agent Response ({response_time:.2f}s):")
                print("-" * 60)
                print(full_response)
                print("-" * 60)
            else:
                print(f"\n❌ No response received from agent")
                full_response = "No response"
            
            # Store in conversation history
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'prompt': message,
                'response': full_response,
                'response_time': response_time,
                'events_count': len(events_collected)
            })
            
            return full_response
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"\n❌ {error_msg}")
            
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'prompt': message,
                'response': error_msg,
                'response_time': 0,
                'events_count': 0,
                'error': True
            })
            
            return error_msg
    
    def show_help(self):
        """Show help information"""
        print("\n📋 CFO AGENT CAPABILITIES:")
        print("-" * 40)
        print("• Financial data retrieval from Zoho Books")
        print("• Cash burn rate calculations")
        print("• Profit margin analysis")
        print("• Period-over-period comparisons")
        print("• Expense breakdown and analysis")
        print("• Revenue trend analysis")
        print()
        print("📝 EXAMPLE PROMPTS:")
        print("-" * 40)
        print("• 'What was our revenue last quarter?'")
        print("• 'Calculate our cash burn rate for Q2'")
        print("• 'Show me profit margins for this year'")
        print("• 'Why did expenses increase last month?'")
        print("• 'Compare Q1 and Q2 performance'")
    
    def show_history(self):
        """Show conversation history"""
        print(f"\n📜 CONVERSATION HISTORY ({len(self.conversation_history)} interactions):")
        print("-" * 60)
        
        for i, interaction in enumerate(self.conversation_history, 1):
            print(f"\n{i}. [{interaction['timestamp']}]")
            print(f"   Q: {interaction['prompt'][:100]}...")
            if interaction.get('error'):
                print(f"   A: ❌ {interaction['response']}")
            else:
                print(f"   A: ✅ {interaction['response'][:100]}...")
            print(f"   ⏱️  {interaction['response_time']:.2f}s")
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def save_session_log(self):
        """Save the session log"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"interactive_session_{timestamp}.json"
        
        session_data = {
            'session_metadata': {
                'session_id': self.SESSION_ID,
                'start_time': datetime.now().isoformat(),
                'total_prompts': len(self.conversation_history),
                'agent_name': 'cfo_agent'
            },
            'conversation_history': self.conversation_history
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(session_data, f, indent=2)
            print(f"📝 Session saved to: {filename}")
        except Exception as e:
            print(f"❌ Failed to save session: {e}")
    
    async def run_interactive_session(self):
        """Main interactive session loop"""
        # Setup
        if not await self.setup_session():
            return
        
        self.print_banner()
        
        # Interactive loop
        while self.prompt_count < self.max_prompts:
            try:
                # Get user input
                self.print_prompt_header(self.prompt_count + 1)
                
                user_input = input(f"💬 Enter your prompt (or command): ").strip()
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit']:
                    print("\n👋 Ending session...")
                    break
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                elif user_input.lower() == 'history':
                    self.show_history()
                    continue
                elif user_input.lower() == 'clear':
                    self.clear_screen()
                    self.print_banner()
                    continue
                elif not user_input:
                    print("❌ Please enter a prompt or command.")
                    continue
                
                # Process the prompt
                self.prompt_count += 1
                print(f"\n📤 Sending to CFO Agent: {user_input}")
                
                # Send to agent
                response = await self.send_message(user_input)
                
                # Ask for follow-up context if needed
                if self.prompt_count < self.max_prompts:
                    follow_up = input(f"\n🤔 Any follow-up or additional context? (press Enter to skip): ").strip()
                    if follow_up:
                        print(f"\n📤 Follow-up: {follow_up}")
                        await self.send_message(follow_up)
                
                # Show remaining prompts
                remaining = self.max_prompts - self.prompt_count
                if remaining > 0:
                    print(f"\n💡 {remaining} prompts remaining in this session.")
                
            except KeyboardInterrupt:
                print(f"\n\n⏹️  Session interrupted by user")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                break
        
        # Session summary
        print(f"\n{'='*60}")
        print("📊 SESSION SUMMARY")
        print(f"{'='*60}")
        print(f"Total prompts tested: {len(self.conversation_history)}")
        print(f"Average response time: {sum(h['response_time'] for h in self.conversation_history) / len(self.conversation_history):.2f}s" if self.conversation_history else "N/A")
        print(f"Errors encountered: {sum(1 for h in self.conversation_history if h.get('error'))}")
        
        # Save session
        if self.conversation_history:
            save_choice = input(f"\n💾 Save session log? (y/n): ").strip().lower()
            if save_choice == 'y':
                self.save_session_log()
        
        print(f"\n🎯 Session Analysis:")
        print("Now you can analyze the conversation history to evaluate:")
        print("• Response quality and accuracy")
        print("• Agent behavior and delegation patterns")
        print("• Error handling effectiveness")
        print("• User experience and clarity")

async def main():
    """Main function"""
    session = InteractiveCFOSession()
    await session.run_interactive_session()

if __name__ == "__main__":
    print("🚀 Starting Interactive CFO Agent Session...")
    
    try:
        # Check if we have the required environment
        if not os.getenv("GOOGLE_API_KEY"):
            print("❌ GOOGLE_API_KEY not found in environment variables")
            print("Please set your Google API key in the .env file")
            sys.exit(1)
        
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Failed to start session: {e}")
        import traceback
        traceback.print_exc()