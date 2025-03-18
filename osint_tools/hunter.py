import requests
import base64
import configparser
from datetime import date

def hunter(user_query):
    config = configparser.ConfigParser()
    config.read("api.env")
    hunter_api = config.get("HUNTER", "HUNTER_API_KEY")
    query = user_query
    encoded_query = base64.urlsafe_b64encode(query.encode("utf-8")).decode('ascii')
    page = 1
    page_size = 10
    # start_time = date.today().replace(year=date.today().year - 1, month=1, day=1).strftime("%Y-%m-%d")
    # end_time = date.today().replace(year=date.today().year - 1, month=11, day=30).strftime("%Y-%m-%d")

    start_time = "2022-01-01"
    end_time = "2022-01-03"

    url = f"https://api.hunter.how/search?api-key={hunter_api}&query={encoded_query}&page={page}&page_size={page_size}&start_time={start_time}&end_time={end_time}"

    response = requests.get(url, verify=False)
    return response.json()['data']['list']