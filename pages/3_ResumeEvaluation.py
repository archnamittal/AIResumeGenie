import streamlit as st
from utils import get_llm, load_pdf

st.title("📄 Resume Evaluation")

llm = get_llm()

uploaded = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if st.button("Evaluate Resume"):

    if not uploaded:
        st.error("Upload a resume.")
        st.stop()

    resume_text = load_pdf(uploaded)

    prompt = f"""
Evaluate this resume and provide:

1. Score out of 100
2. Strengths
3. Weaknesses
4. Skills Mentioned
5. Recommended Skills
6. Next Career Path

Resume:
{resume_text}
"""

    placeholder = st.empty()
    full_response = ""

    for chunk in llm.stream(prompt):
        token = chunk.content or ""
        full_response += token
        placeholder.markdown(full_response)
