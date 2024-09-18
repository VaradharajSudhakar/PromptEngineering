# Author: Sudhakar Varadharaj
# Created: 09/07/2024
# Last Modified: 09/07/2024
# Reference : LangChain Documentation
# Description: This is a basic agent executor that uses OpenAI functions agent to execute the agent.
# Required Packages: langgraph,langchain-openai,openai,dotenv,tavily-python
import os
import operator
from openai import OpenAI
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import Annotated, TypedDict, Union
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage
from langgraph.prebuilt.tool_executor import ToolExecutor
from langgraph.graph import END, StateGraph, START
from langchain_ollama import ChatOllama

load_dotenv()

# Load the environment variables
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL")

tools = [TavilySearchResults(max_results=1)]

# Get the prompt to use from community hub
# You can modify this prompt to use your own prompt
prompt = hub.pull("hwchase17/openai-functions-agent")

ollamaModel = ChatOllama(
    model="llama3.1",
    temperature=0,
    # other params...
)
# Choose the LLM that will will drive the agent
llm = ChatOpenAI(model=MODEL, api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE, temperature=0)

# Construct the OpenAI functions agent
#agent = create_openai_functions_agent(llm, tools, prompt)
agent = create_openai_functions_agent(ollamaModel, tools, prompt)

# Define Graph State
# This is the state of the graph that will be passed to the agent
# This is a dictionary that can be modified to store any information
# LangChain agent has a few attributes:
# - input: The input message that the agent receives from the user
# - chat_history: The chat history of the agent and previous conversation messages passed to the agent
# - intermediate_results: The intermediate results of the agent. This is list of actions and corresponding observations 
#   that the agents has taken and observed. This is useful for debugging and understanding the agent's behavior.
# - agent_outcome: The outcome of the agent. This is the action that the agent has taken. This can be an AgentAction or AgentFinish
# - intermediate_steps: The intermediate steps of the agent. This is a list of tuples where the first element is the action taken by the agent
#   and the second element is the observation made by the agent. This is useful for debugging and understanding the agent's behavior.

class AgentState(TypedDict):
    input: str
    chat_history: list[BaseMessage]
    agent_outcome: Union[AgentAction,AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]],operator.add]


# Create the agent executor
# It takes a list of tools and executes them
# The tool executor is a stateful object that can be used to execute tools
# The tool executor can be used to execute tools in a stateful manner
tool_executor = ToolExecutor(tools)

# Define the agent
def run_agent(data):
    agent_outcome = agent.invoke(data)
    print("agent outcome :",agent_outcome)
    return {"agent_outcome": agent_outcome}

# Define the function to execute the tools 
def execute_tools(data):
    # Get the most recent agent outcome. This is the key added in the agent above
    agent_action = data["agent_outcome"]
    output = tool_executor.invoke(agent_action)
    print("tool calling output :",output)
    return {"intermediate_steps": [(agent_action, str(output))]}

# Defind Logic that will be used to determin which conditional edge to go down
# If the agent outcome is an AgentFinish, then the agent execution should end
# Otherwise, the agent should continue
def should_continue(data):
    if isinstance(data["agent_outcome"], AgentFinish):
        return "end"
    else:
        return "continue"


# This is a state graph that defines the agent execution workflow
workflow = StateGraph(AgentState)

# Define the two nodes we will cycle between
workflow.add_node("agent", run_agent)
workflow.add_node("action", execute_tools)

# Set the entrypoint as 'agent'
# This is the node that the workflow will start first
workflow.add_edge(START, "agent")

# We now add a conditional edge that will determine which node to go to next
workflow.add_conditional_edges(
        # First, we use 'agent' as the start node. This means these are the edges 
        # that will be checked after the 'agent' node is executed
        "agent", 
        # Next, we define the condition that will be checked 
        should_continue,
        {
            "continue": "action",
            "end": END
        },
        )

# Define the final workflow
workflow.add_edge("action", "agent")

# Compile the workflow. This will create a function that can be used to execute the workflow
app = workflow.compile()

# Define the input data
data = {"input": "I am Sudhakar Varadharaj , Living in Dalton Georgia. What is the weather in my city?","chat_history": []}

# Execute the workflow

for s in app.stream(data):
    print(list(s.values())[0])
    print("\n\n")
    print("=====================================")