import requests
from bs4 import BeautifulSoup

def fetch_thumbnail_and_title(url):
    """
    Fetches the thumbnail URL and title from a given webpage.

    Args:
        url (str): Webpage URL.

    Returns:
        dict: {'thumbnail_url': str, 'title': str} or None if failed.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Fetch thumbnail URL
        thumbnail_url_tag = soup.find('meta', property='og:image')
        if thumbnail_url_tag:
            original_url = thumbnail_url_tag['content']
            cleaned_url = original_url.split('/w_')[0] + original_url.split('eco')[1]
            cleaned_url = cleaned_url.replace('avif,q_auto:','')
            thumbnail_url = cleaned_url
        else:
            thumbnail_url = None
        
        # Fetch title
        title_tag = soup.find('h1')
        if title_tag:
            title = title_tag.text.strip()
        else:
            title = None
        
        return {'thumbnail_url': thumbnail_url, 'title': title}
    
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    return None
