from reportGenerator import main, InfluxClient, load_json_data_file, load_yaml_data_file
from sys import exit
from os import environ

if __name__ == "__main__":
    INFLUXDB_CLIENT = InfluxClient(f'http://{environ["INFLUXDB_HOST"]}:{environ["INFLUXDB_PORT"]}', org=environ["INFLUXDB_ORG_NAME"], token=environ["INFLUXDB_TOKEN"], bucket=environ["INFLUXDB_BUCKET_NAME"])
    INDICATORS_BY_CATEGORY = load_yaml_data_file("/opt/report/src/indics.yaml")
    OFFENDERS = load_json_data_file("/opt/report/offenders/result.json")

    if(exit_code_variable := environ.get("EXIT_CODE_FAIL")):
        try:
            exit_code_fail = int(exit_code_variable)
        except ValueError:
            exit_code_fail = 0
    try:
        some_failed = main(INFLUXDB_CLIENT, INDICATORS_BY_CATEGORY, OFFENDERS)
        exit(0 if not some_failed else exit_code_fail)
    except Exception as e:
        print(str(e))
        exit(1)
