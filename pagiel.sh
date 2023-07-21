
# sets the docker compose command used to launch the Docker stacks
docker_compose_cmd=${DOCKER_COMPOSE_CMD:-docker compose}
docker_compose_options=${DOCKER_COMPOSE_OPTIONS}
docker_compose_pagiel="$docker_compose_cmd $docker_compose_options"
exportFormat="xml" 

# function

# help function

help() {
    echo "Process script to start PAGIEL"
    echo ""
    echo "This script uses the 'docker compose' command by default to launch the tools."
    echo "If you want to use 'docker-compose', run the script as follows:"
    echo "DOCKER_COMPOSE_CMD=""docker-compose"" bash pagiel.sh [...]"
    echo "Command used to call Docker compose: '${docker_compose_cmd}'."
    echo ""
    echo "Syntax : ./pagiel.sh [-h|P|G|S|Y|R|F|d|D] [--docker-image|docker-port|docker-compose-file|docker-front-contanier]"
    echo
    echo "-h : print this and exit"
    echo "-P : disable PowerAPI"
    echo "-G : disable GreenIT Analysis CLI"
    echo "-S : disable Sitespeed"
    echo "-Y : disable Yellow Lab Tools"
    echo "-R : disable report generation"
    echo "-F : disable Robot Framework"
    echo "-d : setup test for an image"
    echo "-D : setup test for a docker-compose"
    echo "--docker-image : image to test (mandatory with -d)"
    echo "--docker-port : port of the website (default 80)"
    echo "--docker-compose-file : docker-compose file to test (mandatory with -D)"
    echo "--docker-front-container : name of the container exposing the website (default : test-container)"
}

# Powerapi section

startPowerAPI () {
    ${docker_compose_pagiel} up -d smartwatts
    ${docker_compose_pagiel} up -d powerapi-hwpc-sensor
}

stopPowerAPI () {
    ${docker_compose_pagiel} stop smartwatts
    ${docker_compose_pagiel} stop powerapi-hwpc-sensor
}

# Selenium section
startSelenium () {
    ${docker_compose_pagiel} up -d chrome
    ${docker_compose_pagiel} up -d selenium-hub
}

stopSelenium () {
    ${docker_compose_pagiel} stop chrome
    ${docker_compose_pagiel} stop selenium-hub
}

# Input file conversion for others tools
convertInput() {
    errCode=0
    echo "Converting input file"
    ${docker_compose_pagiel} run --rm url-converter
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "Convertion failure"
        exit $errCode
    fi
}

convertInputDocker() {
    echo "Converting docker input file"
    ${docker_compose_pagiel} run --rm url-converter /home/urlconverter/urls.yaml --localContainerName $1 --localContainerPort $2
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "Conversion failure"
        exit $errCode
    fi
}

# Docker section

# Single image 
startContainer() { # dockerImage containerName dockerNetwork
    docker pull $1
    docker container run --rm -d --name $2 --network $3 $1
}

stopContainer() { # dockerImage containerName
    docker container stop $2
    docker image rm -f $1
}

# docker-compose
startDockerCompose(){ # dockerComposeFile dockerNetwork
    python3 ./scripts/docker-compose-conf.py $1 $2
    ${docker_compose_cmd} --file=$1 up -d
}

stopDockerCompose(){ # dockerComposeFile
    ${docker_compose_cmd} --file=$1 down
}

# Test function
testGreenITAnalysis() {
    ${docker_compose_pagiel} run --rm eco-index
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "GreenIT Analysis failure"
        exit $errCode
    fi
}

testSitespeed() {
    ${docker_compose_pagiel} run --rm sitespeed 
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "Sitespeed failure"
        exit $errCode
    fi
}

testYellowLabTools() {
    ${docker_compose_pagiel} --profile test up --abort-on-container-exit --exit-code-from yellowlabtools yellowlabtools 
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "YellowLabTools failure"
        exit $errCode
    fi
}

testsrobot() {
    ${docker_compose_pagiel} run --rm robot-chrome-test
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "Robot Framework failure"
        exit $errCode
    fi
}

makeReport() {
    # Démarrage du conteneur de génération de rapport
    ${docker_compose_pagiel} run --rm report
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        exit $errCode
    fi
    echo "Report generated"
}

# cleanup function
cleanup() {
    if [ "$doRobotFramework" = true ] ; then
        stopSelenium
    fi

    if [ "$doPowerAPI" = true ] ; then
        stopPowerAPI
    fi

    if [ "$dockerMode" = "image" ] ; then
        stopContainer $dockerImage $dockerContainerName
    elif [ "$dockerMode" = "compose" ] ; then
        stopDockerCompose $dockerComposeFile
    fi
}

trap cleanup EXIT

doPowerAPI=true
doRobotFramework=true
doGreenItAnalysis=true
doSitespeed=true
doYellowLabTool=true
doReport=true
dockerMode=default
dockerContainerName=test-container
dockerPort=80
dockerComposeFile=""
dockerNetwork=pagiel

OPTS=$(getopt \
    --options "hPGSYRFdD" \
    --longoptions "docker-image:,docker-port:,docker-front-container:,docker-compose-file:" \
    --name "$(basename "$0")" \
    -- "$@"
)

eval set -- $OPTS
while [[ $# > 0 ]]; do
   case ${1} in
      -h) # display Help
         help
         doPowerAPI=false
         doRobotFramework=false
         exit;;
      -P) doPowerAPI=false;;
      -G) doGreenItAnalysis=false;;
      -S) doSitespeed=false;;
      -Y) doYellowLabTool=false;;
      -F) doRobotFramework=false;;
      -R) doReport=false;;
      -d) dockerMode=image;;
      -D) dockerMode=compose;;
      --docker-image) dockerImage=$2 && shift;;
      --export-format) exportFormat=$2 && shift;;
      --docker-port) dockerPort=$2 && shift;;
      --docker-front-container) dockerContainerName=$2 && shift;;
      --docker-compose-file) dockerComposeFile=$2 && shift;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
   shift
done

if [ "$exportFormat" = "csv" ] ; then
    exportFormat="csv"
fi
if [ "$doPowerAPI" = true ] ; then
    startPowerAPI
fi

if [ "$dockerMode" = "default" ] ; then
    convertInput
else
    convertInputDocker $dockerContainerName $dockerPort
    if [ "$dockerMode" = "image" ] ; then
        startContainer $dockerImage $dockerContainerName $dockerNetwork
    else
        startDockerCompose $dockerComposeFile $dockerNetwork
    fi
fi

if [ "$doGreenItAnalysis" = true ] ; then
    testGreenITAnalysis
fi

if [ "$doSitespeed" = true ] ; then
    testSitespeed
fi

if [ "$doYellowLabTool" = true ] ; then
    testYellowLabTools
fi

if [ "$doRobotFramework" = true ] ; then
    startSelenium
    sleep 1 # selenium needs 1s before robotframework can query it
    testsrobot
fi

if [ "$doReport" = true ] ; then
    makeReport
fi

