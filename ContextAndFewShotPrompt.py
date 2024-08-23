# Author: Sudhakar Varadharaj
# Date: 08/04/2024
# Description: CHAIN PROMPTING
# Context and Few-Shot Prompting


import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL")

prompt_system = "You are a helpful assistant whose goal is to write short poems."

prompt = """Write a short poem about {topic}"""

examples = {
    "Winter": "The snow falls gently, covering the ground in a blanket of white. The air is crisp and cold, but the fire is warm and inviting. The world is quiet and still, a peaceful winter wonderland.",
    "Spring": "The flowers bloom, the birds sing, and the sun shines bright. The world is alive with color and life, a beautiful spring day. The air is fresh and sweet, the grass is green, and the trees are in bloom.",
    "Fall": "The leaves change color, the air is cool and crisp, and the days grow shorter. The world is painted in shades of red, orange, and yellow, a beautiful autumn landscape. The harvest is in, the pumpkins are ripe, and the apples are ready to pick."
}

prompt_user_example01 = prompt.format(topic="Winter")
prompt_user_example02 = prompt.format(topic="Spring")
prompt_user_example03 = prompt.format(topic="Fall")

prompt_user_request = prompt.format(topic="Summer")

client = OpenAI(base_url=OPENAI_API_BASE, api_key=OPENAI_API_KEY)

response = client.chat.completions.create(model=MODEL, 
                                        messages=[
                                            {"role": "system", "content": prompt_system}, 

                                            {"role": "user", "content": prompt_user_example01},
                                            {"role": "assistant", "content": examples["Winter"]},

                                            {"role": "user", "content": prompt_user_example02},
                                            {"role": "assistant", "content": examples["Spring"]},

                                            {"role": "user", "content": prompt_user_example03},
                                            {"role": "assistant", "content": examples["Fall"]},

                                            {"role": "user", "content": prompt_user_request}
                                            ])

print(response.choices[0].message.content)