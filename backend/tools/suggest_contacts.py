import os
import requests
from langchain_core.tools import tool

@tool
def suggest_contacts(prompt: str):
    """
    Uses SerpAPI to find LinkedIn profiles relevant to a job or company.
    Returns a list of dictionaries with name, LinkedIn URL, and snippet.
    """

    serpapi_endpoint = "https://serpapi.com/search.json"
    
    improved_prompt = f"site:linkedin.com/in {prompt} contact"
    
    params = {
        "engine": "google",
        "q": improved_prompt,
        "num": 10,
        "api_key": os.getenv("SERP_API_KEY")
    }

    try:
        response = requests.get(serpapi_endpoint, params=params)
        response.raise_for_status()  # raise exception if response is not 200
        data = response.json()

        contacts_list = []
        for contact in data.get("organic_results", []):
            link = contact.get("link", "")
            if "linkedin.com/in" in link:
                contacts_list.append({
                    "name": contact.get("title", "N/A"),
                    "linkedin_url": link,
                    "snippet": contact.get("snippet", "")
                })

        return contacts_list or [{"message": "No LinkedIn profiles found with these parameters."}]

    except Exception as e:
        return [{"error": f"SerpAPI error: {str(e)}"}]
