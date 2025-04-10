import requests
import base64
import configparser
from datetime import date

def fullhunt(user_query):
    config = configparser.ConfigParser()
    config.read("api.env")
    fullhunt_api_key = config.get("FULLHUNT", "FULLHUNT_API_KEY")

    headers = {
        'X-API-KEY': fullhunt_api_key,
    }

    response = requests.get(f"https://fullhunt.io/api/v1/domain/{user_query}/details", headers=headers)

    if response.json().get('hosts'):
        return response.json()['hosts']

    else:
        return 0