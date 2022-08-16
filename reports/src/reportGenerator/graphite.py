import requests
import re
from reportGenerator.exceptions import InvalidUrlException

urlRegex = "https?:\/\/([\-a-zA-Z0-9.]+(?:\:\d{1,5})?)\/?((?:\/?[a-zA-Z0-9\-_?=&.~!$'()*+,;:@%]+)*)\/?"

def extract_url_and_page(config_url):
    result = re.search(urlRegex, config_url)
    if not result or not result.group(1):
        raise InvalidUrlException(config_url)
    return (result.group(1).replace('.', '_'), result.group(2).replace('/', '_') if result.group(2) else '_')

def prepare_endpoint(endpoint, test_url, function):
    (db_url, page) = extract_url_and_page(test_url)
    return endpoint.replace("$groupUrl", db_url).replace("$url", db_url).replace("$page", page).replace("$function", function)


class GraphiteClient:
    def __init__(self, url, auth):
        self.url = url
        self.auth= auth

    def query(self, raw_endpoint, test_url, function='median', tps_from="-30d", tps_to=None, max_data_points=1812, format="json"):
        endpoint = f'{self.url}/render?target={prepare_endpoint(raw_endpoint, test_url, function)}&format={format}&from={tps_from}{"&to={tps_to}" if tps_to else ""}&maxDataPoints={max_data_points}'
        results = requests.get(endpoint, auth=self.auth).json()
        for result in results:
            if(result.get("datapoints")):
                result["datapoints"] = list(filter(lambda value: value[0] != None, result["datapoints"]))
        return results

    def query_last(self, endpoint, test_url, tps_from="-30d", tps_to=None, format='json'):
        results = self.query(endpoint, test_url, tps_from=tps_from, tps_to=tps_to, format=format)
        for result in results:
            if(result.get("datapoints")):
                result["datapoints"] = result["datapoints"][-1:]
        return results
    
    def query_last_value(self, endpoint, test_url, tps_from="-30d", tps_to=None, format='json'):
        return self.query(endpoint, test_url, tps_from=tps_from, tps_to=tps_to, format=format)[0]["datapoints"][-1][0]


