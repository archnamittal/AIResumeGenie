import streamlit as st
from utils import get_llm, load_pdf

st.title("✉️ Cover Letter Generator")

llm = get_llm()

job_description = st.text_area("Paste Job Description")
uploaded = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if st.button("Generate Cover Letter"):

    if not job_description or not uploaded:
        st.error("Provide both job description and resume.")
        st.stop()

    resume_text = load_pdf(uploaded)

    prompt = f"""
Write a 300-450 word professional cover letter.

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

    st.download_button(
        "Download Cover Letter",
        full_response,
        "cover_letter.txt"
    )
