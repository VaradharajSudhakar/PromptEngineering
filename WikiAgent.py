import os
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Load the environment variables
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL")

llm = OpenAI(temperature=0,model_name=MODEL,api_key=OPENAI_API_KEY)

tools = load_tools(['wikipedia'],llm=llm)

agent = initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=True)

agent.run("What year was the founder of SpaceX born and Tesla born and what is the nameof the first company he founded?") 
