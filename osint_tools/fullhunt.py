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

            data = {
                "host": response.json()['hosts']['host'],
                "domain": response.json()['hosts']['domain'],
                "ip_address": response.json()['hosts']['ip_address'],
                "http_status_code": response.json()['hosts']['http_status_code'],
                "http_title": response.json()['hosts']['http_title'],
                "network_ports": response.json()['hosts']['network_ports'],
                "tags": response.json()['hosts']['tags'],

                "dns_a": response.json()['hosts']['dns']['a'],
                "dns_aaa": response.json()['hosts']['dns']['aaa'],
                "dns_cname": response.json()['hosts']['dns']['cname'],
                "dns_ptr": response.json()['hosts']['dns']['ptr'],

                "ip_metadata_asn": response.json()['hosts']['ip_metadata']['asn'],
                "ip_metadata_isp": response.json()['hosts']['ip_metadata']['isp'],
                "ip_metadata_organization": response.json()['hosts']['ip_metadata']['organization'],
                "ip_metadata_city_name": response.json()['hosts']['ip_metadata']['city_name'],
                "ip_metadata_region": response.json()['hosts']['ip_metadata']['region'],
                "ip_metadata_postal_code": response.json()['hosts']['ip_metadata']['postal_code'],
                "ip_metadata_country_name": response.json()['hosts']['ip_metadata']['country_name'],
                "ip_metadata.location_latitude": response.json()['hosts']['ip_metadata']['location_latitude'],
                "ip_metadata.location_longitude": response.json()['hosts']['ip_metadata']['location_longitude'],
            }

            return data
        elif response.json().get('message') == 'Invalid API Key':
            raise Exception("Invalid API Key")
        else:
            raise Exception(response.json().get('message'))
    except Exception:
        return False