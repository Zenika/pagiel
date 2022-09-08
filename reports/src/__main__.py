from reportGenerator import main, GraphiteClient, InfluxClient, SonarClient, load_json_data_file, load_yaml_data_file
from sys import exit
from os import environ

if __name__ == "__main__":
    GRAPHITE_CLIENT = GraphiteClient(f'http://{environ["GRAPHITE_HOST"]}:{environ["GRAPHITE_PORT"]}', (environ["GRAPHITE_USERNAME"], environ["GRAPHITE_PASSWORD"]))
    INFLUXDB_CLIENT = InfluxClient(f'http://{environ["INFLUXDB_HOST"]}:{environ["INFLUXDB_PORT"]}', org=environ["INFLUXDB_ORG_NAME"], token=environ["INFLUXDB_TOKEN"], bucket=environ["INFLUXDB_BUCKET_NAME"])
    SONAR_CLIENT = SonarClient(f'http://{environ["SONAR_HOST"]}:{environ["SONAR_PORT"]}', environ["SONAR_PROJECT_KEY"], {"login": environ["SONAR_USERNAME"], "password": environ["SONAR_PASSWORD"]})
    INDICATORS_BY_CATEGORY = load_yaml_data_file("/opt/report/src/indics.yaml")
    OFFENDERS = load_json_data_file("/opt/report/offenders/result.json")

    if(exit_code_variable := environ.get("EXIT_CODE_FAIL")):
        try:
            exit_code_fail = int(exit_code_variable)
        except ValueError:
            exit_code_fail = 0
    try: 
        some_failed = main(GRAPHITE_CLIENT, INFLUXDB_CLIENT, SONAR_CLIENT, INDICATORS_BY_CATEGORY, OFFENDERS)
        exit(0 if not some_failed else exit_code_fail)
    except Exception as e:
        print(str(e))
        exit(1)
