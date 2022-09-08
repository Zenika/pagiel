#!/bin/bash
sourceCodeRepository=$1

source ./scripts/parcours-common.sh

# main loop 
process () {
    converturl
    tests
    testEcoCode $sourceCodeRepository
    report
}

process