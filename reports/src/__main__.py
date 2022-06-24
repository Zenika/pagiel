import os
import xml.etree.cElementTree as ET
from datetime import datetime

import yaml

from graphite import GraphiteClient
from influxdb import InfluxClient
from exceptions import ComparatorException, CategoryException, IndicatorException

def loadDataFiles(src):
    with open(src) as indicsYaml:
        return yaml.load(indicsYaml, Loader=yaml.FullLoader)

def testIndicator(test, indicator, comparison, indicatorsCategoryDict):
    if not indicatorsCategoryDict.get(indicator):
        raise IndicatorException(indicator)

    print(f"--- Indicateur {indicator} ---")

    res = {}

    indicatorValue = None
    if(indicatorsCategoryDict[indicator].get("influxMeasurement")):
        indicatorValue = influxClient.queryLastValue(indicatorsCategoryDict[indicator]["influxMeasurement"], indicator, test["name"])
    else:
        indicatorValue = graphiteClient.queryLastValue(indicatorsCategoryDict[indicator]["graphiteAddress"], test["url"])

    for comparisonMode, expectedValue in comparison.items():
        match comparisonMode:
            case ">":
                res[f"{comparisonMode} {str(expectedValue)}"] = {"result": indicatorValue > expectedValue, "expected": expectedValue, "value": indicatorValue}
            case ">=":
                res[f"{comparisonMode} {str(expectedValue)}"] = {"result": indicatorValue >= expectedValue, "expected": expectedValue, "value": indicatorValue}
            case "<":
                res[f"{comparisonMode} {str(expectedValue)}"] = {"result": indicatorValue < expectedValue, "expected": expectedValue, "value": indicatorValue}
            case "<=":
                res[f"{comparisonMode} {str(expectedValue)}"] = {"result": indicatorValue <= expectedValue, "expected": expectedValue, "value": indicatorValue}
            case "==":
                res[f"{comparisonMode} {str(expectedValue)}"] = {"result": indicatorValue == expectedValue, "expected": expectedValue, "value": indicatorValue}
            case "!=":
                res[f"{comparisonMode} {str(expectedValue)}"] = {"result": indicatorValue != expectedValue, "expected": expectedValue, "value": indicatorValue}
            case _:
                raise ComparatorException(comparisonMode)
        
        print(f"{indicatorValue} {comparisonMode} {expectedValue}")

    return res

def testCategory(test, category, indicators):
    if not indicatorDict.get(category):
        raise CategoryException(category)
    
    print(f"--- Catégorie {category} ---")
    res = {}

    for indicator, comparisons in indicators.items():
        res[indicator] = testIndicator(test, indicator, comparisons, indicatorDict[category])

    return res

def testUrlList(urlList):
    res = {}
    for test in urlList:
        if test.get("require"):
            print(f"--- Vérifications pour {test['name']} ---")
            res[test['name']] = {}

            for category, indicators in test["require"].items():
                res[test['name']][category] = testCategory(test, category, indicators)
    
    return res

def generateTestCaseXml(parent, indicator, comparison, result):
    indicXml = ET.SubElement(parent, "testcase")
    indicXml.set("id", f"{indicator} {comparison}")
    indicXml.set("name", f"{indicator} {comparison}")
    if not result["result"]:
        ET.SubElement(indicXml, "failure").text = f"Valeur attendue : {result['expected']}\nValeur obtenue : {result['value']}"
    return result["result"]

def generateTestSuiteXml(parent, pageName, categoryName, categoryTests):
    pageXml = ET.SubElement(parent, "testsuite")
    pageXml.set("id", f"{pageName}/{categoryName}")
    pageXml.set("name", f"{pageName}/{categoryName}")
    nbPageTest, nbPageFailure = 0, 0
    for indicator, indicTest in categoryTests.items():
        for comparison, result in indicTest.items():
            nbPageTest += 1
            if not generateTestCaseXml(pageXml, indicator, comparison, result):
                nbPageFailure += 1
    pageXml.set("tests", str(nbPageTest))
    pageXml.set("failures", str(nbPageFailure))
    return (nbPageTest, nbPageFailure)

def generateTestsuitesXml(tests):
    testsuites = ET.Element("testsuites")
    testsuites.set("id", "random")
    testsuites.set("name", "eco-test")
    totalTests, totalFailure = 0, 0
    for pageName, pageTests in tests.items():
        for categoryName, categoryTests in pageTests.items():
            nbPageTest, nbPageFailure = generateTestSuiteXml(testsuites, pageName, categoryName, categoryTests)
            totalTests += nbPageTest
            totalFailure += nbPageFailure
    testsuites.set("tests", str(totalTests))
    testsuites.set("failures", str(totalFailure))
    return ET.ElementTree(testsuites)

graphiteClient = GraphiteClient(f'http://{os.environ["GRAPHITE_HOST"]}:{os.environ["GRAPHITE_PORT"]}', (os.environ["GRAPHITE_USERNAME"], os.environ["GRAPHITE_PASSWORD"]))
influxClient = InfluxClient(f'http://{os.environ["INFLUXDB_HOST"]}:{os.environ["INFLUXDB_PORT"]}', org=os.environ["INFLUXDB_ORG_NAME"], token=os.environ["INFLUXDB_TOKEN"], bucket=os.environ["INFLUXDB_BUCKET_NAME"])
indicatorDict = loadDataFiles("/opt/report/src/indics.yaml")

urlList = loadDataFiles("/opt/report/urls.yaml")

resultDict = testUrlList(urlList)

if len(resultDict) > 0:
    timestamp = int(datetime.now().timestamp())

    resultXMl = generateTestsuitesXml(resultDict)
    resultXMl.write("/opt/report/results/report.xml")
    resultXMl.write(f"/opt/report/results/report-{timestamp}.xml")
