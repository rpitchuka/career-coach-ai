from langchain_core.tools import Tool
from backend.tools.resume_analyzer import analyze_resume
from backend.tools.job_finder import search_jobs_muse
from backend.tools.suggest_contacts import suggest_contacts
from backend.tools.generate_message import generate_personalized_message
from langchain.agents import initialize_agent, AgentExecutor, AgentType

resume_analyzer_tool = Tool.from_function(
    func= analyze_resume,
    name= "resume_analyzer",
    description= "Use this to answer any question or improvement suggestions about the user's resume."
)

job_search_tool = Tool.from_function(
    func= search_jobs_muse,
    name= "job_finder",
    description= "Use this to fetch jobs from Muse API Endpoint, as per user's requirement."
)

suggest_contacts_tool = Tool.from_function(
    func= suggest_contacts,
    name="contact_suggestor",
    description="Use this tool to suggest relevant contact information based on the user's prompt."
)

personalized_message_tool = Tool.from_function(
    func= generate_personalized_message,
    name= "message_generator",
    description="Use this to generate personalized linkedin messages to user specified contacts."
)

def get_agent(llm_client) -> AgentExecutor:
    tools = [resume_analyzer_tool, job_search_tool, suggest_contacts_tool, personalized_message_tool]
    agent = initialize_agent(
        tools,
        llm_client,
        agent= AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        handle_parsing_errors = True,
        verbose = True
    )

    return agent

