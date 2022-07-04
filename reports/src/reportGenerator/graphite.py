import requests
import re

urlRegex = "https?:\/\/([\-a-zA-z0-9.]+(?:\:[0-9]{1,5})?)\/?((?:\/?[a-zA-Z0-9\-_?=&.~!$'()*+,;:@%]+)*)\/?"

def extractUrlAndPage(configUrl):
    result = re.search(urlRegex, configUrl)
    if not result:
        raise Exception(f"{configUrl} n'est pas une url valide")
    return (result.group(1).replace('.', '_'), result.group(2).replace('/', '_') if result.group(2) else '_')

def prepareEndpoint(endpoint, testUrl, function, grouped):
    (dbUrl, page) = extractUrlAndPage(testUrl)
    return endpoint.replace("$groupUrl", dbUrl + "." if grouped else "").replace("$url", dbUrl).replace("$page", page).replace("$function", function)


class GraphiteClient:
    def __init__(self, url, auth):
        self.url = url
        self.auth= auth

    def query(self, rawEndpoint, testUrl, grouped=True, function='median', tps_from="-30d", tps_to=None, maxDataPoints=1812, format="json"):
        endpoint = f'{self.url}/render?target={prepareEndpoint(rawEndpoint, testUrl, function, grouped)}&format={format}&from={tps_from}{"&to={tps_to}" if tps_to else ""}&maxDataPoints={maxDataPoints}'
        # print(endpoint)
        results = requests.get(endpoint, auth=self.auth).json()
        for result in results:
            if(result.get("datapoints")):
                result["datapoints"] = list(filter(lambda value: value[0] != None, result["datapoints"]))
        return results

    def queryLast(self, endpoint, testUrl, tps_from="-30d", tps_to=None, format='json'):
        results = self.query(endpoint, testUrl, tps_from=tps_from, tps_to=tps_to, format=format)
        for result in results:
            if(result.get("datapoints")):
                result["datapoints"] = result["datapoints"][-1:]
        return results
    
    def queryLastValue(self, endpoint, testUrl, tps_from="-30d", tps_to=None, format='json'):
        return self.query(endpoint, testUrl, tps_from=tps_from, tps_to=tps_to, format=format)[0]["datapoints"][-1][0]


