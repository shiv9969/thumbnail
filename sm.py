import httpx
from bs4 import BeautifulSoup
import re

def get_thumbnail_and_title(url):
    """
    Fetches thumbnail URLs and title from the given URL.
    
    Args:
    url (str): URL to process.
    
    Returns:
    tuple: (landscape_url, portrait_url, title)
    """
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.3'
    }
    
    response = httpx.get(url, headers=headers, timeout=30)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        image_urls = re.findall(r'https?://\S+\.jpg', str(soup))
        original_url = image_urls[0].split(',')[0]
        
        # Create landscape and portrait URLs
        landscape_url = original_url.replace("large_16_9", "xl_image_16_9")
        portrait_url = original_url.replace("large_16_9", "xl_image_2_3")
        
        # Fetch h1 tag text
        h1_tag = soup.find('h1')
        if h1_tag:
            title = h1_tag.text.strip()
        else:
            title = "No h1 tag found"
        
        return landscape_url, portrait_url, title
    else:
        return None, None, "Failed to retrieve webpage. Status code: {}".format(response.status_code)
