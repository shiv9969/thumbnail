import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.ERROR)

def fetch_metadata(url):
    """Fetches metadata (landscape image URL and title) from a given URL."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, timeout=5, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        metadata = {}
        
        # Landscape image URL (16x9)
        landscape_image = soup.select_one('meta[property="og:image"]')
        if landscape_image:
            metadata['landscape_image_url'] = landscape_image['content']
        
        # Title from h1 tag
        title = soup.select_one('h1')
        if title:
            metadata['title'] = title.text.strip()
        else:
            # Fallback to og:title if h1 not found
            title_meta = soup.select_one('meta[property="og:title"]')
            if title_meta:
                metadata['title'] = title_meta['content']
        
        return metadata
    
    except requests.RequestException as e:
        logging.error(f"Error fetching metadata from {url}: {e}")
        return None

if __name__ == "__main__":
    url = input("Enter URL: ")
    metadata = fetch_metadata(url)
    
    if metadata:
        print(f"Landscape Image URL: {metadata.get('landscape_image_url')}")
        print(f"Title: {metadata.get('title')}")
    else:
        print("Failed to retrieve metadata.")
