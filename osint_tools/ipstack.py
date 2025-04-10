import configparser
import requests

def ipstack(ip):
    config = configparser.ConfigParser()
    config.read("api.env")
    try:
        ipstack_api_key = config.get("IPSTACK", "IPSTACK_API_KEY")
    except configparser.NoOptionError:
        return False

    response = requests.post(f"http://api.ipstack.com/{ip}?access_key={ipstack_api_key}")

    if response.text.find("invalid_access_key"):
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