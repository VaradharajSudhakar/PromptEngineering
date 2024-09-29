from typing import Annotated

from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from typing_extensions import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage


#A StateGraph object defines the structure of our chatbot as a "state machine"
#defining State
class State(TypedDict):
    messages: Annotated[list, add_messages]

#Graph initalizer
graph_builder = StateGraph(State)


#Define the LLM
llm = ChatOllama(
    model="llama3.1",
    temperature=0,
    # other params...
)

#define the tool:
tool = TavilySearchResults(max_results=2)
tools = [tool]

#Binding the LLM to tools
llm_with_tools = llm.bind_tools(tools)

#define the Tool Node
tool_node = ToolNode(tools=[tool])

#define the Chatbot 
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# nodes
# nodes to represent the llm and functions our chatbot can call 

#adding the chatbot node
graph_builder.add_node("chatbot", chatbot)

#adding the tools node
graph_builder.add_node("tools", tool_node)

# edges
# edges to specify how the bot should transition between these functions.

#define the conditional edge
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

#define the edge
graph_builder.add_edge("tools", "chatbot")

#define the Entry Point
graph_builder.set_entry_point("chatbot")

#Create a MemorySaver checkpointer
memory = MemorySaver()

# Compile to run our graph.
graph = graph_builder.compile(
    checkpointer=memory,
    # This is new!
    interrupt_before=["tools"],
    # Note: can also interrupt __after__ actions, if desired.
    # interrupt_after=["tools"]
)

user_input = "I'm learning LangGraph. Could you do some research on it for me?"
config = {"configurable": {"thread_id": "1"}}
# The config is the **second positional argument** to stream() or invoke()!
events = graph.stream(
    {"messages": [("user", user_input)]}, config, stream_mode="values"
)
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()

#To check the interrupt below debug messages added
#snapshot = graph.get_state(config)
#print(snapshot.next)

#existing_message = snapshot.values["messages"][-1]
#print(existing_message.tool_calls)
#existing_message.pretty_print()


#Human interruption : Below code is to replace tool call args
snapshot = graph.get_state(config)
existing_message = snapshot.values["messages"][-1]
print("Original")
print("Message ID", existing_message.id)
print(existing_message.tool_calls[0])
new_tool_call = existing_message.tool_calls[0].copy()
new_tool_call["args"]["query"] = "LangGraph human-in-the-loop workflow"
new_message = AIMessage(
    content=existing_message.content,
    tool_calls=[new_tool_call],
    # Important! The ID is how LangGraph knows to REPLACE the message in the state rather than APPEND this messages
    id=existing_message.id,
)

print("Updated")
print(new_message.tool_calls[0])
print("Message ID", new_message.id)
graph.update_state(config, {"messages": [new_message]})

print("\n\nTool calls")
graph.get_state(config).values["messages"][-1].tool_calls

# `None` will append nothing new to the current state, letting it resume as if it had never been interrupted
events = graph.stream(None, config, stream_mode="values")
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()

#Below code is to display the state history
to_replay = None
for state in graph.get_state_history(config):
    print("Num Messages: ", len(state.values["messages"]), "Next: ", state.next)
    print("-" * 80)
    if len(state.values["messages"]) == 6:
        # We are somewhat arbitrarily selecting a specific state based on the number of chat messages in the state.
        to_replay = state
        
        