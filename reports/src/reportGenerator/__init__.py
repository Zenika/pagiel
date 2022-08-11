from typing import Any, Dict
from xml.etree.cElementTree import SubElement, Element, ElementTree
from json import load as loadJson
from datetime import datetime
from collections import defaultdict

from yaml import load as yamlload, FullLoader

from reportGenerator.graphite import GraphiteClient
from reportGenerator.influxdb import InfluxClient
from reportGenerator.exceptions import ComparatorException, CategoryException, IndicatorException, MissingComparison

def load_yaml_data_file(src: str) -> Any:
    with open(src, encoding="utf8") as indicsYaml:
        return yamlload(indicsYaml, Loader=FullLoader)

def load_json_data_file(src: str) -> Any:
    with open(src, encoding="utf8") as offenderJSON:
        return loadJson(offenderJSON)

class IndicatorComparator:
    def __init__(self, graphite_client: GraphiteClient, influxdb_client: InfluxClient, indicators_by_category: dict) -> None:
        self.graphite_client = graphite_client
        self.influxdb_client = influxdb_client
        self.indicators_by_category = indicators_by_category
        self.some_failed = False

    def compare(self, comparison_mode: str, expected_value: Any, indicator_value: Any) -> bool:
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
        if indicator.get("influxMeasurement"):
            return self.influxdb_client.queryLastValue(indicator["influxMeasurement"], indicator_key, test["name"])
        return self.graphite_client.queryLastValue(indicator["graphiteAddress"], test["url"])

    def test_indicator(self, test: dict, indicator: str, comparisons: dict, indicators_details: dict) -> dict:
        """
            test all assertion on an indicator, return dict with result
        """

        print(f"--- Indicateur {indicator} ---")

        res = defaultdict(dict)

        indicator_value = self.get_indicator_value(indicator, indicators_details, test)

        for comparisonMode, expectedValue in comparisons.items():
            res[f"{comparisonMode} {expectedValue}"] = self.compare(comparisonMode, expectedValue, indicator_value)
            
            if not res[f"{comparisonMode} {expectedValue}"]["result"]:
                if path := indicators_details.get("path", ""):
                    res[f"{comparisonMode} {expectedValue}"]["path"] = path
                self.some_failed = True

            print(f"{indicator_value} {comparisonMode} {expectedValue}")
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

    def generate_testsuites_xml(self, tests: dict) -> ElementTree:
        """
            Generate testsuites junit tag
        """
        testsuites = Element("testsuites")
        testsuites.set("id", "PAGIEL-test")
        testsuites.set("name", "PAGIEL-test")
        totalTests, totalFailure = 0, 0
        for pageName, pageTests in tests.items():
            for categoryName, categoryTests in pageTests.items():
                nbPageTest, nbPageFailure = self.generate_testsuite_xml(testsuites, pageName, categoryName, categoryTests)
                totalTests += nbPageTest
                totalFailure += nbPageFailure
        testsuites.set("tests", str(totalTests))
        testsuites.set("failures", str(totalFailure))
        return ElementTree(testsuites)

def main(graphite_client: GraphiteClient, influxdb_client: InfluxClient, indicators_by_category: dict, offenders: list) -> bool:
    urlList = load_yaml_data_file("/opt/report/urls.yaml")
    indicator_comparator = IndicatorComparator(graphite_client, influxdb_client, indicators_by_category)
    comparison_results = indicator_comparator.test_url_list(urlList)

    if len(comparison_results) > 0:
        timestamp = int(datetime.now().timestamp())

        junit_generator = JunitReportGenerator(offenders)
        resultXMl = junit_generator.generate_testsuites_xml(comparison_results)
        resultXMl.write("/opt/report/results/report.xml")
        resultXMl.write(f"/opt/report/results/report-{timestamp}.xml")
    return indicator_comparator.some_failed
