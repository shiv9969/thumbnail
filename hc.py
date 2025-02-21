import requests
import json
from urllib.parse import urlparse
from fuzzywuzzy import fuzz, process

api_url = "https://www.hoichoi.tv/cache/popular-search"

def extract_title(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    title = path.strip('/').split('/')[-1]
    return title

def recursive_search(data, target_title):
    found_data = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'title':
                ratio = fuzz.ratio(value.lower(), target_title.lower())
                if ratio > 80:
                    found_data.append(data)
            elif isinstance(value, (dict, list)):
                found_data.extend(recursive_search(value, target_title))
    elif isinstance(data, list):
        for item in data:
            found_data.extend(recursive_search(item, target_title))
    return found_data

def fetch_data(video_url):
    title = extract_title(video_url)
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        found_data = recursive_search(data, title)
        if found_data:
            landscape_url = None
            portrait_url = None
            for found in found_data:
                for key, value in found.items():
                    if isinstance(value, dict):
                        if '_3x4' in value:
                            portrait_url = value['_3x4']
                        if '_16x9' in value:
                            landscape_url = value['_16x9']
            return {
                "landscape_url": landscape_url,
                "portrait_url": portrait_url,
                "title": title
            }
        else:
            return None
    else:
        return None
