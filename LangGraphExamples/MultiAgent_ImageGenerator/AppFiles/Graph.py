from langchain.agents import tool
from langgraph.graph import StateGraph, START, END
from ToolNode import *
from AgentNodes import *
from State import *
from EdgeLogic import *
from IPython.display import Image, display

workflow = StateGraph(AgentState)

workflow.add_node("Researcher", research_node) #only call tavily  
workflow.add_node("Image_Generator", Image_node) #only image generator not passing value
workflow.add_node("call_tool", tool_node)

workflow.add_conditional_edges(
    "Researcher",
    router,
    {"continue": "Researcher", "call_tool": "call_tool", END: END},
)
workflow.add_conditional_edges(
    "Image_Generator",
    router,
    {"continue": "Researcher", "call_tool": "call_tool", END: END},
)

workflow.add_conditional_edges(
    "call_tool",
    # Each agent node updates the 'sender' field
    # the tool calling node does not, meaning
    # this edge will route back to the original agent
    # who invoked the tool
    lambda x: x["sender"],
    {
        "Researcher": "Researcher",
        "Image_Generator": "Image_Generator",
    },
)
workflow.add_edge(START, "Researcher")
graph = workflow.compile()



