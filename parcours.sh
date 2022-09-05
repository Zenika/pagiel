#!/bin/bash
sourceCodeRepository=$1

source ./scripts/parcours-common.sh

#ensure to have only essential container started all time
trap clear EXIT

# main loop 
process () {
    startup
    sleep 20 #smartwatt and hwpc sensor can take a long time to boot
    converturl
    tests
    testsrobot
    testEcoCode $sourceCodeRepository
    report
    sleep 15
}

process