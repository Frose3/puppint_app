import configparser

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
        config = configparser.ConfigParser()
        config.read("api.env")
        try:
            serpapi_api_key = config.get("SERPAPI", "SERPAPI_API_KEY")
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

            return results

        except configparser.NoOptionError:
            return False


    # def google_dorking(query, site, filetype, intitle, intext):
    #     config = configparser.ConfigParser()
    #     config.read("api.env")
    #     try:
    #         serpapi_api_key = config.get("SERPAPI", "SERPAPI_API_KEY")
    #         if serpapi_api_key == "":
    #             return False
    #
    #         params = {
    #             "engine": "google",
    #             "q": f'{query} site:"{site}" filetype:{filetype} intitle:"{intitle}" intext:"{intext}"',
    #             "api_key": f"{serpapi_api_key}",
    #         }
    #
    #         search = GoogleSearch(params)
    #         results = search.get_dict()
    #
    #         return results['organic_results']
    #
    #     except configparser.NoOptionError:
    #         return False