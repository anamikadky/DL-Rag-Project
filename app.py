from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

# Streamlit UI
st.title("LangChain Demo with Gemma2:2b")

# User Input
input_text = st.text_input("What question do you have in mind?")

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the question asked."),
        ("user", "Question: {question}")
    ]
)

# Ollama Model
llm = Ollama(model="gemma2:2b")

# Output Parser
output_parser = StrOutputParser()

# Chain
chain = prompt | llm | output_parser

# Generate Response
if input_text:
    response = chain.invoke({"question": input_text})
    st.write(response)