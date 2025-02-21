import httpx
from bs4 import BeautifulSoup
import re

def get_thumbnail_and_title(url):
    """
    Fetches thumbnail URL and title from a given URL.

    Args:
        url (str): URL to fetch thumbnail and title.

    Returns:
        tuple: (thumbnail_url, title)
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.3'
    }
    try:
        response = httpx.get(url, headers=headers, timeout=30)
        response.raise_for_status()  
    except httpx.RequestError as e:
        print(f"Error: {e}")
        return None, None

    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text.strip() or soup.find('h1').text.strip()
    image_urls = re.findall(r'https?://\S+\.jpg|https?://\S+\.png', str(soup))

    if title and image_urls:
        return image_urls[0], title
    elif title:
        return None, title
    elif image_urls:
        return image_urls[0], None
    else:
        return None, None
