import os
import yaml
import shutil
import argparse

RESOURCE_FILES = "/home/urlconverter/templates/{file}"

GREENIT_INPUT_FILE_ARGS = ["url", "name", "waitForSelector", "waitForXPath", "waitforNavigation", "screenshot", "actions"] 
YELLOWLABTOOLS_INPUT_FILE_ARGS = ["url", "name", "device"]

ROBOT_RESOURCE_TEMPLATE = """
Open Browser To {name}
    Open Browser    {url}    browser=${{BROWSER}}     remote_url=${{SELENIUM}}
    Maximize Browser Window
    Set Selenium Speed    ${{DELAY}}
    Location Should Be      {final_url}
"""
ROBOT_TEST_TEMPLATE = """
{name}
    Open Browser To {name}
    {cookie}
    sleep  10s
    [Teardown]    Close Browser
    sleep  20s
"""
ROBOT_COOKIE = """
    sleep  5s
    Click Element   {cookie_btn}
"""

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description = "Convert user url request to required file format from container")
    parser.add_argument("inputFile", help="User input file")
    parser.add_argument("--ecoIndexFile", help="file for eco-index", default="/home/urlconverter/results/urls.yaml")
    parser.add_argument("--sitespeedFile", help="file for sitespeed", default="/home/urlconverter/results/urls.txt")
    parser.add_argument("--yellowLabToolsFile", help="file for yellowLab tools", default="/home/urlconverter/results/urls-yellowlabtools.yaml")
    parser.add_argument("--robotFolder", help="folder for robot tests", default="/home/urlconverter/tests/")
    return parser.parse_args()

def filter_dict_list_by_key(dict_list: list, expected_keys: list) -> list:
    return [{key: value for key, value in url.items() if key in expected_keys} for url in dict_list]

def save_yaml_file(file_name: str, url_list: list, expected_keys: list):
    with open(file_name, 'w') as file:
        yaml.dump(filter_dict_list_by_key(url_list, expected_keys), file)

def save_robot_files(robot_folder: str, url_list: list):
    robot_resources = [ROBOT_RESOURCE_TEMPLATE.format(url=url["url"], name=url["name"], final_url=url.get("final_url", url["url"])) for url in url_list]
    robot_tests = []
    for url in url_list:
        test = ROBOT_TEST_TEMPLATE.format(name=url["name"], cookie=ROBOT_COOKIE if url.get("cookie_btn") else "")
        if url.get("cookie_btn"):
            test = test.format(cookie_btn=url.get("cookie_btn"))
        robot_tests.append(test)


    robot_resource_file_name = os.path.join(robot_folder, "generated-resource.resource")
    shutil.copyfile(RESOURCE_FILES.format(file="resource.resource"), robot_resource_file_name)
    with open(robot_resource_file_name, "a") as robot_resource_file:
        robot_resource_file.write("\n".join(robot_resources))
    
    robot_test_file_name = os.path.join(robot_folder, "generated-ping.robot")
    shutil.copyfile(RESOURCE_FILES.format(file="tests.robot"), robot_test_file_name)
    with open(robot_test_file_name, "a") as robot_test_file:
        robot_test_file.write("\n".join(robot_tests))

def process(args):
    with open(args.inputFile) as url_input_file:
        url_list = yaml.load(url_input_file, Loader=yaml.FullLoader)
        
        save_yaml_file(args.ecoIndexFile, url_list, GREENIT_INPUT_FILE_ARGS)
        save_yaml_file(args.yellowLabToolsFile, url_list, YELLOWLABTOOLS_INPUT_FILE_ARGS)

        with open(args.sitespeedFile, 'w') as sitespeed_urls:
            sitespeed_urls.write("\n".join([f'{url["url"]} {url["name"]}' for url in url_list]))

        save_robot_files(args.robotFolder, url_list)

def main():
    args = parse_args()
    process(args)

if __name__ == "__main__":
    main()