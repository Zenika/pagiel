from datetime import datetime, timedelta

from influxdb_client import InfluxDBClient

def get_influxdb_timestamp(date):
    return int(date.timestamp())

def generateInfluxQuery(bucket, start, stop, measurement, field, tags=[], last = False):
    tag_query = [f'|> filter(fn: (r) => r["{key}"] == "{value}")' for key, value in tags.items()]
    new_line = "\n"
    return f"""from(bucket: "{bucket}") 
|> range(start: {get_influxdb_timestamp(start)}, stop: {get_influxdb_timestamp(stop)}) 
|> filter(fn: (r) => r._measurement == "{measurement}" and r._field == "{field}")
{new_line.join(tag_query)} 
{"|> last()" if last else ''}"""

class InfluxClient:
    def __init__(self, url, org, token, bucket):
        self.url = url
        self.org = org
        self.token = token
        self.bucket = bucket
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.query_api = self.client.query_api()

    def query(self, measurement: str, field: str, page: str, tags: dict, last:bool=False):
        now = datetime.now()
        yesterday = now + timedelta(days=-1)
        key_to_change = [new_k[0] for new_k in tags.items() if new_k[1] == "$name"]
        if(len(key_to_change) > 0):
            for key in key_to_change:
                tags[key] = page
        flux_query = generateInfluxQuery(self.bucket, yesterday, now, measurement, field, tags=tags, last=last)
        return [row for table in self.query_api.query(flux_query) for row in table.records]
    
    def query_last(self, measurement, field, page, tags):
        return self.query(measurement, field, page, tags, True)
    
    def query_last_value(self, measurement, field, page, tags):
        return self.query_last(measurement, field, page, tags)[0]["_value"]

    def query_fields(self, measurement, page):
        flux_query = f"""from(bucket: "db0")
  |> range(start: 1654073155, stop: 1654677955)
  |> filter(fn: (r) => r["_measurement"] == "{measurement}")
  |> filter(fn: (r) => r["name"] == "{page}")
  |> yield(name: "last")
  """
        return self.query_api.query(flux_query)