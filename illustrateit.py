import requests
import json
import logging
import re

# Constants
REDDIT_API_URL = "https://www.reddit.com/r/Illustration/random.json?limit=1"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
)
IMAGE_EXTENSIONS_PATTERN = re.compile(r'\.(jpg|jpeg|png)$', re.IGNORECASE)
README_FILE = 'README.md'

# Configure logging
logging.basicConfig(level=logging.INFO)

def fetch_random_link(api_url, user_agent):
    try:
        response = requests.get(api_url, headers={'User-agent': user_agent})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request error: {e}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"JSON decoding error: {e}")

def extract_link_url(post_data):
    try:
        post = post_data[0]['data']['children'][0]['data']
        link_url = post.get("url", "")
        if IMAGE_EXTENSIONS_PATTERN.search(link_url):
            return f"{link_url}?width=100&height=100"
        else:
            raise ValueError("No picture link found in the response.")
    except (KeyError, IndexError, AttributeError, ValueError) as e:
        raise RuntimeError(f"An error occurred while extracting picture link URL: {e}")

def update_readme_with_link(markdown):
    try:
        with open(README_FILE, 'r') as file:
            contents = file.readlines()

        for i, line in enumerate(contents):
            if "![Illustration]" in line:
                contents[i] = markdown + "\n"
                break

        with open(README_FILE, 'w') as file:
            file.writelines(contents)
    except (IOError, FileNotFoundError) as e:
        raise RuntimeError(f"An error occurred while updating {README_FILE}: {e}")

def main():
    try:
        post_data = fetch_random_link(REDDIT_API_URL, USER_AGENT)
        link_url = extract_link_url(post_data)
        markdown = f"![Illustration]({link_url})"
        update_readme_with_link(markdown)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
