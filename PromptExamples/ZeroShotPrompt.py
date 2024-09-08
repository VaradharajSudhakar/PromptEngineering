# Author: Sudhakar Varadharaj
# Date: 08/04/2024
# Description: ZERO SHOT PROMPTING 
# Zero-shot prompting is when a model is asked to produce output without examples or training data.

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL")

prompt_system = "You are a helpful assistant whose goal is to write short poems."

prompt = """Write a short poem about {topic}"""

prompt_user = prompt.format(topic="Summer")

client = OpenAI(base_url=OPENAI_API_BASE, api_key=OPENAI_API_KEY)

response = client.chat.completions.create(model=MODEL, 
                                        messages=[
                                            {"role": "system", "content": prompt_system}, 
                                            {"role": "user", "content": prompt_user}])

print(response.choices[0].message.content)