import requests
import json
import logging

# Constants
REDDIT_API_URL = "https://www.reddit.com/r/Illustration/random.json?limit=1"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
)

# Configure logging
logging.basicConfig(level=logging.INFO)

def fetch_random_link(api_url, user_agent):
    try:
        response = requests.get(api_url, headers={'User-agent': user_agent})
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404)
        return json.loads(response.text)
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding error: {e}")

def extract_link_url(post_data):
    try:
        if (
            isinstance(post_data, list)
            and post_data
            and "data" in post_data[0]
            and "children" in post_data[0]["data"]
            and post_data[0]["data"]["children"]
            and "data" in post_data[0]["data"]["children"][0]
            and "url" in post_data[0]["data"]["children"][0]["data"]
        ):
            link_url = post_data[0]["data"]["children"][0]["data"]["url"]
            return f"{link_url}?width=100&height=100"
        else:
            logging.error("Unexpected JSON structure in the response.")
    except Exception as e:
        logging.error(f"An error occurred while extracting link URL: {e}")

def update_readme_with_link(markdown):
    try:
        with open('README.md', 'r') as file:
            contents = file.readlines()

        for i, line in enumerate(contents):
            if "![Illustration]" in line:
                contents[i] = markdown + "\n"
                break

        with open('README.md', 'w') as file:
            file.writelines(contents)
    except Exception as e:
        logging.error(f"An error occurred while updating README.md: {e}")

def main():
    post_data = fetch_random_link(REDDIT_API_URL, USER_AGENT)
    if post_data:
        link_url = extract_link_url(post_data)
        if link_url:
            markdown = f"![Illustration]({link_url})"
            update_readme_with_link(markdown)

if __name__ == "__main__":
    main()
