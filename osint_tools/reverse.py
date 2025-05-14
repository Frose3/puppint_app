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

        data = {
            "favicon": results["organic_results"]["favicon"],
            "link": results["organic_results"]["link"],
            "title": results["organic_results"]["title"],
            "source": results["organic_results"]["source"],
            "displayed_link": results["organic_results"]["displayed_link"],
            "snippet": results["organic_results"]["snippet"],
            "redirect_link": results["organic_results"]["redirect_link"],
        }

        return data

    except Exception as e:
        return False