# Author: Sudhakar Varadharaj
# Created: 09/22/2024
# Last Modified: 09/22/2024
# Description: Expert Trip Planner Crew for personalized travel itinerary planning.
# Dependencies: CrewAI, DuckDuckGoSearchRun, ChatOpenAI, ChatOllama
# References: crewai documentation (https://crewai.readthedocs.io/) and github copilot suggestions
import sys
import os
import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from textwrap import dedent

OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL")

load_dotenv()

openai_llm = ChatOpenAI(model=MODEL, api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE, temperature=0)
ollama_llm = ChatOllama(model="llama3.1",temperature=0,)

# Model Selection 
llm = openai_llm

duckduckgo_search = DuckDuckGoSearchRun()

destination = "New York"

# Agent for personalized travel itinerary planning
# Function to create a travel crew
#def create_travel_crew(destination):
  
travel_advisor = Agent(
    role="Travel Advisor",  # Changed from Expert Travel Agent
    goal=f"Craft a personalized itinerary for a trip based on your preferences.",
    backstory="A seasoned globetrotter, passionate about creating unforgettable travel experiences!",
    verbose=True,
    allow_delegation=True,
    tools=[duckduckgo_search],
    LLM=llm
  )

# New agent for City Explorer and Activity Scout

city_explorer = Agent(  # New agent - City Explorer
    role="City Explorer",  # New role
    goal=f"Explore potential destinations and suggest exciting cities based on your interests.",
    backstory="An expert in uncovering hidden travel gems, ready to find the perfect city for your trip!",
    verbose=True,
    allow_delegation=True,
    tools=[duckduckgo_search],
    LLM=llm
  )

# New agent for Activity Scout
activity_scout = Agent(
    role="Activity Scout",
    goal=f"Find exciting activities and attractions in {destination} that match your interests.",
    backstory="An expert curator of unique experiences, ready to unveil the hidden gems of {destination}.",
    verbose=True,
    allow_delegation=True,
    tools=[duckduckgo_search],
    LLM=llm
  )

# New agent for Logistics Coordinator
logistics_coordinator = Agent(
    role="Logistics Coordinator",
    goal=f"Help you navigate the logistics of your trip to {destination}, including flights, accommodation, and transportation.",
    backstory="A logistical whiz, ensuring your trip runs smoothly from start to finish.",
    verbose=True,
    allow_delegation=True,
    tools=[duckduckgo_search],
    LLM=llm
  )

  # Define Tasks (modified based on new agent)
  # Task 1 can use either travel_advisor or city_explorer depending on user input
if destination:
    task1 = Task(
        description=f"Plan a personalized itinerary for a trip to {destination}. Consider preferences like travel style (adventure, relaxation, etc.), budget, and desired activities.",
        expected_output="Personalized itinerary for a trip to {destination}.",
        agent=travel_advisor,
        LLM=llm
      )
else:
    task1 = Task(
        description=f"Help you explore potential destinations and suggest exciting cities to visit based on your interests (e.g., beaches, culture, nightlife).",
        expected_output="List of recommended destinations and interesting cities to visit.",
        agent=city_explorer,
        LLM=llm
      )

task2 = Task(
    description=f"Find exciting activities and attractions in {destination} that align with your preferences (e.g., museums, hiking, nightlife).",
    expected_output="List of recommended activities and attractions in {destination}.",
    agent=activity_scout,
    LLM=llm
  )

task3 = Task(
    description=f"Help you navigate the logistics of your trip to {destination}. Search for flights, accommodation options, and local transportation based on your preferences and itinerary.",
    expected_output="Recommendations for flights, accommodation, and transportation for your trip to {destination}.",
    agent=logistics_coordinator,
    LLM=llm
  )

# Create and Run the Crew
travel_crew = Crew(
    agents=[travel_advisor, city_explorer, activity_scout, logistics_coordinator],
    tasks=[task1, task2, task3],
    verbose=True,
    process=Process.sequential,
    LLM=llm
  )

tripPlanResults = travel_crew.kickoff()
print("\n\n########################")
print("## Here is you Trip Plan")
print("########################\n")
print(tripPlanResults)