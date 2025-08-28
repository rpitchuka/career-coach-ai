# RiseUP AI - Career Coach Assistant 🚀

An **AI-powered career coach** built with **LangChain, OpenAI, and Streamlit**.  
This assistant helps job seekers and professionals by analyzing resumes, suggesting jobs, recommending networking contacts, and generating personalized outreach messages.  

## Features
- **Resume Analyzer** → Provides insights on strengths, gaps, and alignment with job roles.  
- **Job Finder** → Finds relevant opportunities based on skills, domain, and interests.  
- **Contact Suggester** → Recommends networking contacts to improve reach.  
- **Message Generator** → Creates tailored outreach messages for recruiters or LinkedIn.  
- **Streamlit UI** → Simple web interface for interactive use.  

## Tech Stack
- **Frontend**: Streamlit  
- **Backend / Orchestration**: LangChain, Python  
- **LLM Integration**: OpenAI GPT models  
- **Modules**:  
  - `agent.py` → Core agent orchestration  
  - `resume_analyzer.py` → Resume insights and parsing  
  - `job_finder.py` → Job search and filtering  
  - `suggest_contacts.py` → Contact recommendations  
  - `generate_message.py` → Outreach message creation  
  - `streamlit_app.py` → UI entry point  
- **Dependencies**: see `requirements.txt`

## Getting Started
### Prerequisites
- Python 3.10+  
- An OpenAI API key  

### Installation
```bash
git clone https://github.com/<your-username>/career-coach-ai.git
cd career-coach-ai
pip install -r requirements.txt
