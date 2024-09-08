# Author: Sudhakar Varadharaj
# Date: 08/04/2024
# Description: CHAIN OF THOUGHT PROMPTING
# Chain of Thought Prompting involves chaining multiple prompts together to create a sequence of instructions for the model.
# This sequence of prompts can guide the model's behavior and output by providing context and constraints for the task.

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
