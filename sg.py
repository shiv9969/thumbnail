import httpx
from bs4 import BeautifulSoup
import re
import random

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'
]

def get_sg_data(url):
    headers = {
        'User-Agent': random.choice(user_agents)
    }
    
    try:
        response = httpx.get(url, headers=headers, timeout=30, follow_redirects=True)
        response.raise_for_status()
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            image_urls = re.findall(r'https?://\S+\.jpg', str(soup))
            title = soup.find('title').text.strip()
            
            if image_urls:
                first_url = image_urls[0]
                return first_url, title
            else:
                return None, title
        else:
            return None, None
    except (httpx.RequestError, httpx.TimeoutException) as e:
        print(f"Error: {e}")
        return None, None
