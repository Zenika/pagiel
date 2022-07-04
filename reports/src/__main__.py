from reportGenerator import main, GraphiteClient, InfluxClient, load_json_data_file, load_yaml_data_file
from sys import exit
from os import environ

if __name__ == "__main__":
    GRAPHITE_CLIENT = GraphiteClient(f'http://{environ["GRAPHITE_HOST"]}:{environ["GRAPHITE_PORT"]}', (environ["GRAPHITE_USERNAME"], environ["GRAPHITE_PASSWORD"]))
    INFLUXDB_CLIENT = InfluxClient(f'http://{environ["INFLUXDB_HOST"]}:{environ["INFLUXDB_PORT"]}', org=environ["INFLUXDB_ORG_NAME"], token=environ["INFLUXDB_TOKEN"], bucket=environ["INFLUXDB_BUCKET_NAME"])
    INDICATORS_BY_CATEGORY = load_yaml_data_file("/opt/report/src/indics.yaml")
    OFFENDERS = load_json_data_file("/opt/report/offenders/result.json")

    try: 
        main(GRAPHITE_CLIENT, INFLUXDB_CLIENT, INDICATORS_BY_CATEGORY, OFFENDERS)
    except Exception as e:
        print(str(e))
        exit(1)
