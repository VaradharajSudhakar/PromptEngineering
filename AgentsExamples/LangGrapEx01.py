# This is a simple example of how to use the LangGraph library to create a simple conversational agent
# The agent will ask the user for a question and then answer it using the OpenAI API
# The agent will continue to ask for questions until the user types 'q' to quit

import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import Annotated, TypedDict
from Graph import create_graph

load_dotenv()

# Load the environment variables
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL")

# Set the environment variables
os.environ["OPENAI_API_BASE"] = OPENAI_API_BASE
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["MODEL"] = MODEL

# Define the UserInput type
class UserInput(TypedDict):
    input: str
    continue_conversation: bool

# Define the functions for the agent states
def get_user_input(state: UserInput) -> UserInput:
    user_input = input("Enter your question ('q' to quit) : ")
    return {
            "input": user_input,
            "continue_conversation": user_input.lower() != "q"
          }

# Define the function to process the question
def process_question(state: UserInput):
    graph = create_graph()
    result = graph.invoke(
            {
                "input": state["input"]
             })
    print("\n Answer : ")
    print(result["output"].content)

    return state

# Create the conversation graph
# The conversation graph is a directed graph that represents the different states that an agent can be in during the simulation.
def create_conversation_graph():
    workflow = StateGraph(UserInput)

    workflow.add_node("get_input", get_user_input)
    workflow.add_node("process_question", process_question)
    workflow.set_entry_point("get_input")
    
    workflow.add_conditional_edges(
        "get_input",
        lambda x: "continue" if x["continue_conversation"] else "end",
        {
            "continue": "process_question",
            "end": END
        }
    )

    workflow.add_edge("process_question", "get_input")

    return workflow.compile()

# Main function to run the conversation
def main():
    conversation_graph = create_conversation_graph()
    conversation_graph.invoke({"input": "", "continue_conversation": True})

if __name__ == "__main__":
    main()


    

