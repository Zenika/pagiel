*** Settings ***
Documentation     A resource file with reusable keywords and variables.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported SeleniumLibrary.
Library           SeleniumLibrary

*** Variables ***
${SELENIUM}          http://selenium-hub:4444/wd/hub
${BROWSER}           Chrome
${DELAY}             0


*** Keywords ***
