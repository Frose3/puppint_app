import os
import configparser
import requests
from dotenv import load_dotenv

def ipstack(ip):
    try:
        load_dotenv(dotenv_path="api.env")
        ipstack_api_key = os.getenv("IPSTACK_API_KEY")
        if ipstack_api_key == "":
            return False

        response = requests.post(f"http://api.ipstack.com/{ip}?access_key={ipstack_api_key}")

        if response.text.find("invalid_access_key") != -1:
            return 2

        data = {
            "ip": ip,
            "country": response.json()["country_name"],
            "city": response.json()["city"],
            "region": response.json()["region_name"],
            "zip": response.json()["zip"],
            "latitude": response.json()["latitude"],
            "longitude": response.json()["longitude"],
            "language": response.json()["location"]["languages"][0]["name"]
        }

        return data
    except configparser.NoOptionError:
        return False