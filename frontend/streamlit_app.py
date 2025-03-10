import os
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
from backend.agent import get_agent
from langchain_openai import ChatOpenAI
from backend.tools.resume_analyzer import extract_resume_text


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="RiseUP AI", page_icon= "🚀", initial_sidebar_state= "auto")

### Sidebar
with st.sidebar:

    st.header("🚀 RiseUP Profile")
    
    name = st.text_input("Your Full Name: ", key = "user_name")
    # email = st.text_input("Email Address:", key = "user_email")
    # target = st.text_input("Job Role(s) aiming ?", key= "user_target")
    # location = st.text_input("Location Prefered:", help="City, State Abb")
    resume = st.file_uploader("Upload your Resume", help=".pdf only", type= ["pdf"], accept_multiple_files= False)

    api_key = st.text_input("Your OpenAI API Key:", 
                            type="password", 
                            placeholder="sk-proj-",
                            help="You can get your key at https://platform.openai.com/account/api-keys")
    st.markdown(
        "<small>"
        "⚠️ <i>We never store or log your personal details or API key. They remain only in your browser session.</i>"
        "</small>", 
        unsafe_allow_html=True)
    
    save_profile = st.button("💾 Save Profile")

    if save_profile:
        
        if all([name, resume, api_key]):
            st.session_state.user_profile = {
                "user_name": name,
                # "user_email": email,
                # "user_target": "Data Science",
                # "user_location": "Remote/ Flexible",
                # "user_experience": "Mid Level"
                "user_resume": extract_resume_text(resume)
            }
            st.session_state["openai_api_key"] = api_key
            st.success("Profile saved successfully!")


        else:
            st.warning("⚠️ Please fill all the fields.")

### Main UI
def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system",  "content":  """
         You are an AI-powered Career Coach called “RiseUP AI.” 
         Your mission is to help the user with their career by choosing one of these tools as per user's request:
         
        - **resume_analyzer_tool**: When the user wants to analyze, review, or improve their resume.
        - **job_search_tool**: When the user wants help finding jobs.
        - **suggest_contacts_tool**: When user asks for some referrals or contact information.
         
         - If the user’s message is purely small talk (e.g., “Hi,” “How are you?”), 
         respond with a friendly acknowledgement and ask how you can help with their career goals today—do not attempt any of the above tasks.
         Always be concise, actionable, and professional. Keep the conversation focused on advancing the user’s career. """
        }
    ]

user_profile = st.session_state.get("user_profile", {})
user = user_profile.get("user_name", "")

if user:
    st.markdown(f"""
        <h2 style='color:#2E86AB;'>👋 {get_greeting()}, <span style='color:#FF6B6B;'>{user}</span>!</h2>
        <h5 style='margin-top:-10px;'>RiseUP Career Coach 🚀 is ready to assist you — let's land that dream job!</h5>
    """, unsafe_allow_html=True)

else:
     st.markdown("""
        <h2 style='color:#2E86AB;'>👋 Hello there!</h2>
        <h4 style='margin-top:-10px;'>I'm <span style='color:#FF6B6B;'>RiseUP</span> your AI-powered career coach.</h4>
        <h5>Let's explore jobs, refine resumes, or connect you with the right people!</h5>
    """, unsafe_allow_html=True)


for message in st.session_state.chat_history:
    if message["role"] != "system":
        st.chat_message(message["role"]).write(message["content"])

if st.session_state.get("openai_api_key"):

    llm_client = ChatOpenAI(api_key = st.session_state.openai_api_key, model = "gpt-4o-mini", temperature = 0.7)

    # Intializing Agent
    riseup_agent_executor = get_agent(llm_client)

    if prompt:= st.chat_input(placeholder="Please analyse my resume for Software Engineer job duties."):
        
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        riseup_response = riseup_agent_executor.run(input = prompt, chat_history = st.session_state.chat_history)

        st.session_state.chat_history.append({"role": "assistant", "content": riseup_response})
        st.chat_message("assistant").write(riseup_response)

