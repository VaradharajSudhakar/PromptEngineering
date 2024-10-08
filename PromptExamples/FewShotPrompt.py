# Author: Sudhakar Varadharaj
# Date: 08/04/2024
# Description: ZERO SHOT PROMPTING 
# Few-shot prompting is a technique used to fine-tune a language model by providing a small number of examples or prompts.
# This allows the model to learn new tasks or concepts quickly and efficiently.
# Few-shot prompting can be used to improve the performance of a language model on specific tasks or domains.
# It can also help the model generate more accurate and relevant outputs by providing context and constraints.
# Few-shot prompting is a powerful tool for customizing and adapting language models to suit different applications and use cases.
# Few-shot prompting can be combined with other techniques such as zero-shot prompting and chain prompting to create more complex and sophisticated interactions with language models.
# Few-shot prompting is a versatile and flexible approach that can be applied to a wide range of natural language processing tasks and challenges.  

# Few Shot Prompt Example:
# In this example, we will use a few-shot prompt to guide the model in generating the emotion associated with a given color.
# We will provide several examples of colors and emotions to help the model learn the relationship between them.
# The model will then use this information to generate the emotion associated with a new color that was not included in the examples.
# The few-shot prompt will provide clear instructions and examples to guide the model in generating the desired output.

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

# Define the prompt system example
prompt_system = "You are an AI assistant that can identify emotions associated with colors."

examples = [
    {"color": "red", "emotion": "passion"},
    {"color": "blue", "emotion": "calm"},
    {"color": "green", "emotion": "nature"},
    {"color": "yellow", "emotion": "happiness"}
]


# Define the template
example_format_template = """
Color: {color}
Emotion: {emotion}\n
"""

example_prompt = PromptTemplate(
    input_variables=["color", "emotion"],
    template=example_format_template
)

# Define the few-shot prompt
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="""Here are some examples of colors and emotions:\n""",
    suffix="""\n\n Now, given the new color , identify the emotion associated with in:\n Color:{input}\n Emotion:""",
    input_variables=["input"],
    example_separator="\n"
)


# Define the input for the few-shot prompt
formatted_prompt = few_shot_prompt.format(input="purple")
few_shot_prompt = prompt=PromptTemplate(template=formatted_prompt, input_variables=[])

# Create the LLMChain for the prompt
chain =  few_shot_prompt | llm | StrOutputParser()

# Run the chain to get the AI Generated emotion associated with the input color 
response = chain.invoke({})

print("\nFew Shot Prompt Example:")
print("     Color   : purple")
print("     Emotion : ", response)


# Summary: 
# This prompt provides clear instructions and several examples to guide the model in generating the desired output.
# The model is trained to understand the relationship between colors and emotions based on the provided examples.

# Limitations:
# The model's performance may vary based on the quality and diversity of the examples provided.
# The model may struggle with complex or abstract relationships between colors and emotions.
# The model may generate unexpected or incorrect outputs if the examples do not cover all possible scenarios.
# The model may not always provide accurate or reliable outputs, and human oversight or validation may be necessary.
# The model may not fully capture the nuances or complexities of human emotions and color associations.






