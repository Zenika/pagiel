from datetime import datetime, timedelta

from influxdb_client import InfluxDBClient

def getInfluxdbTimestamp(date):
    return int(date.timestamp())

class InfluxClient:
    def __init__(self, url, org, token, bucket):
        self.url = url
        self.org = org
        self.token = token
        self.bucket = bucket
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.query_api = self.client.query_api()

    def query(self, measurement, field, page, last=False):
        now = datetime.now()
        yes = now + timedelta(days=-1)
        pageTag = "pageName" if measurement == "eco_index" else "name"
        fluxQuery = f'from(bucket: "{self.bucket}") |> range(start: {getInfluxdbTimestamp(yes)}, stop: {getInfluxdbTimestamp(now)}) |> filter(fn: (r) => r._measurement == "{measurement}" and r.{pageTag} == "{page}" and r._field == "{field}") {"|> last()" if last else ""}'
        # print(fluxQuery)
        return [row for table in self.query_api.query(fluxQuery) for row in table.records]
    
    def queryLast(self, measurement, field, page):
        return self.query(measurement, field, page, True)
    
    def queryLastValue(self, measurement, field, page):
        return self.queryLast(measurement, field, page)[0]["_value"]

    def queryFields(self, measurement, page):
        fluxQuery = f"""from(bucket: "db0")
  |> range(start: 1654073155, stop: 1654677955)
  |> filter(fn: (r) => r["_measurement"] == "{measurement}")
  |> filter(fn: (r) => r["name"] == "{page}")
  |> yield(name: "last")
  """
        return self.query_api.query(fluxQuery)