from google.adk.agents import LlmAgent
from agent.subagents.financial_analyst_agent.instructions import get_analyst_instructions
from agent.subagents.financial_analyst_agent.tools import calculate_cash_burn, calculate_profit_margins
from dotenv import load_dotenv

load_dotenv()

# Create the Financial Analyst Agent
financial_analyst_agent = LlmAgent(
    name="financial_analyst_agent",
    model="gemini-2.5-pro-preview-06-05",
    description="Expert financial analyst that performs calculations and diagnostic analysis on financial data. Calculates metrics like cash burn, profit margins, growth rates, and provides insights on financial performance drivers.",
    instruction=get_analyst_instructions(),
    tools=[calculate_cash_burn, calculate_profit_margins]
)