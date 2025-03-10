import os
import streamlit as st
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def generate_personalized_message(prompt: str) -> str:

    """
    Given the contact information and job description, 
    generate a personalized LinkedIn message addressed to the contact.
    
    This message may:
        - Request a referral for a specific position
        - Ask work-related questions
        - Introduce the user to the contact in a professional tone
    """
    user_name = st.session_state.user_profile.get("user_name")

    llm_client = ChatOpenAI(api_key= os.getenv("OPENAI_API_KEY"), model= "gpt-4o-mini", temperature= 0.7)
    
    messages = [
        {"role": "system", "content": """
         You are an assistant that drafts professional, warm, and concise LinkedIn messages.
         These messages are meant to help users reach out to potential contacts (like hiring managers or employees)
         for job referrals, opportunities, or informational chats.
         Address the message with proper professional format and information and include salutations wherever needed."""},

        {"role": "user", "content": f"{prompt}. My name is {user_name}. Please personalize the message with my name where needed."}

    ]

    response = llm_client.invoke(messages).content

    return response
    