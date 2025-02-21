import requests
from bs4 import BeautifulSoup

def fetch_metadata(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')
        
        metadata = {}
        metadata['thumbnail_url'] = soup.find('meta', property='og:image')['content']
        metadata['title'] = soup.find('meta', property='og:title')['content'] or soup.find('title').text.strip()
        
        return metadata
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Error: {e}")
        return None
