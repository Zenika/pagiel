*** Settings ***
Documentation     A test suite which load different web site.
...
...               This test has a workflow that is created using keywords in
...               the imported resource file.
Resource          resource.robot

*** Test Cases ***
LowTechMazine
    Open Browser To LowTechMagazine
    sleep  5s
    Click Link      High-Tech Problems
    sleep  10s
    [Teardown]    Close Browser

Amazon
    Open Browser To Amazon
    sleep  5s
    Click Link      AmazonBasics
    sleep  10s
    [Teardown]    Close Browser

Nike
    Open Browser To Nike
    sleep  5s
    Click Link      Homme
    sleep  10s
    [Teardown]    Close Browser

Arkea
    Open Browser To Arkea
    sleep  5s
    Click Link      About us
    sleep  10s
    [Teardown]    Close Browser

LowTechMazine2
    Open Browser To LowTechMagazine
    sleep  5s
    Click Link      High-Tech Problems
    sleep  10s
    [Teardown]    Close Browser