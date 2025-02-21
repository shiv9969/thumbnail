import requests
from bs4 import BeautifulSoup

def fetch_thumbnail_and_title(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        thumbnail_url = soup.find('meta', property='og:image')
        title = soup.find('title')

        if thumbnail_url and title:
            return thumbnail_url['content'], title.text.strip()
        elif thumbnail_url:
            return thumbnail_url['content'], None
        elif title:
            return None, title.text.strip()
        else:
            return None, None

    except Exception as e:
        print(f"Error: {e}")
        return None, None
