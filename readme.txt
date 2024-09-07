Graphs
LangGraph models agent workflows as graphs. You define the behavior of your agents using three key components 

State:  A shared data structure that represents the current snapshot of your application. It can be any Python type, 
        but is typically a TypedDict or Pydantic BaseModel

Nodes:  Python functions that encode the logic of your agents. They receive the current State as input, perform some 
        computation or side-effect, and return an updated State.

Edges:  Python functions that determine which Node to execute next based on the current State. They can be conditional
        branches or fixed transitions. 

By composing Nodes and Edges, you can create complex, looping workflows that evolve the State overtime. 
The real power, though, comes from how LangGraph manages that State. To emphasize: Nodes and Edges are nothing more than 
Python functions - they can contain an LLM or just good Python code. 

**************************************************************************
Tavily is a search engine, specifically designed for AI agents and tailored for RAG purposes. 
Through the Tavily Search API, AI developers can effortlessly integrate theri applications with realtime online information.
For more details about Tavily
https://docs.tavily.com/docs/welcome
https://docs.tavily.com/docs/python-sdk/tavily-search/getting-started

**************************************************************************

LangChain Hub
https://smith.langchain.com/hub

**************************************************************************

