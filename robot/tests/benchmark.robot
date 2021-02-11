*** Settings ***
Documentation     A test suite with a single test for valid login.
...
...               This test has a workflow that is created using keywords in
...               the imported resource file.
Resource          resource.robot

*** Test Cases ***
LowTechMazine
    Open Browser To LowTechMagazine
    sleep  5s
    Click Link High-Tech Problems
    sleep  5s
    [Teardown]    Close Browser

Amazon
    Open Browser To Amazon
    sleep  5s
    Click Link AmazonBasics
    sleep  5s
    [Teardown]    Close Browser

Nike
    Open Browser To Nike
    sleep  5s
    Click Link Homme
    sleep  5s
    [Teardown]    Close Browser