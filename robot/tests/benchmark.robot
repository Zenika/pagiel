*** Settings ***
Documentation     A test suite with a single test for valid login.
...
...               This test has a workflow that is created using keywords in
...               the imported resource file.
Resource          resource.robot

*** Test Cases ***
LowTechMazine
    Open Browser https://www.lowtechmagazine.com/ browser=Chrome remote_url=http://selenium-hub:4444/wd/hub
    sleep  5s
    Click Link High-Tech Problems
    sleep  5s
    [Teardown]    Close Browser

Amazon
    Open Browser https://www.amazon.fr/ browser=Chrome remote_url=http://selenium-hub:4444/wd/hub
    sleep  5s
    Click Link AmazonBasics
    sleep  5s
    [Teardown]    Close Browser

Nike
    Open Browser https://www.nike.com/fr/ browser=Chrome remote_url=http://selenium-hub:4444/wd/hub
    sleep  5s
    Click Link Homme
    sleep  5s
    [Teardown]    Close Browser