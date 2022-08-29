from datetime import datetime, timedelta

from influxdb_client import InfluxDBClient

def get_influxdb_timestamp(date):
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
        page_tag = "pageName" if measurement == "eco_index" else "name"
        flux_query = f'from(bucket: "{self.bucket}") |> range(start: {get_influxdb_timestamp(yes)}, stop: {get_influxdb_timestamp(now)}) |> filter(fn: (r) => r._measurement == "{measurement}" and r.{page_tag} == "{page}" and r._field == "{field}") {"|> last()" if last else ""}'
        return [row for table in self.query_api.query(flux_query) for row in table.records]
    
    def query_last(self, measurement, field, page):
        return self.query(measurement, field, page, True)
    
    def query_last_value(self, measurement, field, page):
        return self.query_last(measurement, field, page)[0]["_value"]

    def query_fields(self, measurement, page):
        flux_query = f"""from(bucket: "db0")
  |> range(start: 1654073155, stop: 1654677955)
  |> filter(fn: (r) => r["_measurement"] == "{measurement}")
  |> filter(fn: (r) => r["name"] == "{page}")
  |> yield(name: "last")
  """
        return self.query_api.query(flux_query)