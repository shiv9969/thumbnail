
import httpx
from bs4 import BeautifulSoup
import re


def get_kik_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.3'
    }

    response = httpx.get(url, headers=headers, timeout=30)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        image_urls = re.findall(r'https?://\S+\.jpg', str(soup))
        title = soup.find('title').text.strip()

        # Remove everything after "Watch"
        watch_index = title.find('Watch')
        if watch_index != -1:
            title = title[:watch_index].strip()

        if image_urls:
            first_url = image_urls[0]
            return first_url, title
        else:
            return None, title
    else:
        return None, None
