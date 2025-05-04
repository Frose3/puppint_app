import configparser
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

def reverse_image(img_url):
    try:
        load_dotenv(dotenv_path="api.env")
        serpapi_api_key = os.getenv("SERPAPI_API_KEY")
        if serpapi_api_key == "":
            return False

        params = {
            "engine": "google_reverse_image",
            "image_url": f"{img_url}",
            "api_key": f"{serpapi_api_key}",
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        return results

    except configparser.NoOptionError:
        return False