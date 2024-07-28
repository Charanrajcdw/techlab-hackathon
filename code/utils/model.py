from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import AzureOpenAI
import streamlit as st
import os

os.environ["OPENAI_API_VERSION"] = st.secrets.OPENAI_API_VERSION
os.environ["AZURE_OPENAI_ENDPOINT"] = st.secrets.AZURE_OPENAI_ENDPOINT
os.environ["AZURE_OPENAI_API_KEY"] = st.secrets.AZURE_OPENAI_API_KEY

def create_agent(df):
    llm = AzureOpenAI(
        deployment_name="gpt-35-turbo-instruct",
        verbose= True,
        temperature= 0
    )
    return create_pandas_dataframe_agent(llm, df,  verbose=True, allow_dangerous_code=True)

def process_query(query, agent):
    max_attempts = 5
    while max_attempts > 0:
        response = agent.invoke(query)
        if 'output' in response:
            if(response['output'] == 'Agent stopped due to iteration limit or time limit.'):
                max_attempts -= 1
                print(f"Attempts Tried :: {max_attempts}")
            else:
                return response['output']
        else:
            print("No output found in the response")
    if max_attempts == 0:
        print(f"Agent failed for query {query}")