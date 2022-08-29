from unittest import TestCase, main as test_main

from reportGenerator import load_json_data_file, load_yaml_data_file, JunitReportGenerator

OFFENDERS = load_json_data_file("/opt/report/src/testfiles/test-result.json")
INDICATORS_BY_CATEGORY = load_yaml_data_file("/opt/report/src/indics.yaml")


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


if __name__ == '__main__':
    test_main()