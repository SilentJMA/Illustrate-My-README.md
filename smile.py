import requests
import json
import logging

# Constants
REDDIT_API_URL = "https://www.reddit.com/r/SketchDaily/random.json?limit=1"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
)

# Configure logging
logging.basicConfig(level=logging.INFO)

def fetch_random_meme(api_url, user_agent):
    try:
        response = requests.get(api_url, headers={'User-agent': user_agent})
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404)
        return json.loads(response.text)
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding error: {e}")

def extract_meme_url(meme_data):
    try:
        if (
            isinstance(meme_data, list)
            and meme_data
            and "data" in meme_data[0]
            and "children" in meme_data[0]["data"]
            and meme_data[0]["data"]["children"]
            and "data" in meme_data[0]["data"]["children"][0]
            and "url" in meme_data[0]["data"]["children"][0]["data"]
        ):
            meme_url = meme_data[0]["data"]["children"][0]["data"]["url"]
            return f"{meme_url}?width=100&height=100"
        else:
            logging.error("Unexpected JSON structure in the response.")
    except Exception as e:
        logging.error(f"An error occurred while extracting meme URL: {e}")

def update_readme_with_meme(markdown):
    try:
        with open('README.md', 'r') as file:
            contents = file.readlines()

        for i, line in enumerate(contents):
            if "![Make me Smile]" in line:
                contents[i] = markdown + "\n"
                break

        with open('README.md', 'w') as file:
            file.writelines(contents)
    except Exception as e:
        logging.error(f"An error occurred while updating README.md: {e}")

def main():
    meme_data = fetch_random_meme(REDDIT_API_URL, USER_AGENT)
    if meme_data:
        meme_url = extract_meme_url(meme_data)
        if meme_url:
            markdown = f"![Make me Smile]({meme_url})"
            update_readme_with_meme(markdown)

if __name__ == "__main__":
    main()
