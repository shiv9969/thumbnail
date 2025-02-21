import requests
from bs4 import BeautifulSoup

def fetch_metadata(url):
    """
    Fetches metadata (thumbnail URL and title) from a given URL.

    Args:
        url (str): The URL to fetch metadata from.

    Returns:
        dict: A dictionary containing 'thumbnail_url' and 'title'.
    """
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        metadata = {}
        metadata['thumbnail_url'] = soup.find('meta', property='og:image')['content']
        metadata['title'] = soup.find('meta', property='og:title')['content'] or soup.find('title').text.strip()
        
        return metadata
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    url = input("Enter URL: ")
    metadata = fetch_metadata(url)
    if metadata:
        print(f"Thumbnail URL: {metadata['thumbnail_url']}")
        print(f"Title: {metadata['title']}")
    else:
        print("Failed to retrieve metadata.")
