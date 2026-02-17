import os
import tempfile
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader


MODEL = "groq/compound"
TEMPERATURE = 0.7


def get_llm():
    if "GROQ_API_KEY" not in st.secrets:
        st.error("Missing GROQ_API_KEY in secrets.toml")
        st.stop()

    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

    return ChatGroq(
        model=MODEL,
        temperature=TEMPERATURE
    )


def load_pdf(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.read())
        tmp_path = tmp.name

    loader = PyPDFLoader(tmp_path)
    docs = loader.load()

    return "\n\n".join(doc.page_content for doc in docs)
