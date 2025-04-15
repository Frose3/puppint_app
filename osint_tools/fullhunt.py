import requests
import base64
import configparser
from datetime import date
import httpx

def fullhunt(user_query):
    config = configparser.ConfigParser()
    config.read("api.env")
    try:
        fullhunt_api_key = config.get("FULLHUNT", "FULLHUNT_API_KEY")
        if fullhunt_api_key == "":
            return False
    except configparser.NoOptionError:
        return False

    headers = {
        'X-API-KEY': fullhunt_api_key,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Connection': 'close'
    }

    url = f"https://fullhunt.io/api/v1/domain/{user_query}/details"
    response = httpx.get(url, headers=headers)

    if response.json().get('hosts'):
        return response.json()['hosts']
    elif response.json().get('message') == 'Invalid API Key':
        return 2
    else:
        return 3