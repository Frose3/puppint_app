import configparser

import requests
from serpapi import GoogleSearch

def reverse_image(img_url):
    config = configparser.ConfigParser()
    config.read("api.env")
    try:
        serpapi_api_key = config.get("SERPAPI", "SERPAPI_API_KEY")
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