# agent_app.py
import os
import sys
import asyncio
import contextlib
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
load_dotenv()


from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPServerParams



from agent.subagents.data_retrieval_agent.data_retrieval import data_retrieval_agent
from agent.cfoAgent.instructions import cfo_instructions

#temp
from working_with_zoho_api.auth.get_access_token import get_valid_access_token
ZOHO_ORGANIZATION_ID = "60040042565"
access_token = get_valid_access_token()


GOOGLE_API_KEY = os.getenv("GOOGLE_ADK_API_KEY")
mcp_tools = MCPToolset(
    connection_params=StreamableHTTPServerParams(
        url="http://localhost:8002/mcp",  # Change this to your actual MCP server URL
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-Zoho-Organization-ID": ZOHO_ORGANIZATION_ID,
        }
    )
)

# 2️⃣ Attach MCP tools to sub-agent
data_retrieval_agent.tools = [mcp_tools]

# 3️⃣ Define root agent (CFO)
cfo_agent = LlmAgent(
    name="cfo_agent",
    model="gemini-2.5-pro-preview-06-05",
    description="Agent is the primary coordinator and the sole point of contact for the human user. Its purpose is to interpret the user's natural language request, create a multi-step execution plan, and delegate specific tasks to the appropriate specialist agents (DataRetrievalAgent, FinancialAnalystAgent, ForecastingAgent, VisualizationAgent). It does not perform any calculations, data fetching, or analysis itself. It synthesizes the results from its team into a final, coherent response for the user.",
    instruction=cfo_instructions(),
    sub_agents=[data_retrieval_agent]
)
root_agent = cfo_agent

# 4️⃣ Run the agent
# if __name__ == "__main__":
#     runner = Runner(cfo_agent)
#     result = runner.run([GenerateRequest(text="Retrieve the latest quarterly revenue for Apple Inc.")])
#     print(result)