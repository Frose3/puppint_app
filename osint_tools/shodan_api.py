import shodan
import configparser
import os

def deep_get(d, keys, default='N/A'):
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, default)
        else:
            return default

    if d is not None:
        return d
    else:
        return default

def shodan_search(user_request):
    # config = configparser.ConfigParser()
    # config.read("api.env")

    try:
        # shodan_api_key = config.get("SHODAN", "SHODAN_API_KEY")
        shodan_api_key = os.getenv("SHODAN_API")
        api = shodan.Shodan(shodan_api_key)

        results = api.search(user_request)

        all_data = []

        for item in results['matches']:
            data = {
                "title": deep_get(item, ['http', 'title']),
                "hostnames": item.get('hostnames', []),
                "org": item.get('org', 'N/A'),
                "isp": item.get('isp', 'N/A'),
                "port": item.get('port', 'N/A'),
                "city": deep_get(item, ['location', 'city']),
                "country": deep_get(item, ['location', 'country']),
                "ip": item.get('ip_str', 'N/A'),
                "domains": item.get('domains', []),
                "product": deep_get(item, ['http', 'product']),
                "ssl_subject_cn": deep_get(item, ['ssl', 'cert', 'subject', 'CN']),
                "ssl_issuer_cn": deep_get(item, ['ssl', 'cert', 'issuer', 'CN']),
                "ssl_valid_from": deep_get(item, ['ssl', 'cert', 'issued']),
                "ssl_valid_to": deep_get(item, ['ssl', 'cert', 'expires']),
                "ssl_expired": deep_get(item, ['ssl', 'cert', 'expired']),
                "ssl_cipher_name": deep_get(item, ['ssl', 'cipher', 'name']),
                "ssl_version": deep_get(item, ['ssl', 'cipher', 'version']),
            }
            all_data.append(data)

        return all_data

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
