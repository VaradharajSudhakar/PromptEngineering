from langgraph.graph import StateGraph, END
from typing import Annotated, TypedDict
from Agents import analyze_question, answer_code_question, answer_generic_question

# Creating the graph for the agent states
# The graph represents the different states that an agent can be in during the simulation.
# You can precise the format here which could be helpful for multimodal graphs 

class AgentState(TypedDict):
    input: str
    output: str
    decision: str

# Create the agent graph
# The agent graph is a directed graph that represents the different states that an agent can be in during the simulation.
# def create_agent_graph() -> StateGraph[AgentState]:
#     graph = StateGraph[AgentState]()

#     # Add the states to the graph
#     graph.add_state("start", {"input": "input"})
#     graph.add_state("analyze_question", {"input": "input", "decision": "decision"})
#     graph.add_state("answer_code_question", {"input": "input", "output": "output"})
#     graph.add_state("answer_generic_question", {"input": "input", "output": "output"})

#     # Add the transitions between the states
#     graph.add_transition("start", "analyze_question", analyze_question)
#     graph.add_transition("analyze_question", "answer_code_question", answer_code_question)
#     graph.add_transition("analyze_question", "answer_generic_question", answer_generic_question)
#     graph.add_transition("answer_code_question", END)
#     graph.add_transition("answer_generic_question", END)

#     return graph

# Create the agent graph
# The agent graph is a directed graph that represents the different states that an agent can be in during the simulation.
# Here is a simple 3 steps graph that is going to be working in the below "decision" condition
def create_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("analyze",analyze_question)
    workflow.add_node("dev_agent",answer_code_question)
    workflow.add_node("generic_agent",answer_generic_question)

    workflow.add_conditional_edges(
        "analyze",
        lambda x: x["decision"],
        {
            "code": "dev_agent", 
            "general": "generic_agent"
        }
    )

    workflow.set_entry_point("analyze")
    workflow.add_edge("dev_agent", END)
    workflow.add_edge("generic_agent", END)

    return workflow.compile()
