# Ce script va lancer le process de test sur chacun des commit entre les tags "demo start" et "demo-end", avec un délai de 15 minutes entre chaque test

trap clear EXIT

clear(){
    git checkout demo
    docker-compose stop smartwatts
    docker-compose stop powerapi-hwpc-sensor
    docker-compose stop chrome
    docker-compose stop selenium-hub
    echo "container stopped"
}

process() {
    echo "building demo"
    docker-compose up --build -d demo
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
    echo "run YellowLabTools"
    docker-compose --profile test up --abort-on-container-exit --exit-code-from yellowlabtools yellowlabtools 
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "YellowLabTools failed"
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
}

git checkout demo-end
nbcommit=$(($(git rev-list demo-start..demo-end --count) + 1))
commitList=$(git log --reverse --pretty=oneline -$nbcommit)
errCode=0
echo "starting sensors"
docker-compose --profile preconso up -d
echo "waiting for sensor" #smartwatt and hwpc sensor can take a long time to boot
sleep 20
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

while IFS= read -r commit; do
    commithash="${commit:0:7}"
    echo 
    git checkout $commithash
    sleep 2
    process
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "commit $commithash failed"
        exit 1
    fi
    echo "$commit tested"
    date +%T
    sleep 900
done <<< "$commitList"

echo 'ended'

clear 