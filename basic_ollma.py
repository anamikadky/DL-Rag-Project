
import streamlit as st
from langchain_ollama import OllamaLLM

st.title("C++ Text Chatbot")
st.write("Ask questions about your C++ text file!")

# Load Ollama model
llm = OllamaLLM(model="gemma2:2b")

# Read C++ text file
with open("CPP.txt", "r", encoding="utf-8") as file:
    cpp_text = file.read()

# User input
question = st.text_input("Ask a question about C++")

if st.button("Get Answer"):
    if question:
        prompt = f"""
        Answer the question using the following C++ text.
        If the answer is not present, say so.

        C++ Text:
        {cpp_text}

        Question: {question}
        Answer:
        """

        with st.spinner("Gemma is thinking..."):
            response = llm.invoke(prompt)

        st.subheader("Answer")
        st.write(response)
