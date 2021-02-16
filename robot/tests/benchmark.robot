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
    sleep  5s
    Click Button    Connexion
    Account Page Should Be Open
    sleep  5s
    [Teardown]    Close Browser

LowTechMazine
    sleep  30s
    Open Browser To LowTechMagazine
    sleep  5s
    Click Link      High-Tech Problems
    sleep  5s
    [Teardown]    Close Browser

Amazon
    sleep  30s
    Open Browser To Amazon
    sleep  5s
    Click Link      AmazonBasics
    sleep  5s
    [Teardown]    Close Browser

Nike
    sleep  30s
    Open Browser To Nike
    sleep  5s
    Click Link      Homme
    sleep  5s
    [Teardown]    Close Browser

Arkea
    sleep  30s
    Open Browser To Arkea
    sleep  5s
    Click Link      About us
    sleep  5s
    [Teardown]    Close Browser

Valid Login
    sleep  30s
    Open Browser To Login Page
    Login Page Should Be Open
    sleep  5s
    Click Button    Connexion
    Account Page Should Be Open
    sleep  30s
    [Teardown]    Close Browser
