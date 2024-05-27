import sys
import requests
import argparse
import traceback
import os
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


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


def ai_generate(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        traceback.print_exc()
        return None


def validate_args(args):
    if args.url:
        if args.url.startswith("http"):
            return True
        else:
            print("Invalid URL. Please provide a valid URL.")
            return False
    else:
        print("Please provide a URL or a prompt.")
        return False


def main():
    parser = argparse.ArgumentParser(description="Fetch a webpage.")
    parser.add_argument("url", help="The URL of the webpage to fetch.")
    args = parser.parse_args()
    is_args_valid = validate_args(args=args)

    if not is_args_valid:
        print("Invalid arguments.")
        print("Usage: python main.py <URL>")
        sys.exit(1)

    page_content = fetch_reader_page(args.url)

    if not page_content:
        print(f"Failed to fetch web page: {args.url}")

    prompt = f"Generate an OpenAPI specification for the following webpage: {args.url}.\
        The webpage content is as follows: {page_content}"

    oas_file = ai_generate(prompt)

    with open("oas.yaml", "w") as f:
        f.write(oas_file)


if __name__ == "__main__":
    main()
