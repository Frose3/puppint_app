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
        all_data = []
        for result in results['image_results']:
            data = {
                "favicon": result["favicon"],
                "link": result["link"],
                "title": result["title"],
                "source": result["source"],
                "displayed_link": result["displayed_link"],
                "snippet": result["snippet"],
                "redirect_link": result["redirect_link"],
            }
            all_data.append(data)

        return all_data

    except Exception as e:
        print(e)
        return e