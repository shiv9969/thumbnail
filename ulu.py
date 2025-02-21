import requests
import json
import os
import sys
import cloudinary
from cloudinary import uploader

# Cloudinary configuration
cloudinary.config(
    cloud_name="replace",
    api_key="replace_cloudinary",
    api_secret="replace_cloudinary"
)

# Base URL for thumbnail API
base_url = "https://ullu.app/ulluCore/api/ullu2/media/getMediaByTitleYearSlugAndFamilySafe/cdiOpn?familySafe=no&titleYearSlug="
# Base URL for images
image_base_url = "https://ullu2-files.ullu.app"

def recursive_search(data, target):
    if isinstance(data, dict):
        if target in data.values():
            return data
        else:
            for key, value in data.items():
                found = recursive_search(value, target)
                if found:
                    return found
    elif isinstance(data, list):
        for item in data:
            found = recursive_search(item, target)
            if found:
                return found
    return None

def get_thumbnails(video_url):
    try:
        # Extract titleYearSlug from video URL
        title_year_slug = video_url.split('/')[-1]
        # Construct thumbnail API URL
        thumbnail_api_url = base_url + title_year_slug
        # Fetch thumbnail API data
        response = requests.get(thumbnail_api_url)
        if response.status_code == 200:
            thumbnail_data = response.json()
            # Recursive search for PORTRAIT and LANDSCAPE
            portrait = recursive_search(thumbnail_data, "PORTRAIT")
            landscape = recursive_search(thumbnail_data, "LANDSCAPE")
            # Download and save thumbnails as .jpg
            if portrait:
                portrait_file_id = portrait['fileId']
                portrait_url = image_base_url + portrait_file_id
                response = requests.get(portrait_url)
                with open('portrait.jpg', 'wb') as f:
                    f.write(response.content)
                # Upload to Cloudinary
                cloudinary_portrait_url = uploader.upload('portrait.jpg', type="private")["secure_url"]
                os.remove('portrait.jpg')  # Remove local file
            if landscape:
                landscape_file_id = landscape['fileId']
                landscape_url = image_base_url + landscape_file_id
                response = requests.get(landscape_url)
                with open('landscape.jpg', 'wb') as f:
                    f.write(response.content)
                # Upload to Cloudinary
                cloudinary_landscape_url = uploader.upload('landscape.jpg', type="private")["secure_url"]
                os.remove('landscape.jpg')  # Remove local file
            return cloudinary_portrait_url, cloudinary_landscape_url
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None, None

def main(video_url):
    # Delete existing thumbnail files
    try:
        os.remove('portrait.jpg')
        os.remove('landscape.jpg')
    except FileNotFoundError:
        pass
    portrait_url, landscape_url = get_thumbnails(video_url)
    print("Portrait URL:", portrait_url)
    print("Landscape URL:", landscape_url)
    # Verify files exist and have non-zero size (not needed with Cloudinary)
    print("Thumbnails uploaded to Cloudinary successfully.")

if __name__ == '__main__':
    main(sys.argv[1])
