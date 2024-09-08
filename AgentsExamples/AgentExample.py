# Import relevant functionality
from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_openai import ChatOpenAI
import getpass
import os
from openai import OpenAI
from dotenv import load_dotenv
from langchain.agents import tool

# Custom tools
# @tool
# def get_word_length(word: str) -> int:
#     """Returns the length of a word."""
#     return len(word)


load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Create 
memory = MemorySaver()


# Getting the Env value
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL")

# Point to the local server
model = ChatOpenAI(base_url=OPENAI_API_BASE, api_key=OPENAI_API_KEY)

# Setting up the Tavily
tavilySearchAPIWrapper = TavilySearchAPIWrapper(tavily_api_key=TAVILY_API_KEY)
search = TavilySearchResults(api_wrapper=tavilySearchAPIWrapper)

# conf the tools
tools = [search]
agent_executor = create_react_agent(model, tools, checkpointer=memory)


# # Use the agent
config = {"configurable": {"thread_id": "abc123"}}
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im Viknesh! and i live in TN")]}, config
):
    print(chunk)
    print("----")

for chunk in agent_executor.stream(
   {"messages": [HumanMessage(content="whats the weather where I live?")]}, config
):
   print(chunk)
   print("----")

for chunk in agent_executor.stream(
   {"messages": [HumanMessage(content="whats is todays news where I live?")]}, config
):
   print(chunk)
   print("----")