import os
import requests
import base64
import configparser
from datetime import date
import httpx
from dotenv import load_dotenv

def fullhunt(user_query):
    try:
        load_dotenv(dotenv_path="api.env")
        fullhunt_api_key = os.getenv("FULLHUNT_API_KEY")
        if fullhunt_api_key == "":
            return False

        headers = {
            'X-API-KEY': fullhunt_api_key,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Connection': 'close'
        }

        response = httpx.get(f"https://fullhunt.io/api/v1/domain/{user_query}/details", headers=headers)

        if response.json().get('hosts'):
            return response.json()['hosts']
        elif response.json().get('message') == 'Invalid API Key':
            raise Exception("Invalid API Key")
        else:
            raise Exception(response.json().get('message'))
    except configparser.NoOptionError:
        return False