# function

# help function

help() {
    echo "Process script to start PAGIEL"
    echo ""
    echo "Syntax : ./pagiel.sh [-h|P|G|S|Y|R|F|d|D] [--docker-image|docker-port|docker-compose-file|docker-front-contanier]"
    echo
    echo "-h : print this and exit"
    echo "-P : disable PowerAPI"
    echo "-G : disable GreenIT Analisys CLI"
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
    docker-compose up -d smartwatts
    docker-compose up -d powerapi-hwpc-sensor
}

stopPowerAPI () {
    docker-compose stop smartwatts
    docker-compose stop powerapi-hwpc-sensor
}

# Selenium section
startSelenium () {
    docker-compose up -d chrome
    docker-compose up -d selenium-hub
}

stopSelenium () {
    docker-compose stop chrome
    docker-compose stop selenium-hub
}

# Input file conversion for others tools
convertInput() {
    errCode=0
    echo "Converting input file"
    docker-compose run --rm url-converter
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "Convertion failure"
        exit $errCode
    fi
}

convertInputDocker() {
    echo "Converting docker input file"
    docker-compose run --rm url-converter /home/urlconverter/urls.yaml --localContainerName $1 --localContainerPort $2
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
    docker-compose --file=$1 up -d
}

stopDockerCompose(){ # dockerComposeFile
    docker-compose --file=$1 down
}

# Test function
testGreenITAnalysis() {
    docker-compose run --rm eco-index
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "GreenIT Analysis failure"
        exit $errCode
    fi
}

testSitespeed() {
    docker-compose run --rm sitespeed 
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "Sitespeed failure"
        exit $errCode
    fi
}

testYellowLabTools() {
    docker-compose --profile test up --abort-on-container-exit --exit-code-from yellowlabtools yellowlabtools 
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "YellowLabTools failure"
        exit $errCode
    fi
}

testsrobot() {
    docker-compose run --rm robot-chrome-test
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "Robot Framework failure"
        exit $errCode
    fi
}

makeReport() {
    # Démarrage du conteneur de génération de raport
    echo "Start report generation"
    docker-compose run --rm report
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

currentDir=$(pwd | tr '[:upper:]' '[:lower:]')
currentDir=${currentDir##*/}

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
dockerNetwork=${currentDir}_default

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
      --docker-port) dockerPort=$2 && shift;;
      --docker-front-container) dockerContainerName=$2 && shift;;
      --docker-compose-file) dockerComposeFile=$2 && shift;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
   shift
done

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
    testsrobot
fi

if [ "$doReport" = true ] ; then
    makeReport
fi

