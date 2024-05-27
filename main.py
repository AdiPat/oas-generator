import requests
import traceback
import os
from dotenv import load_dotenv


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def fetch_html(url: str) -> str:
    try:
        response = requests.get(url)
        return response.text
    except requests.exceptions.RequestException as e:
        traceback.print_exc()
        return None


def fetch_reader_page(url: str) -> str:
    try:
        url = "https://r.jina.ai/" + url
        return fetch_html(url)
    except requests.exceptions.RequestException as e:
        traceback.print_exc()
        return None
