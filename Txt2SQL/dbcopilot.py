import os
from dotenv import load_dotenv
import streamlit as st
from langchain.tools import BaseTool, Tool, tool
from langchain.callbacks.base import BaseCallbackHandler
from langchain import PromptTemplate
import pandas as pd
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain_openai import ChatOpenAI
from sqlalchemy.engine import URL

st.set_page_config(page_title="DBCopilot", page_icon="📊")
st.header('Copilot for structured databases.')

load_dotenv()

OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL")

openai_llm = ChatOpenAI(model=MODEL, api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE, temperature=0)

# Database configuration from environment variables
db_server = os.getenv('DB_SERVER')
db_name = os.getenv('DB_NAME')

# Connection string for SQL Server with Windows Authentication
conn_str = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={db_server};'
    f'DATABASE={db_name};'
    f'Trusted_Connection=yes;'
)

dburl = URL.create("mssql+pyodbc", query={"odbc_connect": conn_str})

database = SQLDatabase.from_uri(dburl)

toolkit = SQLDatabaseToolkit(db=database, llm=openai_llm)

prompt_prefix = """ 
##Instructions:
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the below tools. Only use the information returned by the below tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.
As part of your final answer, ALWAYS include an explanation of how to got to the final answer, including the SQL query you run. Include the explanation and the SQL query in the section that starts with "Explanation:".

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

If the question does not seem related to the database, just return "I don\'t know" as the answer.

##Tools:

"""

prompt_format_instructions = """ 
Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]\nAction Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question.

Explanation:

<===Beging of an Example of Explanation:

I joined the invoices and customers tables on the customerid column, which is the common key between them. This will allowed me to access the Total and Country columns from both tables. Then I grouped the records by the country column and calculate the sum of the Total column for each country, ordered them in descending order and limited the SELECT to the top 5.

```sql
SELECT top 5 c.country AS Country, SUM(i.total) AS Sales
FROM customer c
JOIN invoice i ON c.customerid = i.customerid
GROUP BY Country
ORDER BY Sales DESC;
```

===>End of an Example of Explanation
"""

agent_executor = create_sql_agent(
    prefix=prompt_prefix,
    format_instructions = prompt_format_instructions,
    llm=openai_llm,
    toolkit=toolkit,
    verbose=True,
    top_k=10
)

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query = st.chat_input(placeholder="Ask me anything!")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container())
        response = agent_executor.run(user_query, callbacks = [st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
