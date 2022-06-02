#!/bin/bash
source ./scripts/parcours-common.sh

#ensure to have only essential container started all time
trap cleanup EXIT

dockerImage=$1
dockerPort=$2
dockerContainerName=test
networkDir=$(pwd | tr '[:upper:]' '[:lower:]')
network=${networkDir##*/}_default

# start local container
startContainer() {
    docker pull $dockerImage
    docker container run --rm -d --name $dockerContainerName --network $network $dockerImage
}

# stop container
stopContainer() {
    docker container stop $dockerContainerName
    docker image rm -f $dockerImage
}

# cleanup function with in trap
cleanup(){
    clear
    stopContainer
}

# main loop
process () {
    startContainer
    startup
    sleep 20 #smartwatt and hwpc sensor can take a long time to boot
    echo "run url-converter"
    # docker-compose run allow to overide the command in the docker-compose.yml
    docker-compose run --rm url-converter /home/urlconverter/urls.yaml --localContainerName $dockerContainerName --localContainerPort $dockerPort
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "url failed"
        exit 1
    fi
    tests
}

process