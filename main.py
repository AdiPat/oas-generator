import requests
import traceback


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
