from google.adk.agents import LlmAgent
from agent.subagents.data_retrieval_agent.instructions import get_instructions
from dotenv import load_dotenv
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPServerParams
import os

#temp
from working_with_zoho_api.auth.get_access_token import get_valid_access_token
ZOHO_ORGANIZATION_ID = "60040042565"
access_token = get_valid_access_token()


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


mcp_tools = MCPToolset(
    connection_params=StreamableHTTPServerParams(
        url="http://localhost:8002/mcp",  
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-Zoho-Organization-ID": ZOHO_ORGANIZATION_ID,
        }
    )
)

data_retrieval_agent = LlmAgent(
    name="data_retrieval_agent",
    model="gemini-2.5-pro-preview-06-05",
    description="Specialist agent for securely fetching structured financial data (e.g., profit/loss, expenses) and return it in a structured format",
    instruction=get_instructions(),
    tools=[mcp_tools]
)

