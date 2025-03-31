import shodan
import configparser

def shodan_search():
    config = configparser.ConfigParser()
    config.read("api.env")
    shodan_api_key = config.get("SHODAN", "SHODAN_API_KEY")

    api = shodan.Shodan(shodan_api_key)

    try:
        # Search Shodan
        results = api.search('apache')

        # Show the results
        print('Results found: {}'.format(results['total']))
        for result in results['matches']:
            print('IP: {}'.format(result['ip_str']))
            print(result['data'])
            print('')
    except shodan.APIError as e:
        print('Error: {}'.format(e))