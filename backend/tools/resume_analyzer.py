import streamlit as st
from PyPDF2 import PdfReader
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

def extract_resume_text(uploaded_file) -> str:

    resume_text = ""

    if uploaded_file.name.endswith(".pdf"):
       
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            extracted_text = page.extract_text()
            resume_text += extracted_text
        return resume_text

@tool
def analyze_resume(prompt: str) -> str:
    """
    Given the full resume text and a user prompt, this tool:
        - Provides formatted feedback on strengths and skill gaps
        - Gives an ATS-friendliness rating (1-10) with justification
        - Offers actionable suggestions for improvement
        - If the user mentions a target role or job title in the prompt, 
        the tool compares the resume against that target and suggests alignment strategies and give a job match % (e.g., missing keywords, domain relevance, phrasing).
    """

    resume_text = st.session_state.get("user_profile", {}).get("user_resume")

    if resume_text:

        llm_client = ChatOpenAI(api_key = st.session_state.openai_api_key, model = "gpt-4o-mini", temperature = 0.7)

        resume_analysis_prompt = [
            {
                "role": "system", 
                "content": f"""
                Given Resume Text: \n
                {resume_text} \n\n

                - Provide formatted feedback on strengths and highlight skill gaps if any.
                - Give an ATS-friendliness rating between  (1-10) with justification.
                - Offer actionable suggestions for improvements.
                If the user specifies targeted job role, you must compare the current resume against the target role, 
                tell the current strenghts in context to the current role from the resume, 
                specify gaps (if an and alignment strategies. 
                Also give a job match score before and how would it improve after making these changes -justify."""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        riseup_resume_analysis = llm_client.invoke(resume_analysis_prompt).content
        
        return riseup_resume_analysis
      
    else:
      return "⚠️ No resume found. Please upload your resume before requesting analysis."
      