import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

prompt_system = "You are a helpful assistant whose goal is to help write stories."
prompt = """Continue the following story. Write no more than 50 words. \n\nOnce upon a time, there was a small village at the edge of a forest. The villagers were peaceful and lived in harmony with nature. One day, a mysterious stranger arrived in the village. He was tall, with a long beard and a cloak that covered his face. The villagers were curious about him and wanted to know more about him. The stranger said he was a wizard and had come to help the village. The villagers were skeptical at first, but the stranger proved his magic by conjuring a rainbow in the sky. The villagers were amazed and welcomed the wizard with open arms. The wizard stayed in the village and helped the villagers with his magic. The village prospered and became known far and wide for its beauty and magic. The villagers were grateful to the wizard and considered him a hero. The wizard lived in the village for many years, and the villagers lived happily ever after."""


client = OpenAI(base_url=OPENAI_API_BASE, api_key=OPENAI_API_KEY)

response = client.chat.completions.create(model="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF", 
                                        messages=[
                                            {"role": "system", "content": prompt_system}, 
                                            {"role": "user", "content": prompt}])

print(response.choices[0].message.content)