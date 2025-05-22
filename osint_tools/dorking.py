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

            all_data = []
            for result in results['organic_results']:
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

        except Exception as p:
            print(p)
            return False
