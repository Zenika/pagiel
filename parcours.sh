#!/bin/bash

trap 'docker-compose stop smartwatts && docker-compose stop powerapi-hwpc-sensor && docker-compose stop chrome && docker-compose stop selenium-hub && echo "containers stopped"' EXIT

errCode=0

process () {
    echo "start test"
    echo "démarage des sensors"
    docker-compose --profile preconso up -d
    echo "run url-converter"
    docker-compose --profile pretest up --abort-on-container-exit --exit-code-from url-converter url-converter
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "url failed"
        exit 1
    else
        echo "url fonct"
    fi
    echo "run eco-index"
    docker-compose --profile test up --abort-on-container-exit --exit-code-from eco-index eco-index
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "eco-index failed"
        exit 1
    fi
    echo "run sitespeed"
    docker-compose --profile test up --abort-on-container-exit --exit-code-from sitespeed sitespeed 
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "sitespeed failed"
        exit 1
    fi
    echo "run robot-chrome-test"
    docker-compose --profile conso up --abort-on-container-exit --exit-code-from robot-chrome-test robot-chrome-test
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "robot-framework failed"
        exit 1
    fi
    echo "fin des tests"
}

process