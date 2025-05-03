import json
from typing import Any
import logging

import requests

class Tempmail:
    def __init__(self, login, password, api_domain = 'https://api.mail.tm/'):
        self.login = login
        self.password = password
        self.api_domain = api_domain

    def create_email(self) -> Any:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        if self.get_domain() is None:
            logging.error("Doména není k dispozici")
            return None

        data = {
            "address": f"{self.login}@{self.get_domain()}",
            "password": f"{self.password}"
        }

        response = requests.post(f"{self.api_domain}/accounts", headers=headers, data=json.dumps(data))
        if response.status_code == 201:
            response = response.json()['address']
            return response
        elif response.status_code == 422:
            logging.debug("Daný email již existuje.")
            return 422
        elif response.status_code == 500:
            logging.error(response.json()["detail"])
            return None
        else:
            logging.error(response.json()["violations"][0]["message"])
            return None

    def get_domain(self):
        response = requests.get(f"{self.api_domain}/domains?page=1")
        if response.status_code == 200:
            return response.json()["hydra:member"][0]["domain"]
        else:
            return None