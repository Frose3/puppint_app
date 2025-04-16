import shodan
import configparser


def shodan_search(user_request):
    config = configparser.ConfigParser()
    config.read("api.env")
    try:
        shodan_api_key = config.get("SHODAN", "SHODAN_API_KEY")

        api = shodan.Shodan(shodan_api_key)

        results = api.search(user_request)

        return results

    except shodan.APIError as e:
        return False

def shodan_host(user_request):
    config = configparser.ConfigParser()
    config.read("api.env")
    try:
        shodan_api_key = config.get("SHODAN", "SHODAN_API_KEY")
        if shodan_api_key == "":
            return False

        api = shodan.Shodan(shodan_api_key)

        host = api.host(user_request)

        return host

    except shodan.APIError as e:
        return False
