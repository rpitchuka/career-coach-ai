import os
import json
import requests
import streamlit as st
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def search_jobs_muse(prompt: str) -> dict:
    """
    Given a user's prompt to find jobs based on some specifications,
    this tool is used to hit the Jsearch Rapid API endpoint, and 
    return relevant jobs to the user.
    """
    rapid_api_endpoint = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "x-rapidapi-host": "jsearch.p.rapidapi.com",
        "x-rapidapi-key": os.getenv("X-RapidAPI-Key")
    }

    query_params = {
        "query": prompt
    }

    api_response = requests.get(url= rapid_api_endpoint, headers= headers, params= query_params)

    return api_response.json()
