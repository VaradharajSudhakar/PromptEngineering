# Author: Sudhakar Varadharaj
# Date: 08/04/2024
# Description: CHAIN PROMPTING
# Chain Prompting involves chaining multiple prompts together to create a sequence of instructions for the model.
# This sequence of prompts can guide the model's behavior and output by providing context and constraints for the task.
# Chain Prompting is a powerful technique for customizing the behavior and output of language models for complex tasks.


# In this snippet, we demonstrate how to use chain prompting to chain multiple prompts together to create a sequence of instructions for the model.
# The first prompt asks the model to provide the name of a famous scientist who developed the theory of general relativity.
# The model generates the name of the scientist.
# The second prompt asks the model to provide a brief description of the scientist's theory of general relativity.
# The model generates a fact about the scientist based on the provided name.
import os
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Load the environment variables
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL")

# Initialize the model
llm = ChatOpenAI(model_name=MODEL, api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE, temperature=0)

# Prompt 1
# Ask the model to provide the name of a famous scientist who developed the theory of general relativity
template_question = """What is the name of the famous scientist who developed the theory of general relativity?
Answer:"""

# Create a prompt template for the question
prompt_question = PromptTemplate(
    input_variables=[],
    template=template_question
)

# Prompt 2
# Ask the model to provide a brief description of the scientist's theory of general relativity
template_fact = """ Provide a brief description of scientist {scientist}'s theory of general relativity.
Answer:"""
prompt_fact = PromptTemplate(
    input_variables=["scientist"],
    template=template_fact
)


# Chain the question prompt with the language model and output parser
chain = prompt_question | llm | StrOutputParser()

# Run the chain to get the AI Generated scientist name
# The input to the chain is an empty dictionary since the question prompt does not require any input variables
response_question = chain.invoke({})

# Extract the scientist name from the response
scientist_name = response_question.strip()

# Create the chain for the fact prompt
chain = prompt_fact | llm | StrOutputParser()

# Run the chain to get the AI Generated fact about the scientist
response_fact = chain.invoke({"scientist": scientist_name})

# Print the results
print("\n Scientist Name:", scientist_name)
print("\n Fact about the Scientist:", response_fact)

# Summary:
# The chain prompting technique allows for chaining multiple prompts together to guide the model's behavior and output.
# The sequence of prompts provides context and constraints for the task, resulting in more accurate and relevant responses.
# Chain prompting is a powerful technique for customizing the behavior and output of language models for complex tasks.

# In this snippet, we demonstrate how to use chain prompting to chain multiple prompts together to create a sequence of instructions for the model.
# The first prompt asks the model to provide the name of a famous scientist who developed the theory of general relativity.
# The model generates the name of the scientist.
# The second prompt asks the model to provide a brief description of the scientist's theory of general relativity.
# The model generates a fact about the scientist based on the provided name.


