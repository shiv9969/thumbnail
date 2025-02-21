import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def modify_url(url):
    """
    Modify the thumbnail URL.
    
    :param url: Original thumbnail URL.
    :return: Modified thumbnail URL.
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    
    # Remove aspectRatio
    query_params.pop('aspectRatio', None)
    
    # Update width
    query_params['width'] = ['3800']
    
    # Update format
    query_params['format'] = ['jpeg']
    
    modified_query = urlencode(query_params, doseq=True)
    modified_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, modified_query, parsed_url.fragment))
    
    return modified_url


def fetch_thumbnail_and_title(url):
    """
    Fetch thumbnail URL and page title.
    
    :param url: Webpage URL.
    :return: Modified thumbnail URL, page title.
    """
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Fetch thumbnail URL
        thumbnail_url = soup.find('meta', property='og:image')['content']
        modified_thumbnail_url = modify_url(thumbnail_url)
        
        # Fetch page title
        title = soup.find('h1').text.strip()
        
        return modified_thumbnail_url, title
    
    except Exception as e:
        print(f"Error: {e}")
        return None, None
