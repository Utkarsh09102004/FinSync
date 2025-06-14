# agent_app.py
import os
import sys
import asyncio
import contextlib
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
load_dotenv()


from google.adk.agents import LlmAgent

from google.adk.tools import agent_tool


from agent.subagents.data_retrieval_agent.data_retrieval import data_retrieval_agent
from agent.subagents.financial_analyst_agent.financial_analyst import financial_analyst_agent
from agent.cfoAgent.instructions import cfo_instructions

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")



# 3️⃣ Wrap the agents as tools
data_retrieval_tool = agent_tool.AgentTool(agent=data_retrieval_agent)


# 4️⃣ Define root agent (CFO) with the agent tools
cfo_agent = LlmAgent(
    name="cfo_agent",
    model="gemini-2.5-flash-preview-05-20",
    description="Agent is the primary coordinator and the sole point of contact for the human user. Its purpose is to interpret the user's natural language request, create a multi-step execution plan, and delegate specific tasks to the appropriate specialist agents (DataRetrievalAgent, FinancialAnalystAgent, ForecastingAgent, VisualizationAgent). It does not perform any calculations, data fetching, or analysis itself. It synthesizes the results from its team into a final, coherent response for the user.",
    instruction=cfo_instructions(),
    tools=[data_retrieval_tool],
    sub_agents=[financial_analyst_agent]
)
root_agent = cfo_agent

# 4️⃣ Run the agent
# if __name__ == "__main__":
#     runner = Runner(cfo_agent)
#     result = runner.run([GenerateRequest(text="Retrieve the latest quarterly revenue for Apple Inc.")])
#     print(result)