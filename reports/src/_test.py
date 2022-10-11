from unittest import TestCase, main as test_main
from os import environ

from reportGenerator import load_json_data_file, load_yaml_data_file, JunitReportGenerator, InfluxClient

OFFENDERS = load_json_data_file("/opt/report/src/testfiles/test-result.json")
INDICATORS_BY_CATEGORY = load_yaml_data_file("/opt/report/src/indics.yaml")
URLS_TEST = load_yaml_data_file("/opt/report/src/testfiles/test-urls.yaml")


class TestOffenderPath(TestCase):
    def __init__(self, method_name: str = ...) -> None:
        super().__init__(method_name)
        self.junit_generator = JunitReportGenerator(OFFENDERS)

    def test_paths(self):
        """
        Test that existing path work
        """
        for category, category_dict in INDICATORS_BY_CATEGORY.items():
            for indicator, indicator_detail in category_dict.items():
                if(indicator_detail.get("path")):
                    # print(f"{category} {indicator} {indicator_detail.get('path')}")
                    self.assertNotEqual(self.junit_generator.get_offender_for("Docker-index", indicator, indicator_detail["path"].split(".")), "")


class TestInfluxDB(TestCase):
    def __init__(self, method_name: str = ...) -> None:
        super().__init__(method_name)
        self.influxdb_client = InfluxClient(f'http://{environ["INFLUXDB_HOST"]}:{environ["INFLUXDB_PORT"]}', 
            org=environ["INFLUXDB_ORG_NAME"], token=environ["INFLUXDB_TOKEN"], bucket=environ["INFLUXDB_BUCKET_NAME"])
        
    def test_influxdb(self):
        """
        Test every endpoint from InfluxDB
        """
        for category, category_dict in INDICATORS_BY_CATEGORY.items():
            for indicator, indicator_detail in category_dict.items():
                query_result = self.influxdb_client.query_last(indicator_detail["Measurement"], 
                                indicator_detail["Field"], 
                                URLS_TEST[0]["name"], 
                                indicator_detail["Tags"].copy())
                if(len(query_result) == 0):
                    print(indicator)
                self.assertNotEqual(len(query_result), 0)

if __name__ == '__main__':
    test_main()