import streamlit as st
from utils import get_llm, load_pdf

st.title("🎯 Resume vs Job Description Match")

llm = get_llm()

job_description = st.text_area("Paste Job Description")
uploaded = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if st.button("Calculate Match Score"):

    if not job_description or not uploaded:
        st.error("Provide both inputs.")
        st.stop()

    resume_text = load_pdf(uploaded)

    prompt = f"""
Analyze resume vs job description.

Provide:

Score: X/100
Overall Match: X%
Keywords matched
Missing keywords
Skill gaps
Improvement suggestions

Job Description:
{job_description}

Resume:
{resume_text}

Do not invent information.
"""

    placeholder = st.empty()
    full_response = ""

    for chunk in llm.stream(prompt):
        token = chunk.content or ""
        full_response += token
        placeholder.markdown(full_response)
