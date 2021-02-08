*** Settings ***
Documentation     A resource file with reusable keywords and variables.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported SeleniumLibrary.
Library           SeleniumLibrary

*** Variables ***
${SELENIUM}          http://localhost:4444/wd/hub
${APPLICATION}       http://localhost:8090
${BROWSER}           Chrome
${DELAY}             0
${VALID USER}        demo
${VALID PASSWORD}    mode
${LOGIN URL}         ${APPLICATION}/#/login
${ACCOUNT URL}       ${APPLICATION}/#/account
${WELCOME URL}       ${APPLICATION}/#/
${ERROR URL}         ${APPLICATION}/error.html


*** Keywords ***
Open Browser To Login Page
    Open Browser    ${LOGIN URL}    browser=${BROWSER}    remote_url=${SELENIUM}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}
    Login Page Should Be Open

Go To Login Page
    Go To    ${LOGIN URL}
    Login Page Should Be Open

Submit Credentials
    Click Button    login_button

Login Page Should Be Open
    Location Should Be      ${LOGIN URL}
    Title Should Be         Login

Account Page Should Be Open
    Location Should Be      ${ACCOUNT URL}
    Title Should Be         Account