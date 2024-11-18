from typing import Annotated

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
import requests
import io
from PIL import Image
from langchain.tools.render import render_text_description


API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
headers = {"Authorization": } # Please add the autorization key , which you can generate from hugging face for the black-forest-labs LLM

tavily_tool = TavilySearchResults(max_results=2)



@tool
def Image_Generator(
    desc: str,
):
    """Use this to generate image. If you want to see the output of a image,
    you should print it out with `print(...)`. This is visible to the user.

    Args:
        desc:(string) description
    """
    try:
        print('image prompt : ',desc)
        response = requests.post(API_URL, headers=headers, json=desc)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        return f"Failed to execute. Error: {repr(e)}"
    imageBinaryBytes = response.content
    print('imageBinaryBytes : ',imageBinaryBytes)
    imageStream = io.BytesIO(imageBinaryBytes)
    imageFile = Image.open(imageStream)
    imageFile.save('C:/Viknesh/MyProjects/GenAI/myphoto.jpg', 'JPEG')
    return (
        "\n\nIf you have completed all tasks, respond with FINAL ANSWER."
    )

# rendered_tools = render_text_description([Image_Generator,tavily_tool])
# rendered_tools 
# print(rendered_tools)
# print(Image_Generator.name)
# print(Image_Generator.description)
# print(Image_Generator.args)

# Image_Generator.invoke({"desc": "diwali wishes image"})
