
import streamlit as st
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama

# Streamlit page

st.title("College Knowledge Assistant")
st.write("Ask questions about college rules and student services.")

# Find TXT files in the same folder as this Python file
BASE_DIR = Path(__file__).resolve().parent

# Load college documents and create FAISS vector database
@st.cache_resource
def load_vectorstore():
    documents = []

    for file_path in BASE_DIR.glob("*.txt"):
        # Skip your existing C++ chatbot document
        if file_path.name.lower() == "cpp.txt":
            continue

        loader = TextLoader(str(file_path), encoding="utf-8")
        documents.extend(loader.load())

    if not documents:
        raise ValueError(
            "No college TXT files found. "
            "Place your college TXT files beside college_app.py."
        )

    # Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    # Convert text into embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create FAISS vector database
    vector_db = FAISS.from_documents(chunks, embeddings)

    return vector_db


# Load the vector database
try:
    db = load_vectorstore()
except Exception as e:
    st.error(f"Could not load college documents: {e}")
    st.stop()


# Connect to the installed Ollama model
llm = ChatOllama(
    model="gemma2:2b",
    temperature=0
)

# Ask a question
query = st.text_input("Enter your college-related question")

if query:
    # Retrieve relevant document chunks
    docs = db.similarity_search(query, k=3)

    # Prepare context and source names
    context = ""

    for doc in docs:
        source = Path(doc.metadata["source"]).name
        context += (
            f"\nSource: {source}\n"
            f"Content: {doc.page_content}\n"
        )

    # Build the RAG prompt
    prompt = f"""
You are a College Knowledge Assistant.

Answer the student's question using only the supplied documents.

Rules:
1. Do not invent college rules, fees, dates, or contact details.
2. If the answer is not available, say:
   "I could not find sufficient information in the college documents."
3. If the documents contain conflicting information, explain the conflict.
4. Do not claim that a rule is official unless the documents establish it.
5. Keep the answer clear and simple.

COLLEGE DOCUMENTS:
{context}

STUDENT QUESTION:
{query}

ANSWER:
"""

    # Generate answer
    try:
        with st.spinner("Generating answer..."):
            response = llm.invoke(prompt)

        st.subheader("Answer")
        st.write(response.content)

        # Show supporting sources
        st.subheader("Supporting Sources")

        for doc in docs:
            source = Path(doc.metadata["source"]).name

            with st.expander(f"Source: {source}"):
                st.write(doc.page_content)

    except Exception as e:
        st.error(
            f"Could not generate an answer: {e}\n\n"
            "Check that Ollama is running and the model "
            "'gemma2:2b' is installed."
        )

