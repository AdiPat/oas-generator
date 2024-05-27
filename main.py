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
        print("Running Prompt: ", prompt)
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        print("response: ", response.text)
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


def count_tokens(text: str) -> int:
    tokens = text.split()
    return len(tokens)


def main():
    print("Welcome to OAS Generator!")
    parser = argparse.ArgumentParser(description="Fetch a webpage.")
    parser.add_argument("url", help="The URL of the webpage to fetch.")
    args = parser.parse_args()
    is_args_valid = validate_args(args=args)

    if not is_args_valid:
        print("Invalid arguments.")
        print("Usage: python main.py <URL>")
        sys.exit(1)

    print("Fetching: ", args.url)

    page_content = fetch_reader_page(args.url)
    tokens = count_tokens(page_content)

    print(f"Processing ${tokens} tokens from the webpage.")

    if not page_content:
        print(f"Failed to fetch web page: {args.url}")

    prompt = f"Generate an OpenAPI specification for the following webpage. \
        Don't truncate the output, return the full YAML specification for the page. \
        The webpage content is as follows: ```{page_content}```"

    oas_file = ai_generate(prompt)

    if not oas_file:
        print("Failed to generate OAS file. ")
        sys.exit(1)

    print(
        f"Writing OpenAPI specification to oas.yaml: tokens = ${count_tokens(oas_file)}"
    )

    with open("oas.yaml", "w") as f:
        f.write(oas_file)


if __name__ == "__main__":
    main()
