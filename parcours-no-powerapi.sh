#!/bin/bash

source ./scripts/parcours-common.sh

# main loop 
process () {
    converturl
    tests
    report
}

process