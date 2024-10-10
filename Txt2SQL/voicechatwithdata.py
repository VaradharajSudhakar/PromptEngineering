import os
import time
import pygame
import pyaudio
import pyodbc
from gtts import gTTS
import streamlit as userinterface
from langchain_openai.chat_models import ChatOpenAI
from dotenv import load_dotenv
import speech_recognition as sr 
import streamlit as userinterface
from langchain_community.agent_toolkits.sql.base import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.callbacks import StreamlitCallbackHandler
from models.LLMConnection import select_llm
from config.dbconfig import get_sqldatabase
from prompts.prompthub import get_prompt_template,pull_prompt

openaillm = select_llm("openai")
database = get_sqldatabase()

sqltoolkit = SQLDatabaseToolkit(db=database, llm=openaillm)

sql_prompt_prefix = get_prompt_template("SQL_GENERAL_PREFIX")
sql_prompt_instruction = get_prompt_template("SQL_GENERAL_INSTRUCTION")

prompt_prefix = pull_prompt("SQL_GENERAL_PREFIX")
prompt_instruction = pull_prompt("SQL_GENERAL_INSTRUCTION")

sqlagent = create_sql_agent(
    prefix=prompt_prefix,
    format_instructions=prompt_instruction,
    toolkit=sqltoolkit,
    llm=openaillm,
    verbose=True,
    top_k=10
)

def text_to_speech(text):
        tts = gTTS(text, lang='en')
        tts.save("voicedata\startup.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("voicedata\startup.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.mixer.quit()

def speech_to_text(self):
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        print("Initialize...")
        recognizer.adjust_for_ambient_noise(mic, duration=10)
        userinterface.chat_message("Assistant").write("Listening now...")
        audio = recognizer.listen(mic)
        try:
            self.text = recognizer.recognize_google(audio)
            print("You said: ", self.text)
            return self.text
        except:
            userinterface.chat_message("Assistant").write("I am sorry, I did not get that. Can you please repeat?")
            return "Find the list of top 10 customers who have made the most purchases in the last 6 months"


userinterface.set_page_config(page_title="Database Intelligence")
userinterface.header('Database Intelligence')

start_message = "Hello, I am your database assistant.? Please ask me anything about the data. I am here to assist you."

if "messages" not in userinterface.session_state or userinterface.sidebar.button("Clear message history"):
    userinterface.session_state["messages"] = [{"role": "sqlassistant", "content": start_message}]

for msg in userinterface.session_state.messages:
    userinterface.chat_message(msg["role"]).write(msg["content"])


text_to_speech(start_message)

userinterface.chat_message("Assistant").write("Initializing...")

user_query = speech_to_text(userinterface)

if user_query:
     userinterface.session_state.messages.append({"role": "user", "content": user_query})
     userinterface.chat_message("user").write(user_query)

     with userinterface.chat_message("sqlassistant"):
         st_cb = StreamlitCallbackHandler(userinterface.container())
         response = sqlagent.run(user_query, callbacks = [st_cb])
         userinterface.session_state.messages.append({"role": "sqlassistant", "content": response})
         userinterface.write(response)

