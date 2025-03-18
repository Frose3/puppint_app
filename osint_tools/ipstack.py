import configparser
import requests

def ipstack(ip):
    config = configparser.ConfigParser()
    config.read("api.env")
    ipstack_api_key = config.get("IPSTACK", "IPSTACK_API_KEY")

    response = requests.post(f"http://api.ipstack.com/{ip}?access_key={ipstack_api_key}")

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