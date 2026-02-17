import streamlit as st
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from utils import get_llm, load_pdf

st.title("🤖 AI Career Coach")

llm = get_llm()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded:
    resume_text = load_pdf(uploaded)

    system_message = SystemMessage(
        content=f"""
You are a professional career coach.

Resume:
{resume_text[:4000]}
"""
    )

    for msg in st.session_state.chat_history:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        st.chat_message(role).write(msg.content)

    user_input = st.chat_input("Ask about your resume...")

    if user_input:
        st.session_state.chat_history.append(HumanMessage(content=user_input))
        messages = [system_message] + st.session_state.chat_history

        placeholder = st.empty()
        full_response = ""

        for chunk in llm.stream(messages):
            token = chunk.content or ""
            full_response += token
            placeholder.markdown(full_response)

        st.session_state.chat_history.append(AIMessage(content=full_response))
else:
    st.info("Upload a resume to begin.")
