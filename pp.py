import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import logging

logging.basicConfig(level=logging.INFO)

def extract_identifier(input_url: str) -> str:
    """
    Extract identifier from input URL.
    
    Args:
    input_url (str): Input URL.
    
    Returns:
    str: Identifier.
    """
    parsed_url = urlparse(input_url)
    query_params = parse_qs(parsed_url.query)
    identifier = parsed_url.path.split('/')[-1]
    return identifier

def get_thumbnail(homepage_url: str, identifier: str) -> dict:
    """
    Get thumbnail URLs and video title.
    
    Args:
    homepage_url (str): Homepage URL.
    identifier (str): Identifier.
    
    Returns:
    dict: Thumbnail URLs and video title or None.
    """
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.3',
    ]
    headers = {'User-Agent': user_agents[0]}
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            response = httpx.get(homepage_url, headers=headers, timeout=10)
            response.raise_for_status()
        except (httpx.RequestError, httpx.HTTPError) as e:
            logging.error(f"Request error (attempt {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                # Rotate User-Agent and wait before retrying
                headers['User-Agent'] = user_agents[(attempt + 1) % len(user_agents)]
                import time
                time.sleep(2 ** attempt)
            else:
                return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    thumbnail_element = soup.find(lambda tag: tag.has_attr('data-find') and tag['data-find'] == identifier)
    if thumbnail_element is None:
        id_value = f"NTA_{identifier}"
        thumbnail_element = soup.find(id=id_value)
    
    if thumbnail_element:
        portrait_url = thumbnail_element.get('src')
        landscape_url = thumbnail_element.get('data-poster')
        title = thumbnail_element.get('data-name')
        
        # Validate URLs
        if portrait_url.startswith('http') and landscape_url.startswith('http'):
            return {
                'portrait_url': portrait_url,
                'landscape_url': landscape_url,
                'title': title
            }
    return None

def process_url(input_url: str) -> str:
    """
    Process URL and format output for Telegram bot.
    
    Args:
    input_url (str): Input URL.
    
    Returns:
    str: Formatted output.
    """
    homepage_url = "https://www.playflix.app"  # Replace with your homepage URL
    identifier = extract_identifier(input_url)
    result = get_thumbnail(homepage_url, identifier)
    if result:        
        output = f"""
<b>Data-poster URL:</b> {result['landscape_url']}

<b>Thumbnail URL:</b> <a href='{result['portrait_url']}'><b>Click Here</b></a>

<b>Title:</b> <b> {result['title']} </b>
"""    
        return output
    else:
        return "Thumbnail not found."
