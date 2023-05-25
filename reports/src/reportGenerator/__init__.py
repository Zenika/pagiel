from typing import Any, Dict
from xml.etree.cElementTree import SubElement, Element, ElementTree
from json import load as loadJson
import csv
from datetime import datetime
from collections import defaultdict
from os import environ
import argparse
import shutil
import os

from yaml import load as yamlload, FullLoader

from reportGenerator.influxdb import InfluxClient
from reportGenerator.exceptions import ComparatorException, CategoryException, IndicatorException, MissingComparison

def load_yaml_data_file(src: str) -> Any:
    with open(src, encoding="utf8") as indicsYaml:
        return yamlload(indicsYaml, Loader=FullLoader)

def load_json_data_file(src: str) -> Any:
    with open(src, encoding="utf8") as offenderJSON:
        return loadJson(offenderJSON)

class IndicatorComparator:
    def __init__(self, influxdb_client: InfluxClient, indicators_by_category: dict) -> None:
        self.influxdb_client = influxdb_client
        self.indicators_by_category = indicators_by_category
        self.some_failed = False

    def compare(self, comparison_mode: str, expected_value: Any, indicator_value: Any) -> dict:
        match comparison_mode:
            case ">":
                return {"result": indicator_value > expected_value, "expected": expected_value, "value": indicator_value}
            case ">=":
                return {"result": indicator_value >= expected_value, "expected": expected_value, "value": indicator_value}
            case "<":
                return {"result": indicator_value < expected_value, "expected": expected_value, "value": indicator_value}
            case "<=":
                return {"result": indicator_value <= expected_value, "expected": expected_value, "value": indicator_value}
            case "==":
                return {"result": indicator_value == expected_value, "expected": expected_value, "value": indicator_value}
            case "!=":
                return {"result": indicator_value != expected_value, "expected": expected_value, "value": indicator_value}
            case _:
                raise ComparatorException(comparison_mode)

    def get_indicator_value(self, indicator_key: str, indicator: dict, test: dict) -> Any:
        """
            Query database for last value
        """
        return self.influxdb_client.query_last_value(indicator["Measurement"], indicator["Field"], test["name"], indicator["Tags"].copy())

    def test_indicator(self, test: dict, indicator: str, comparisons: dict, indicators_details: dict) -> dict:
        """
            test all assertion on an indicator, return dict with result
        """

        print(f"--- Indicateur {indicator} ---")

        res = defaultdict(dict)

        indicator_value = self.get_indicator_value(indicator, indicators_details, test)

        for comparison_mode, expected_value in comparisons.items():
            res[f"{comparison_mode} {expected_value}"] = self.compare(comparison_mode, expected_value, indicator_value)
            
            if not res[f"{comparison_mode} {expected_value}"]["result"]:
                if path := indicators_details.get("path", ""):
                    res[f"{comparison_mode} {expected_value}"]["path"] = path
                self.some_failed = True

            print(f"{indicator_value} {comparison_mode} {expected_value}")
        return res

    def test_category(self, test: dict, category: str, indicators: dict) -> dict:
        if category not in self.indicators_by_category:
            raise CategoryException(category)
        
        print(f"--- Catégorie {category} ---")
        res = defaultdict(dict)

        for indicator, comparisons in indicators.items():
            if not comparisons:
                raise MissingComparison(indicator)
            if indicator not in self.indicators_by_category[category]:
                raise IndicatorException(indicator)
            res[indicator] = self.test_indicator(test, indicator, comparisons, self.indicators_by_category[category][indicator])

        return res

    def test_url_list(self, url_list: list) -> dict:
        res = defaultdict(dict)
        for test in url_list:
            if test.get("require"):
                print(f"--- Vérifications pour {test['name']} ---")

                for category, indicators in test["require"].items():
                    res[test['name']][category] = self.test_category(test, category, indicators)

        return res

class JunitReportGenerator:
    def __init__(self, offenders: list) -> None:
        self.offenders = offenders

    def find_offenders_in_list(self, test_name: str) -> dict:
        return next((offender for offender in self.offenders if offender["name"] == test_name), None)

    def display_offender(self, offender_value: Any, path: list) -> str:
        """
            Json path recursive implementation
        """
        if not offender_value:
            return ""

        if len(path) == 0:
            return str(offender_value)

        key, *remaining_path = path

        if key == "*":
            def map_display_offender(value):
                return self.display_offender(value, remaining_path)
            if type(offender_value) == dict:
                offender_value = offender_value.values()
            return ",\n".join(map_display_offender(value) for value in offender_value)
        
        if "+" in key:
            key1, key2 = key.split("+")
            return f"{self.display_offender(offender_value[key1], [])} {self.display_offender(offender_value[key2], remaining_path)}"

        else:
            return self.display_offender(offender_value[key], remaining_path)

    def get_offender_for(self, test_name: str, indicator: str, path: list) -> str:
        offender_dict = self.find_offenders_in_list(test_name)

        if not offender_dict:
            return ""
        return self.display_offender(offender_dict["offenders"].get(indicator, None), path)

    def generate_test_case_xml(self, parent: Element, testsuite: str, indicator: str, comparison: str, result: dict, test_name: str) -> bool:
        """
            Generate XML testcase and failure. Return bool with assetion result
        """
        indic_xml = SubElement(parent, "testcase")
        indic_xml.set("id", f"{indicator} {comparison}")
        indic_xml.set("name", f"{indicator} {comparison}")
        indic_xml.set("classname", f"{testsuite}")
        if not result["result"]:
            if result.get("path"):
                offenders = self.get_offender_for(test_name, indicator, result["path"].split("."))
            else: 
                offenders = ""
            SubElement(indic_xml, "failure").text = f"Valeur attendue : {result['expected']}\nValeur obtenue : {result['value']}\n{offenders}"
        return result["result"]

    def generate_testsuite_xml(self, parent: Element, test_name: str, category_name: str, category_tests: dict) -> tuple:
        """
            Generate testsuite junit tag
        """
        page_xml = SubElement(parent, "testsuite")
        testsuite_name = f"{test_name}.{category_name}"
        page_xml.set("id", testsuite_name)
        page_xml.set("name", testsuite_name)
        nb_page_test, nb_page_failure = 0, 0
        for indicator, indic_test in category_tests.items():
            for comparison, result in indic_test.items():
                nb_page_test += 1
                if not self.generate_test_case_xml(page_xml, testsuite_name, indicator, comparison, result, test_name):
                    nb_page_failure += 1
        page_xml.set("tests", str(nb_page_test))
        page_xml.set("failures", str(nb_page_failure))
        return (nb_page_test, nb_page_failure)

    def generate_testsuites_xml(self, tests: dict, output_file: str,timestamp: int) -> ElementTree:
        """
            Generate testsuites junit tag
        """
        testsuites = Element("testsuites")
        testsuites.set("id", "PAGIEL-test")
        testsuites.set("name", "PAGIEL-test")
        total_tests, total_failure = 0, 0
        for page_name, page_tests in tests.items():
            for category_name, category_tests in page_tests.items():
                nb_page_test, nb_page_failure = self.generate_testsuite_xml(testsuites, page_name, category_name, category_tests)
                total_tests += nb_page_test
                total_failure += nb_page_failure
        testsuites.set("tests", str(total_tests))
        testsuites.set("failures", str(total_failure))
        result_xml = ElementTree(testsuites)
        result_xml.write(output_file)
        result_xml.write(f"/opt/report/results/report-{timestamp}.xml")
        print("test results written to /opt/report/results/report.xml")

    def export_to_csv(self, comparison_results: dict, output_file: str, timestamp: int):
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Test Name', 'Category', 'Indicator', 'Comparison', 'Expected', 'Value', 'Offenders', 'Result'])
            for test_name, test_results in comparison_results.items():
                for category_name, category_results in test_results.items():
                    for indicator, indic_results in category_results.items():
                        for comparison, result in indic_results.items():
                            row = [test_name, category_name, indicator, comparison, result['expected'], result['value'], result.get('path', ''), result['result']]
                            writer.writerow(row)
        dst_file = f'/opt/report/results/report-{timestamp}.csv'
        shutil.copy(output_file, dst_file)
        print(f"Exported results to {output_file} in CSV format.")

def main(influxdb_client: InfluxClient, indicators_by_category: dict, offenders: list) -> bool:
    url_list = load_yaml_data_file("/opt/report/urls.yaml")
    indicator_comparator = IndicatorComparator(influxdb_client, indicators_by_category)
    comparison_results = indicator_comparator.test_url_list(url_list)
    if len(comparison_results) > 0:
        timestamp = int(datetime.now().timestamp())
        junit_generator = JunitReportGenerator(offenders)
        if(environ["REPORT_FORMAT"] == "csv"):    
            junit_generator.export_to_csv(comparison_results,"/opt/report/results/report.csv",timestamp)
        else:
            junit_generator.generate_testsuites_xml(comparison_results,"/opt/report/results/report.csv",timestamp)

            
    return indicator_comparator.some_failed
