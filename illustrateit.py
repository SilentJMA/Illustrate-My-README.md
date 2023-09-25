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

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define a regex pattern to match common image file extensions
IMAGE_EXTENSIONS_PATTERN = re.compile(r'\.(jpg|jpeg|png)$', re.IGNORECASE)

def fetch_random_link(api_url, user_agent):
    """
    Fetch a random link from Reddit's API.

    Args:
        api_url (str): The API URL to fetch the link.
        user_agent (str): The user agent to use in the request headers.

    Returns:
        dict: The JSON data containing the link information.
    """
    try:
        response = requests.get(api_url, headers={'User-agent': user_agent})
        response.raise_for_status()
        return json.loads(response.text)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request error: {e}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"JSON decoding error: {e}")

def extract_link_url(post_data):
    """
    Extract the URL of a picture link from Reddit post data.

    Args:
        post_data (dict): JSON data containing post information.

    Returns:
        str: The URL of the picture link or None if not found.
    """
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
            if IMAGE_EXTENSIONS_PATTERN.search(link_url):
                return f"{link_url}?width=100&height=100"
        raise ValueError("No picture link found in the response.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while extracting picture link URL: {e}")

def update_readme_with_link(markdown):
    """
    Update the README.md file with a link in Markdown format.

    Args:
        markdown (str): The Markdown representation of the link.
    """
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
        raise RuntimeError(f"An error occurred while updating README.md: {e}")

def main():
    try:
        post_data = fetch_random_link(REDDIT_API_URL, USER_AGENT)
        if post_data:
            link_url = extract_link_url(post_data)
            if link_url:
                markdown = f"![Illustration]({link_url})"
                update_readme_with_link(markdown)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
