
# stop container only usefull for the test
clear () {
    docker-compose stop smartwatts
    docker-compose stop powerapi-hwpc-sensor
    docker-compose stop chrome
    docker-compose stop selenium-hub
}

# start smartwatt ans selenium
startup() {
    echo "Démarrage de PowerAPI"
    docker-compose --profile preconso up -d
}

converturl() {
    errCode=0
    echo "Convertion du fichier d'entrée"
    # this allow to have a potential error wode from the container, duplicate container name isn't a typo
    # container are started without -d option to ensure that the next one start after the end of the previous
    docker-compose --profile pretest up --abort-on-container-exit --exit-code-from url-converter url-converter
    #stopping process if case of error
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "Echec de la convertion du fichier d'entrée"
        exit $errCode
    fi
}

# main test loop
tests() {
    errCode=0
    echo "Démarrage de GreenIT Analysis"
    docker-compose --profile test up --abort-on-container-exit --exit-code-from eco-index eco-index
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "Erreur lors de GreenIT Analysis"
        exit $errCode
    fi
    echo "Démarrage de Sitespeed"
    docker-compose --profile test up --abort-on-container-exit --exit-code-from sitespeed sitespeed 
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "Erreur lors de Sitespeed"
        exit $errCode
    fi
    echo "Démarrage de YellowLabTools"
    docker-compose --profile test up --abort-on-container-exit --exit-code-from yellowlabtools yellowlabtools 
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "Erreur lors de YellowLabTools"
        exit $errCode
    fi
}

testsrobot() {
    echo "Démarrage des tests Robot Framework"
    docker-compose --profile conso up --abort-on-container-exit --exit-code-from robot-chrome-test robot-chrome-test
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        echo "Erreurs lors des tests de Robot Framework"
        exit $errCode
    fi
}

report() {
    # Démarrage du conteneur de génération de raport Junit
    echo "Début de la génération du raport Junit"
    docker-compose --profile report up --abort-on-container-exit --exit-code-from report report
    errCode=$?
    if [ $errCode -ne 0 ];
    then
        exit $errCode
    fi
    echo "Rapport Junit rédigé"
}