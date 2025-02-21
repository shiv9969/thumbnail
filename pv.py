import requests
import re
from bs4 import BeautifulSoup
import random


# List of user agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 11; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'
]


def get_random_header():
    return {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }


def fetch_title(url):
    headers = get_random_header()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html5lib')
        title = soup.find('title')
        if title:
            return title.text.strip()
        h1 = soup.find('h1')
        if h1:
            return h1.text.strip()
        return "Title not found."
    else:
        return f"Failed to retrieve title (Status code: {response.status_code})"


def scrape_azpv_covershot(url):
    headers = get_random_header()
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve page: {response.status_code}")
        return None
    match = re.search(r'\"covershot\":\"(https://m\.media-amazon\.com/images/[^\"]+)\"', response.text)
    if match:
        covershot_url = match.group(1)
        return covershot_url
    else:
        print("Covershot URL not found.")
        return None
