import json

import requests

class Tempmail:
    def __init__(self, login, password, api_domain = 'https://api.mail.tm/'):
        self.login = login
        self.password = password
        self.api_domain = api_domain

    def create_email(self):
        url = self.api_domain + 'accounts'
        headers = {
            'Content-Type': 'application/ld+json',
            'Accept': 'application/ld+json'
        }
        data = {
            "address": f"{self.login}@{self.get_domain()}",
            "password": f"{self.password}"
        }
        if self.get_domain() is None:
            return None

        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 201:
            response = response.json()['content'].decode('utf-8')
            return response.json()['content']
        elif response.status_code == 422:
            print("Account already exists.")
            return f"{self.login}@{self.get_domain()}"
        else:
            return response.json()["violations"][0]["message"]

    def get_domain(self):
        url = self.api_domain + 'domains?page=1'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["hydra:member"][0]["domain"]
        else:
            return response.json()["violations"][0]["message"]