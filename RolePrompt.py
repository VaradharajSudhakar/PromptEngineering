# Author: Sudhakar Varadharaj
# Contributor: Vishal Sudhakar
# Date: 08/04/2024
# Description: ROLE PROMPTING
# Role Prompting involves instructing the model to assume a specific role or identity for task execution. 
# This instruction can influence the model's behavior and output. The role prompting can be used to guide the model


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

template = """
As a futuristic robot band conductor, I need you to help me come up with a song title. 
What's a cool song title for a song about {theme} in the year {year}?"""

role_prompt = PromptTemplate(
    input_variables=["theme", "year"],
    template=template
)

# input for the role prompt
input_data = {
    "theme": "space exploration",
    "year": "2050"
}

# create LLMChain for the role prompt
chain =  role_prompt | llm | StrOutputParser()

# Run the chain to get the AI Generated song title
response = chain.invoke(input_data)

print("\nRole Prompt Example:")
print("     Theme: space exploration")
print("     Year: 2050")
print("     AI Generated Song Title: \n ", response)


# Summary:

# In this snippet, we demonstrate how to use role prompting to instruct the model to assume a specific role or identity for task execution.
# The role prompt instructs the model to generate a song title for a song about space exploration in the year 2050.
# The model generates an AI-generated song title based on the input theme and year.

# Role prompting is a powerful technique for customizing the behavior and output of language models for specific tasks.

# Precise Direction: Role prompting provides precise direction to the model by instructing it to assume a specific role or identity for task execution.
# Specific Output: Role prompting guides the model to generate specific outputs based on the defined role or identity, leading to more relevant and accurate results.
# Customization: Role prompting allows users to customize the model's behavior and output by providing role-specific instructions and constraints.
# Enhanced Performance: Role prompting enhances the performance of language models by guiding them to generate outputs that align with the specified role or identity.
# Improved Usability: Role prompting improves the usability of language models by enabling users to interact with the model in a more intuitive and personalized way.
# Promoting Creativity: Role prompting promotes creativity by encouraging the model to generate outputs that are tailored to the defined role or identity.



