import configparser
import os
from dotenv import load_dotenv

import requests
from serpapi import GoogleSearch

class GoogleDork:
    def __init__(self, query = "", site = "", filetype = "", intitle = "", intext = ""):
        self.query = query
        self.site = site
        self.filetype = filetype
        self.intitle = intitle
        self.intext = intext

    def google_dorking(self):
        try:
            load_dotenv(dotenv_path="api.env")
            serpapi_api_key = os.getenv("SERPAPI_API_KEY")
            if serpapi_api_key == "":
                return False

            if self.filetype == "":
                params = {
                    "engine": "google",
                    "q": f'{self.query} site:"{self.site}" intitle:"{self.intitle}" intext:"{self.intext}"',
                    "api_key": f"{serpapi_api_key}",
                }
            else:
                params = {
                    "engine": "google",
                    "q": f'{self.query} site:"{self.site}" filetype:{self.filetype} intitle:"{self.intitle}" intext:"{self.intext}"',
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

        except Exception:
            return False
