from langchain.tools import tool
import requests
from dotenv import load_dotenv
import os
from rich import print
from tavily import TavilyClient
from bs4 import BeautifulSoup
from readability import Document
import trafilatura
import re

load_dotenv()
tavily_client = TavilyClient(api_key=os.getenv("Tavily_API_KEY"))

@tool
def web_search(query: str) -> str:
    """ search the web for recent and reliable information on a topic. 
    Return the title, URl, and relevant content for each useful result. """

    results = tavily_client.search(query=query, max_results=3)

    output = []

    for result in results['results']:
        output.append(f"Title:{result['title']}\n"
                   f"Url:{result['url']}\n"
                   F"content:{result['content']}\n")

    return "\n".join(output)
@tool
def web_scrape(url : str) -> str:
    """ scrape  and extract clean readable content from a url.
    uses multiple extraction strategies for better reliability."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup([
        "scripts",
        "style",
        "nav",
        "footer",
        "header",
        "aside",
        "form",
    ]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip= True)

    return text