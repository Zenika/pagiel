from unittest import TestCase, main as test_main

from reportGenerator import load_json_data_file, load_yaml_data_file, JunitReportGenerator, IndicatorComparator, CategoryException, IndicatorException, MissingComparison, ComparatorException

URL_LIST = load_yaml_data_file("/opt/report/src/testfiles/test-urls.yaml")
OFFENDERS = load_json_data_file("/opt/report/src/testfiles/test-result.json")
INDICATORS_BY_CATEGORY = load_yaml_data_file("/opt/report/src/indics.yaml")


class TestOffenderPath(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.junit_generator = JunitReportGenerator(OFFENDERS)

    def test_paths(self):
        """
        Test that existing path work
        """
        for category, category_dict in INDICATORS_BY_CATEGORY.items():
            for indicator, indicator_detail in category_dict.items():
                if(indicator_detail.get("path")):
                    # print(f"{category} {indicator} {indicator_detail.get('path')}")
                    self.assertNotEqual(self.junit_generator.get_offender_for("Docker-index", indicator, indicator_detail["path"].split(".")), "", "Every offender path should display information")


class TestIndicatorComparison(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.indicator_comparator = IndicatorComparator(DummyDB(), DummyDB(), INDICATORS_BY_CATEGORY)
    
    def test_no_report(self):
        """
        test return empty dict for no require
        """
        self.assertEqual(self.indicator_comparator.test_url_list([URL_LIST[1]]), {}, "An url list with no require should return an empty dict")
    
    def test_report_only(self):
        """
        test return empty dict with only key for test with require key
        """
        result_dict = self.indicator_comparator.test_url_list(URL_LIST[0:1])
        self.assertEqual(len(result_dict.keys()), 1, "There should be only one key if these is only one test with require")
        self.assertEqual(list(result_dict.keys())[0], "Docker-index", "There should be only one key if these is only one test with require")
    
    def test_unkown_category(self):
        self.assertRaises(CategoryException, self.indicator_comparator.test_url_list, [URL_LIST[2]])
    
    def test_unkown_indicator(self):
        self.assertRaises(IndicatorException, self.indicator_comparator.test_category, URL_LIST[3], "eco", URL_LIST[3]["require"]["eco"])
    
    def test_missing_comparison(self):
        self.assertRaises(MissingComparison, self.indicator_comparator.test_category, URL_LIST[3], "eco", URL_LIST[4]["require"]["eco"])
    
    def test_unkown_comparison(self):
        self.assertRaises(ComparatorException, self.indicator_comparator.compare, "##", 42, 42)

class DummyDB:
    def __init__(self) -> None:
        pass

    def queryLastValue(self, *args):
        return 42

if __name__ == '__main__':
    test_main()