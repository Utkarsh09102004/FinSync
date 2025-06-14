#!/usr/bin/env python3
"""
Session Testing Framework for FinSync CFO Agent
Tests the agent system with comprehensive prompts and analyzes responses
"""

import asyncio
import sys
import os
import json
import time
from datetime import datetime
from typing import List, Dict, Any
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

class TestResults:
    """Container for test results and analysis"""
    def __init__(self):
        self.test_runs: List[Dict[str, Any]] = []
        self.errors: List[Dict[str, Any]] = []
        self.response_times: List[float] = []
        self.successful_runs = 0
        self.failed_runs = 0
        
    def add_result(self, prompt: str, response: str, response_time: float, 
                   error: str = None, metadata: Dict = None):
        """Add a test result"""
        result = {
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt,
            'response': response,
            'response_time': response_time,
            'error': error,
            'metadata': metadata or {}
        }
        
        self.test_runs.append(result)
        self.response_times.append(response_time)
        
        if error:
            self.failed_runs += 1
            self.errors.append(result)
        else:
            self.successful_runs += 1
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics"""
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        
        return {
            'total_tests': len(self.test_runs),
            'successful_runs': self.successful_runs,
            'failed_runs': self.failed_runs,
            'success_rate': (self.successful_runs / len(self.test_runs)) * 100 if self.test_runs else 0,
            'average_response_time': avg_response_time,
            'min_response_time': min(self.response_times) if self.response_times else 0,
            'max_response_time': max(self.response_times) if self.response_times else 0
        }

class CFOAgentTester:
    """Testing framework for the CFO Agent system"""
    
    def __init__(self):
        self.APP_NAME = "finsync_test"
        self.USER_ID = "test_user_001"
        self.SESSION_ID = "test_session_001"
        
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
        
        self.results = TestResults()
    
    async def setup_session(self):
        """Create a new test session"""
        try:
            session = await self.session_service.create_session(
                app_name=self.APP_NAME,
                user_id=self.USER_ID,
                session_id=self.SESSION_ID
            )
            print(f"✅ Session created: {session.id}")
            return session
        except Exception as e:
            print(f"❌ Failed to create session: {e}")
            return None
    
    async def send_query(self, query: str, category: str = "general") -> Dict[str, Any]:
        """Send a query to the agent and collect response"""
        print(f"\n🔍 Testing [{category.upper()}]: {query}")
        
        start_time = time.time()
        response_text = ""
        error_msg = None
        events_collected = []
        
        try:
            # Prepare the user message
            content = types.Content(role='user', parts=[types.Part(text=query)])
            
            # Run the agent and collect events
            async for event in self.runner.run_async(
                user_id=self.USER_ID,
                session_id=self.SESSION_ID,
                new_message=content
            ):
                events_collected.append({
                    'author': event.author,
                    'timestamp': event.timestamp,
                    'is_final': event.is_final_response(),
                    'content_preview': str(event.content)[:100] if event.content else None
                })
                
                # Collect final response
                if event.is_final_response():
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if part.text:
                                response_text += part.text
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error: {error_msg}")
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # Log response
        if response_text:
            print(f"✅ Response ({response_time:.2f}s): {response_text[:200]}...")
        else:
            print(f"❌ No response received")
        
        # Record result
        self.results.add_result(
            prompt=query,
            response=response_text,
            response_time=response_time,
            error=error_msg,
            metadata={
                'category': category,
                'events_count': len(events_collected),
                'events': events_collected
            }
        )
        
        return {
            'query': query,
            'response': response_text,
            'response_time': response_time,
            'error': error_msg,
            'category': category
        }
    
    def get_test_prompts(self) -> List[Dict[str, str]]:
        """Get comprehensive test prompts covering various scenarios"""
        return [
            # 1. Simple Data Retrieval
            {"query": "What was our total revenue last quarter?", "category": "simple_data"},
            {"query": "Show me the current cash balance", "category": "simple_data"},
            {"query": "Get me the profit and loss statement for Q2 2024", "category": "simple_data"},
            
            # 2. Analysis & Calculations
            {"query": "What was our cash burn rate last month?", "category": "analysis"},
            {"query": "Calculate our profit margins for this quarter", "category": "analysis"},
            {"query": "What's our gross margin compared to last year?", "category": "analysis"},
            
            # 3. Comparative Analysis
            {"query": "Compare our Q1 and Q2 revenue performance", "category": "comparison"},
            {"query": "Why did our expenses increase in March compared to February?", "category": "comparison"},
            {"query": "Show me how our cash flow has changed over the last 6 months", "category": "comparison"},
            
            # 4. Diagnostic Questions
            {"query": "Why was our profit margin lower in Q2?", "category": "diagnostic"},
            {"query": "What drove the increase in our operating expenses last quarter?", "category": "diagnostic"},
            {"query": "Explain the factors behind our cash burn spike in April", "category": "diagnostic"},
            
            # 5. Multi-step Complex Queries
            {"query": "Analyze our Q3 financial performance, calculate key metrics, and identify the main drivers of change from Q2", "category": "complex"},
            {"query": "Get our cash flow data for the last 3 months, calculate the burn rate, and explain any trends", "category": "complex"},
            {"query": "Compare our profit margins between Q1 and Q2, then explain what caused any changes", "category": "complex"},
            
            # 6. Ambiguous Queries (should ask for clarification)
            {"query": "How are we doing financially?", "category": "ambiguous"},
            {"query": "Show me our performance", "category": "ambiguous"},
            {"query": "What about our expenses?", "category": "ambiguous"},
            
            # 7. Edge Cases
            {"query": "Calculate our ROI for last year", "category": "edge_case"},
            {"query": "What will our revenue be next quarter?", "category": "edge_case"},
            {"query": "Can you help me with my taxes?", "category": "edge_case"},
            
            # 8. Date Range Variations
            {"query": "Show me revenue for the last 6 months", "category": "date_range"},
            {"query": "What was our cash position on December 31st?", "category": "date_range"},
            {"query": "Get expenses for Q4 2023", "category": "date_range"},
            
            # 9. Tool/Sub-agent Integration Tests
            {"query": "First get our P&L for Q2, then analyze our profit margins", "category": "integration"},
            {"query": "Retrieve cash flow data and calculate burn rate", "category": "integration"},
            
            # 10. Error Handling
            {"query": "Get data for Q17 2024", "category": "error_handling"},
            {"query": "Show me profits for the year 2030", "category": "error_handling"},
        ]
    
    async def run_comprehensive_test(self):
        """Run all test prompts and collect results"""
        print("🚀 Starting Comprehensive CFO Agent Testing")
        print("=" * 60)
        
        # Setup session
        session = await self.setup_session()
        if not session:
            print("❌ Failed to setup session, aborting tests")
            return
        
        # Get test prompts
        test_prompts = self.get_test_prompts()
        total_tests = len(test_prompts)
        
        print(f"📝 Running {total_tests} test scenarios...")
        
        # Run each test
        for i, test_case in enumerate(test_prompts, 1):
            print(f"\n{'='*60}")
            print(f"Test {i}/{total_tests}")
            
            await self.send_query(test_case["query"], test_case["category"])
            
            # Small delay between tests
            await asyncio.sleep(1)
        
        # Print summary
        self.print_summary()
        
        # Save detailed results
        await self.save_results()
    
    def print_summary(self):
        """Print test summary"""
        summary = self.results.get_summary()
        
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Successful: {summary['successful_runs']}")
        print(f"Failed: {summary['failed_runs']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print(f"Avg Response Time: {summary['average_response_time']:.2f}s")
        print(f"Min Response Time: {summary['min_response_time']:.2f}s")
        print(f"Max Response Time: {summary['max_response_time']:.2f}s")
        
        # Category breakdown
        categories = {}
        for result in self.results.test_runs:
            cat = result['metadata'].get('category', 'unknown')
            if cat not in categories:
                categories[cat] = {'total': 0, 'successful': 0, 'failed': 0}
            categories[cat]['total'] += 1
            if result['error']:
                categories[cat]['failed'] += 1
            else:
                categories[cat]['successful'] += 1
        
        print("\n📈 BY CATEGORY:")
        for category, stats in categories.items():
            success_rate = (stats['successful'] / stats['total']) * 100 if stats['total'] > 0 else 0
            print(f"  {category}: {stats['successful']}/{stats['total']} ({success_rate:.1f}%)")
        
        # Error summary
        if self.results.errors:
            print(f"\n❌ ERRORS ({len(self.results.errors)}):")
            for i, error in enumerate(self.results.errors[:5], 1):  # Show first 5 errors
                print(f"  {i}. {error['prompt'][:50]}... -> {error['error']}")
            if len(self.results.errors) > 5:
                print(f"  ... and {len(self.results.errors) - 5} more errors")
    
    async def save_results(self):
        """Save detailed results to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_results_{timestamp}.json"
        
        output_data = {
            'test_metadata': {
                'timestamp': datetime.now().isoformat(),
                'agent_name': 'cfo_agent',
                'total_tests': len(self.results.test_runs),
                'session_id': self.SESSION_ID
            },
            'summary': self.results.get_summary(),
            'test_results': self.results.test_runs,
            'errors': self.results.errors
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(output_data, f, indent=2)
            print(f"\n💾 Detailed results saved to: {filename}")
        except Exception as e:
            print(f"❌ Failed to save results: {e}")

async def main():
    """Main test execution"""
    tester = CFOAgentTester()
    await tester.run_comprehensive_test()

if __name__ == "__main__":
    print("CFO Agent Testing Framework")
    print("Analyzing FinSync agent system performance...\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Testing failed with error: {e}")
        import traceback
        traceback.print_exc()