
import httpx
from bs4 import BeautifulSoup
import re

def get_atx_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.3'
    }
    response = httpx.get(url, headers=headers, timeout=30)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html5lib')
        title = soup.find('h1').text.strip() if soup.find('h1') else "No title found"
        image_urls = re.findall(r'https?://\S+\.jpg', str(soup))
        landscape_keywords = ["16x9", "1920x1080", "_landscape", "_landscape_thumb", "landscape_thumb", "IMG_L", "_1920x1080px", "LANDSCAPE_169", "-1923x1082"]
        portrait_keywords = ["2x3", "1000x1500", "_portrait", "_portrait_thumb", "portrait_thumb", "600x900", "IMGSQ", "_1000x1500px", "PORTRAIT", "-1001x1502", "_1098x1626_3x4"]
        all_url_parts = []
        for img_url in image_urls:
            url_parts = img_url.split(",")
            all_url_parts.extend(url_parts)
        landscape_url = None
        portrait_url = None
        for part in all_url_parts:
            if not landscape_url and ("IMG_L" in part.lower() and "KLIKK" in part.lower() or any(keyword.lower() in part.lower() for keyword in landscape_keywords)):
                landscape_url = part
            elif not portrait_url and ("IMGSQ" in part.lower() and "KLIKK" in part.lower() or any(keyword.lower() in part.lower() for keyword in portrait_keywords)) and part != landscape_url:
                portrait_url = part
        return {
            "title": title,
            "landscape_url": landscape_url,
            "portrait_url": portrait_url
        }
    return None
