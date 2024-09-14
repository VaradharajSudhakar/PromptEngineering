import openai
import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.prompts import PromptTemplate

# Set your OpenAI API key
load_dotenv()

# Load the environment variables
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL")

# Initialize LangChain's OpenAI agent
llm = OpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY)

# Define prompt templates for each agent
development_prompt = PromptTemplate(
    input_variables=["task"],
    template="You are a developer. Write code for the following task: {task}."
)

testing_prompt = PromptTemplate(
    input_variables=["code"],
    template="You are a tester. Test the following code and provide test results: {code}."
)

code_review_prompt = PromptTemplate(
    input_variables=["code"],
    template="You are a code reviewer. Review the following code for issues and improvements: {code}."
)

deployment_prompt = PromptTemplate(
    input_variables=["code"],
    template="You are a deployment engineer. Deploy the following code and provide deployment instructions: {code}."
)

# Define the agents' tasks
def develop_code(task):
    prompt = development_prompt.format(task=task)
    return llm(prompt)

def test_code(code):
    prompt = testing_prompt.format(code=code)
    return llm(prompt)

def review_code(code):
    prompt = code_review_prompt.format(code=code)
    return llm(prompt)

def deploy_code(code):
    prompt = deployment_prompt.format(code=code)
    return llm(prompt)

# Initialize the agents using LangChain's tools
tools = [
    Tool(name="DevelopmentAgent", func=develop_code, description="Writes code for a given task."),
    Tool(name="TestingAgent", func=test_code, description="Tests the provided code."),
    Tool(name="CodeReviewAgent", func=review_code, description="Reviews the provided code."),
    Tool(name="DeploymentAgent", func=deploy_code, description="Deploys the provided code.")
]

# Initialize the environment where the agents can collaborate
agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description")

# Define a task and run the workflow
task_input = "Given a claim loaded in the system, the system should be able to run business rules and return a decision."
print("Task:", task_input)

# Development stage
code_output = agent.run(f"DevelopmentAgent: Write code for {task_input}")
print("\nCode developed:\n", code_output)

# Testing stage
test_output = agent.run(f"TestingAgent: Test the following code: {code_output}")
print("\nTest results:\n", test_output)

# Code review stage
review_output = agent.run(f"CodeReviewAgent: Review the following code: {code_output}")
print("\nCode review:\n", review_output)

# Deployment stage
deploy_output = agent.run(f"DeploymentAgent: Deploy the following code: {code_output}")
print("\nDeployment instructions:\n", deploy_output)
