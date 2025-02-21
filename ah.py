import httpx
from bs4 import BeautifulSoup
import re

def get_ah_data(url):
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
        first_url = image_urls[0].split(',')[0]
        
        # Create landscape and portrait URLs
        landscape_url = first_url.replace("16x9", "16x9") + "?width=4000"
        portrait_url = first_url.replace("16x9", "2x3") + "?width=4000"
        
        # Fetch title from h1 tag
        h1_tag = soup.find('h1')
        if h1_tag:
            title = h1_tag.text.strip()
        else:
            title = "No h1 tag found"
        
        return landscape_url, portrait_url, title
    else:
        return None, None, "Failed to retrieve webpage. Status code: {}".format(response.status_code)
