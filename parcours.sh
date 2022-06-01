#!/bin/bash

#ensure to have only essential container started all time
trap clear EXIT

clear () {
    docker-compose stop smartwatts
    docker-compose stop powerapi-hwpc-sensor
    docker-compose stop chrome
    docker-compose stop selenium-hub
    echo "container stopped"
}

process () {
    errCode=0
    echo "starting sensors"
    docker-compose --profile preconso up -d
    echo "waiting for sensor" #smartwatt and hwpc sensor can take a long time to boot
    sleep 20
    echo "run url-converter"
    # this allow to have a potential error wode from the container, duplicate container name isn't a typo
    # container are started without -d option to ensure that the next one start after the end of the previous
    docker-compose --profile pretest up --abort-on-container-exit --exit-code-from url-converter url-converter
    #stopping process if case of error
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