import sys
import os
import yaml
import shutil

RESOURCE_FILES = "/home/urlconverter/templates/{file}"

GREENIT_INPUT_FILE_ARGS = ["url", "name", "waitForSelector", "waitForXPath", "waitforNavigation", "screenshot", "actions"] 
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

with open(sys.argv[1]) as url_input_file:
    url_list = yaml.load(url_input_file, Loader=yaml.FullLoader)

    with open(sys.argv[2], 'w') as ecoIndexUrlFile:
        documents = yaml.dump([{k: v for k,v in url.items() if k in GREENIT_INPUT_FILE_ARGS} for url in url_list], ecoIndexUrlFile)

    with open(sys.argv[3], 'w') as sitespeed_urls:
        sitespeed_urls.write("\n".join([url["url"] for url in url_list]))

    robot_resources = [ROBOT_RESOURCE_TEMPLATE.format(url=url["url"], name=url["name"], final_url=url.get("final_url", url["url"])) for url in url_list ]
    robot_tests = []
    for url in url_list:
        test = ROBOT_TEST_TEMPLATE.format(name=url["name"], cookie= ROBOT_COOKIE if url.get("cookie_btn") else "")
        if url.get("cookie_btn"):
            test = test.format(cookie_btn=url.get("cookie_btn"))
        robot_tests.append(test)


    robot_resource_file_name = os.path.join(sys.argv[4], "generated-resource.resource")
    shutil.copyfile(RESOURCE_FILES.format(file="resource.resource"), robot_resource_file_name)
    with open(robot_resource_file_name, "a") as robot_resource_file:
        robot_resource_file.write("\n".join(robot_resources))
    
    robot_test_file_name = os.path.join(sys.argv[4], "generated-ping.robot")
    shutil.copyfile(RESOURCE_FILES.format(file="tests.robot"), robot_test_file_name)
    with open(robot_test_file_name, "a") as robot_test_file:
        robot_test_file.write("\n".join(robot_tests))