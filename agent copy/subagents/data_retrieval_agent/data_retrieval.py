from google.adk.agents import LlmAgent
from agent.subagents.data_retrieval_agent.instructions import get_instructions
from dotenv import load_dotenv

load_dotenv()

data_retrieval_agent = LlmAgent(
    name="data_retrieval_agent",
    model="gemini-2.5-pro-preview-06-05",
    description="Specialist agent for securely fetching structured financial data (e.g., profit/loss, expenses) from Zoho Books via an MCP server.",
    instruction=get_instructions()
)

