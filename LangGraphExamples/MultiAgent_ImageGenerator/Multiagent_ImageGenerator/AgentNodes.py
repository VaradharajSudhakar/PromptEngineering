import functools

from langchain_core.messages import AIMessage
from langchain_ollama import ChatOllama
from Tools import *
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    ToolMessage,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langgraph.graph import END, StateGraph, START
from Prompts import *
from log import log_debug
from langchain.tools.render import render_text_description

from langchain_core.prompts import ChatPromptTemplate

rendered_tools = render_text_description([Image_Generator])
rendered_tools


def create_agent(llm, tools, system_message: str):
    """Create an agent."""
    log_debug(f'Creating the agent for {tools}')
    log_debug(f'You have access to the following tools: {tools}.{system_message}')
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                " You are a helpful AI assistant, collaborating with other assistants."
                " Use the provided tools to progress towards answering the question."
                " If you are unable to fully answer, that's OK, another assistant with different tools "
                " will help where you left off. Execute what you can to make progress."
                " you can use the tools for preparing the image description and quotes,"
                " Image description should contains the clear details of how the image should be with crisp and clear words along with some quotes in english,"
                " pass the prepared the Image description for the image as 'desc' to the Image_Generator in tool_calls,"
                " Image_Generator tool to be called to prepare the image and description as to be passed as args ,"
                " If you or any of the other assistants have the final answer or deliverable,"
                " prefix your response with FINAL ANSWER so the team knows to stop,"
                " You have access to the following tools: {tool_names}.\n{system_message}",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    prompt = prompt.partial(system_message=system_message)
    prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
    return prompt | llm.bind_tools(tools)


llm = ChatOllama(
    model="llama3-groq-tool-use",
    temperature=0,
    # other params...
)

# Helper function to create a node for a given agent
# def agent_node(state, agent, name):
#     result = agent.invoke(state)
#     # We convert the agent output into a format that is suitable to append to the global state
#     # If result is a ToolMessage, set the sender to 'call_tool'
#     # We convert the agent output into a format that is suitable to append to the global state
#     if isinstance(result, ToolMessage):
#         result = AIMessage(**result.model_dump(exclude={"type", "name"}), name=name)
#         # log_debug('ToolMessage')
#         # log_debug(f'result: {result}')
#         return {
            
#             "messages": [result],
#             "sender": "call_tool",
#         }
#     else:
#         # log_debug('NotToolMessage')
#         # log_debug(f'result: {result}')
#         result = AIMessage(**result.dict(exclude={"type", "name"}), name=name)
#         return {
#             "messages": [result],
#             "sender": name,
#         }
    

def agent_node(state, agent, name):
    result = agent.invoke(state)
    # We convert the agent output into a format that is suitable to append to the global state
    if isinstance(result, ToolMessage):
        pass
    else:
        result = AIMessage(**result.dict(exclude={"type", "name"}), name=name)
    return {
        "messages": [result],
        # Since we have a strict workflow, we can
        # track the sender so we know who to pass to next.
        "sender": name,
    }



# Research agent and node
research_agent = create_agent(
    llm,
    [tavily_tool],
    system_message="You should provide accurate description for the Image_Generator to use.",
    
)
research_node = functools.partial(agent_node, agent=research_agent, name="Researcher")

# Image_generator
Image_agent = create_agent(
    llm,
    [Image_Generator],
      system_message="You should provide accurate description for the Image_Generator to use.",
)
Image_node = functools.partial(agent_node, agent=Image_agent, name="Image_Generator")

