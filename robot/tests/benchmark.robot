*** Settings ***
Documentation     A test suite which load different web site.
...
...               This test has a workflow that is created using keywords in
...               the imported resource file.
Resource          resource.robot

*** Test Cases ***

Valid Login
    Open Browser To Login Page
    Login Page Should Be Open
    Click Button    Connexion
    Account Page Should Be Open
    sleep  20s
    [Teardown]    Close Browser

LowTechMazine
    Open Browser To LowTechMagazine
    sleep  5s
    Click Link      High-Tech Problems
    sleep  20s
    [Teardown]    Close Browser

Amazon
    Open Browser To Amazon
    sleep  5s
    Click Link      AmazonBasics
    sleep  20s
    [Teardown]    Close Browser

Nike
    Open Browser To Nike
    sleep  5s
    Click Link      Homme
    sleep  20s
    [Teardown]    Close Browser

Arkea
    Open Browser To Arkea
    sleep  5s
    Click Link      About us
    sleep  20s
    [Teardown]    Close Browser

Valid Login
    Open Browser To Login Page
    Login Page Should Be Open
    Click Button    Connexion
    Account Page Should Be Open
    sleep  20s
    [Teardown]    Close Browser
