try:
    from robot.libraries.BuiltIn import BuiltIn
    from robot.api.deco import keyword
    from influxdb_client import InfluxDBClient, Point
    from influxdb_client.client.write_api import SYNCHRONOUS
    from os import environ
    ROBOT = False
except Exception:
    ROBOT = False

class InfluxClient:
    def __init__(self, url, org, token, bucket):
        self.url = url
        self.org = org
        self.token = token
        self.bucket = bucket
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
    
    def write_point(self, test_name):
        p =  Point("robot-tests").tag("testName", test_name).field("multiplier", 1)
        self.write_api.write(bucket = self.bucket, record = p)


instance = InfluxClient(f'http://{environ["INFLUXDB_HOST"]}:{environ["INFLUXDB_PORT"]}', org=environ["INFLUXDB_ORG_NAME"], token=environ["INFLUXDB_TOKEN"], bucket=environ["INFLUXDB_BUCKET_NAME"])

@keyword("INFLUXDB MARK BEGINNING")
def mark_beginning():
    instance.write_point(BuiltIn().get_variable_value("${TEST NAME}"))

@keyword("INFLUXDB MARK END")
def mark_end():
    instance.write_point(BuiltIn().get_variable_value("${TEST NAME}"))