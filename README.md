
<h1 align="center">Plateforme Automatisée de Génération d'Indicateurs Environnementaux sur le Logiciel (PAGIEL)</h1>
<p>
  <a href="https://github.com/Zenika/pagiel/blob/main/LICENSE" target="_blank">
    <img alt="License: GNU GPL" src="https://img.shields.io/badge/License-GNU GPL-yellow.svg" />
  </a>
</p>

Sommaire
- [Présentation du projet](#présentation-du-projet)
- [Installation](#installation)
  - [Prérequis](#prérequis)
  - [Préparation](#préparation)
  - [Runner gitlab](#runner-gitlab)
- [Utilisation](#utilisation)
  - [Fichier input/urls.yaml](#fichier-inputurlsyaml)
  - [Utilisation seule](#utilisation-seule)
  - [Via les CI/CD](#via-les-cicd)
  - [Rapport au format junit](#rapport-au-format-junit)
- [Outillage](#outillage)
  - [Sitespeed.io](#sitespeedio)
  - [Scoring EcoIndex Green IT](#scoring-ecoindex-green-it-httpwwwecoindexfr)
  - [Yellow Lab Tools](#yellow-lab-tools)
  - [Mesure de la consommation énergétique](#mesure-de-la-consommation-énergétique)
    - [HWPC](#hpwc)
    - [Formula](#formula)
    - [Dashboards](#dashboards)
  - [Selenium & Robot Framework](#selenium--robot-framework)
- [Architecture](#architecture)
 - [Configuration suplémentaire pour l'analyse de la consomation énergétique](#installation-et-configuration-de-lenvironnement-pour-lanalyse-de-la-consommation-énergétique)
- [Cas d'usage à imaginer ou amélioration](#cas-dusage-à-imaginer-ou-améliorations)
- [Licence](#licence)
- [Référence](#références)
  - [Mesure de consomation énergétique](#mesure-de-consommation-énergétique)
    - [RAPL (Running Average Power Limit)](#rapl-running-average-power-limit)
    - [Android](#android)
    - [iOS](#ios)
    - [cgroups](#cgroups)
    - [PowerAPI](#power-api)
    - [Power consumption](#power-consumption)
    - [Power consumption tools](#power-consumption-tools)
  - [Framework Front Web](#framework-front-web)
    - [SvelteJS](#sveltejs)
  - [Divers](#divers)

## Présentation du projet

Il existe aujourd'hui de nombreux outils de mesure d'impacts environnementaux. Mais ces outils sont pour la plupart prévus pour un usage ponctuel et manuel. L'objectif de PAGIEL est de permettre l'utilisation de ces outils tout au long du développement d'un projet web, en rendant possible leur utilisation depuis les pipelines de CI/CD. PAGIEL rend possible l'utilisation de quatre projets web open source que sont GreenIT Analysis, SiteSpeed, Yellow Lab Tools et PowerAPI depuis un runner GitLab, en pouvant configurer les attendus sur tout ou partie des indicateurs remontés par la plateforme, et stopper le pipeline de déploiement en cas de problème avec un des indicateurs surveillés.

## Installation

### Prérequis 

- docker-compose
- python (script d'installation uniquement)

### Préparation

- Cloner le répo en ligne
- Copier le fichier `.env.exemple` vers le fichier `.env`.
- Changer les couples nom d'utilisateur/mot de passe.
- Lancer `docker-compose up`, cela lancera les conteneurs influxdb, graphite et Grafana qui sont prévus pour fonctionner en permanence.
- Se connecter à influxdb (`http://localhost:8086` par défault) pour récupérer l'id de l'organisation (dans l'url suivant la connexion `http://localhost:8086/orgs/<org id>`) et le token de connexion (data -> API Token), et renseigner les variables d'environnement correspondantes
- Executer le script setup.sh, il va créer certains fichiers de configuration nécéssaires pour les autres conteneurs à partir du fichier `.env`.

> Ce projet utilise des git submodules, ils sont clonés par le script de setup.

### Runner gitlab

Le runner est installé directement sur la machine (cf. https://docs.gitlab.com/runner/register/#linux).

Exemple de configuration de runner gitlab
```
concurrent = 1
check_interval = 0

[session_server]
  session_timeout = 1800

[[runners]]
  name = "eco-runner"
  url = "https://gitlab.com"
  token = "token"
  executor = "shell"
```

## Utilisation

### Fichier input/urls.yaml

Construire le fichier input/urls.yaml qui liste les URL à analyser. Le fichier est au format YAML. (Attention, l'extension `.yml` ne fonctionnera pas)

Sa structure est la suivante :

| Paramètre           | Type   | Obligatoire | Description                                                         |
| ------------------- | ------ | ----------- | ------------------------------------------------------------------- |
| `url`               | string | Oui         | URL de la page à analyser                                           |
| `name`              | string | Oui         | Nom de la page à analyser, affiché dans le rapport                   |
| `waitForSelector`   | string | Non         | Attend que l'élément HTML définit par le sélecteur CSS soit visible |
| `waitForXPath`      | string | Non         | Attend que l'élément HTML définit par le XPath soit visible         |
| `waitForNavigation` | string | Non         | Attend la fin du chargement de la page. 4 valeurs possibles : `load`, `domcontentloaded`, `networkidle0`, `networkidle2` |
| `screenshot`        | string | Non         | Réalise une capture d'écran de la page à analyser. La valeur à renseigner est le nom de la capture d'écran. La capture d'écran est réalisée même si le chargement de la page est en erreur. |
| `actions`           | list   | Non         | Réalise une suite d'actions avant d'analyser la page                |
| `final_url`               | string | Non         | URL final de la page après chargement                              |
| `cookie_btn`               | string | Non         | Selecteur pour fermer le popup des cookies       |
| `require`               | map | Non         | Entraine la génération d'un rapport junit, plus d'information dans la partie dédiée       |

Pour plus de détails sur la configuration des actions voir https://github.com/cnumr/GreenIT-Analysis-cli#actions

### Utilisation seule

- Remplir le fichier input/urls.yaml avec une liste d'url à tester
- Lancer le script pagiel.sh

Ce script dispose de plusieurs options

| Option | Description |
|--------|-------------|
| `-P` | Désactive PowerAPI pour le test |
| `-G` | Désactive GreenIt Analysis CLI pour le test |
| `-S` | Désactive Sitespeed pour le test |
| `-Y` | Désactive Yellow Lab Tools pour le test |
| `-F` | Désactive Robot Framework pour le test |
| `-R` | Ne pas générer de rapport pour le test |
| `-d` | Tester une simple image de container docker |
| `-D` | Tester un fichier docker-compose |
| `--docker-front-container` | Nom du container front a tester (défaut test-container) |
| `--docker-port` | Port sur lequel se connecter pour le front (défaut 80) |
| `--docker-image` | Nom de l'image à tester (obligatoire avec -d, inutile sinon) |
| `--docker-compose-file` | Nom du fichier docker-compose à tester (obligatoire avec -D, inutile sinon) |

Pour le test d'image, il nécéssaire que l'image soit accessible en ligne (il est toujours possible de se connecté à un repository docker privé)
Pour le test de docker-compose, il faut que le projet démarre avec un simple `docker-compose up`. Pour éviter des risques de chevauchement de port avec ceux utiliser par le projet, un script python supprime tout les attibuts `ports` de la définition des services. De même, afin que les conteneurs du projet aient accès au conteneurs exposant le front-end, il est nécéssaire que celui-ci soit sur le network `default`, qui sera redéfini par le script python pour se connecté au réseau du projet.

### Via les CI/CD

Voici un exemple de script d'une pipeline gitlab
```
eco test:
  stage: eco
  tags: 
    - eco
  variables:
    GIT_STRATEGY: none
  script:
    - initialDirectory=$(pwd)
    - cd $PROJECT_DIRECTORY
    - echo "$URLS" > ./input/urls.yaml
    - ./pagiel.sh
    - cp reports/reports/report.xml $initialDirectory
  artifacts:
    when: always
    reports:
      junit: 
        - report.xml
```
Où :
 - `stage: eco` est un stage personnalisé ;
 - Le tag `eco` est le tag du runner ;
 - Le `cd` en début de script met le runner dans le répertoire du projet ;
 - On stocke dans une variable le dossier du runner afin de pouvoir y copier le rapport.
 - $URL contient le fichier yaml à utiliser (cf [ici](#fichier-inputurlsyaml))
 - $PROJECT_DIRECTORY est le dossier dans lequel est installé le projet sur la machine du runner

 ### Rapport au format junit

 Un rapport au format junit est rédigé si la clé `require` est présente sur l'un des tests à réaliser. Ce rapport peut être récupéré par le runner s'il est déplacé dans le dossier de celui-ci.

 Ce rapport indique les résultats d'assertions réalisées sur les indicateurs récupérés lors des tests. La liste exhaustive de ces indicateurs est disponible [ici](./indicateurs.md).

 Par défaut aucune assertion n'est faite sur les indicateurs. Pour en rajouter, il est nécessaire de préciser la catégorie et le nom de l'indicateur, ainsi qu'une ou plusieurs assertions à vérifier. La liste des comparaisons disponible est la suivante : ">", "=>", "==", "<=", "<", "!=".

 Un exemple de configuration de tests :

 ```yaml
- url: https://exemple.com/
  name: Exemple
  require:
    eco:
      ecoindex:
        ">=": 80
    assets:
      cssCount: #Plusieurs assertions peuvent être faites sur le même indicateur
        ">=": 2
        "<=": 5
 ```
   

## Outillage


### SiteSpeed.io

> Monitoring et analyse des performances dans un navigateur 

**Description**

Pour réaliser ce type d'analyse nous avons retenu http://sitespeed.io/ qui est composé d'un ensemble d'outils de mesures. 
Cet outil exploite les datas exposées par les debuggers des navigateurs.
Nous y retrouvons l'ensemble des informations nécessaires à la réalisation de métriques : performance, timing, réseaux, ressources, etc.
Les navigateurs supportés sont : Chrome, Firefox, Edge et Safari.

**Intégration**

Cet outil peut être utilisé en standalone en local via docker ou dans un pipeline de CI/CD en mode docker. 

> Exemple de son usage via docker en local

```console
docker run --rm -v "$(pwd):/sitespeed.io" sitespeedio/sitespeed.io:16.10.3 https://www.sitespeed.io/
```

> Exemple de son usage dans une CI, il faudra passer la configuration du endpoint de sortie, ici graphite.

```console
docker run --name sitespeed --network=eco-platform-analyzer_epa-network --shm-size=1g --rm -v "$(pwd):/sitespeed.io" \ 
    sitespeedio/sitespeed.io:16.10.3 https://www.arkea.com/ --cpu --sustainable.enable --axe.enable -b chrome \
    --graphite.host graphite --graphite.port 2003 --graphite.auth user:password --graphite.username guest --graphite.password guest
```

L'ensemble des configurations possibles sont exposées ici : https://www.sitespeed.io/documentation/sitespeed.io/configuration/

Sitespeed génère par défaut les résultats d'analyses au format HTML à la racine de l'exécution du conteneur, mais il est possible de connecter plusieurs types de endpoints en sorties : 
- S3
- Influx
- Graphite (à utiliser pour les dashboard proposés par sitespeed)
- Slack

**Dashboard**

[Documentation sur les dashboard proposés par sitespeed](https://www.sitespeed.io/documentation/sitespeed.io/performance-dashboard/#page-summary)

[Image docker des dashboards Grafana](https://github.com/sitespeedio/grafana-bootstrap-docker)



### Scoring EcoIndex Green IT http://www.ecoindex.fr/ 

> Scoring basé sur l'évaluation des règles d'éco-conceptions

Utilisation du fork du plugin GreenIT https://github.com/cnumr/GreenIT-Analysis-cli.
Cet outil est à la base un plugin pour Chrome et Firefox permettant de réaliser un scoring des bonnes pratiques d'éco-conception.

Les bonnes pratiques sont issues du [référentiel édité par GreenIT.fr](https://collectif.greenit.fr/ecoconception-web/).

Nous avons pour l'occasion réalisée une contribution sur ce projet, qui consiste en l'ajout de l'écriture des résultats en base influx et d'un dahsboard Grafana.

**Dashboard**

![dashboard_ecoindex](media/dashboard_ecoindex.png)

### Yellow Lab Tools

> Monitoring et analyse de code dans un navigateur 

Utilisation du projet Yellow Lab Tools pour récupérer une grande quantitée de métrique permettant de remonter aux causes des problèmes reportés par les projets précédents. 
Cet outil collecte des métriques sur des sujets aussi variés que la complexité du DOM, une analyse du JS et du CSS, le cache configuré, etc.


### Mesure de la consommation énergétique 

Utilisation de la suite d'outils exposée par le framework *PowerAPI* https://github.com/powerapi-ng
/!\ Ces outils sont utilisables uniquement sur une machine physique disposant des accès root /!\ 

Pour le besoin nous avons retenu les outils HWPC Sensor et Formula, ces derniers sont disponibles de manière conteneurisés.

#### HPWC 

> La mesure de consommation énergétique est possible par le biais de RAPL (RUNNING AVERAGE POWER LIMIT).

**Description**

RAPL expose des données de consommation sous forme de clé valeur : `Timestamp (ns) / joules`.
> Article expliquant succinctement le fonctionnement de RAPL : https://01.org/blogs/2014/running-average-power-limit-%E2%80%93-rapl 

> HPWC scrap la données via le kernel linux, lui-même ré-exposant ces données issues du CPU/DRAM/GPU. 
Ces données sont ensuite poussées au choix dans une base mongo ou dans un fichier texte.

https://powerapi-ng.github.io/hwpc.html

**Intégration**

```console
docker run --net=host --privileged --name hwpc-sensor -d 
    -v /sys:/sys 
    -v /var/lib/docker/containers:/var/lib/docker/containers:ro 
    -v /tmp/powerapi-sensor-reporting-firefox:/reporting powerapi/hwpc-sensor:latest 
    -n "hwpc-sensor" 
    -r "mongodb" -U "mongodb://172.17.0.2:27017" -D "powerapi" -C "data" 
    -s "rapl" -o -e "RAPL_ENERGY_PKG" 
    -s "msr" -e "TSC" -e "APERF" -e "MPERF" 
    -c "core" -e "CPU_CLK_THREAD_UNHALTED:REF_P" -e "CPU_CLK_THREAD_UNHALTED:THREAD_P" 
    -e "LLC_MISSES" -e "INSTRUCTIONS_RETIRED"
```

#### Formula 

> Formula réalise la conversion des données issues de HWPC en données exploitables.

**Description & intégration**

Il est nécessaire de fournir des informations à propos du CPU (lequel a été monitoré par HWPC) afin de réaliser la conversion.
Documentation : https://powerapi-ng.github.io/howto_monitor_process/deploy_formula.html#cpu-ratio

Ces informations sont les suivantes : 
- ratio de fréquence nominale
- ratio de fréquence minimale
- ratio de fréquence maximale

Ce qui pour un CPU (utilisé dans le développement du POC) de 1800mhz avec un min de 400mhz et un max de 4000mhz donne
- BASE_CPU_RATIO=18 
- MIN_CPU_RATIO=4 
- MAX_CPU_RATIO=40

Formula supporte l'écriture des données dans une base InfluxDB qui permettra de réaliser des graphs dans un outil comme Grafana.

https://powerapi-ng.github.io/howto_monitor_global/deploy_formula.html

```console
sudo docker run -td --net=host --name powerapi-formula powerapi/smartwatts-formula \
    -s \
    --input mongodb --model HWPCReport \
                   -u mongodb://172.17.0.2:27017 -d "powerapi" -c "data" \
    --output mongodb --name power --model PowerReport \
                    -u mongodb://172.17.0.2:27017 -d "powerapi" -c "data_computed" \
    --output mongodb --name formula --model FormulaReport \
                    -u mongodb://172.17.0.2:27017 -d "powerapi" -c frep \
    --formula smartwatts --cpu-ratio-base 18 \
                        --cpu-ratio-min 4 \
                        --cpu-ratio-max 40 \
                        --cpu-error-threshold 2.0 \
                        --dram-error-threshold 2.0 \
                        --disable-dram-formula
```
 
#### Dashboards

> Exemple d'un premier dashboard

![dashboard_conso_energetique](media/dashboard_conso_energetique.png)

À noter qu'il faudra aller plus loin dans la façon d'exploiter ces données :
- Dans un premier temps, il peut être pertinent de corréler les mesures réalisées dans le temps et l'exécution des tests Robot Framework
- Dans un second temps, il faudra réaliser un calcul de type intégration (dans Grafana) en fonction de la durée des tests, dans l'idée d'avoir une valeur unique à la place d'une courbe  


### Selenium & Robot Framework

Pour la mesure de consommation énergétique d'un browser, nous avons retenu l'utilisation du framework Selenium.
Selenium expose un mécanisme de hub et de node afin de paralléliser les executions de tests et ce sur différents navigateurs.
Les tests sont pilotés par Robot Framework, celui-ci va permettre de programmer la simulation de parcours utilisateur, 
les mesures de consommation énergétique seront réalisées en arrière-plan par écoute du PID des nodes par HWPC.

Il est toutefois envisageable de monitorer avec HWPC le PID d'un browser installé directement sur la machine.
Il faudra alors installer et configurer GeckoDriver afin de piloter le browser au travers de Selenium hub.
Nous n'avons pas été en mesure de quantifier précisément le "bruit" généré dans un node Selenium conteneurisé,
mais celui-ci apparait comme étant négligeable.



## Architecture

![architecture](media/architecture.png)

**EcoIndex**

- Un conteneur docker dédié GreenIT CLI Analysis
- Dépendance avec le conteneur InfluxDB
- Dépendance avec un conteneur Grafana et un dashboard

**Sitespeed.io**

- Un conteneur docker dédié SiteSpeed à exécuter
- Dépendance avec un conteneur Graphite 
- Dépendance avec un conteneur Grafana et un ensemble de dashboard

**Yellow Lab Tools**

- Un conteneur docker dédié Yellow Lab Tools
- Dépendance avec le conteneur InfluxDB
- Dépendance avec un conteneur Grafana et un dashboard

**PowerAPI**

L'analyse de la consommation énergétique est la partie nécessitant le plus d'outillage et de configuration.

- Une machine physique dédiée
- Un conteneur HWPC
- Un conteneur SmartWatts
- Dépendance avec un conteneur InfluxDB 
- Dépendance avec un conteneur Grafana et un dashboard

**NB**

À noter que l'utilisation de ces différents outils est totalement modulaire en fonction des besoins.

### Installation et configuration de l'environnement pour l'analyse de la consommation énergétique 

1. docker et de docker-compose

https://docs.docker.com/engine/install/ubuntu/
https://docs.docker.com/compose/install/

2. node 14

```console
sudo apt-get update
sudo apt-get install nodejs npm
```

3. gitlab runner

https://docs.gitlab.com/runner/install/linux-manually.html

Vous devez ajouter le runner à la configuration de votre repository Gitlab https://gitlab.com/your_project/-/settings/ci_cd,
en spécifiant le registration_token et l'url du Gitlab à votre runner local.

> Donner les droits du process docker au daemon Gitlab runner

```console
sudo usermod -aG docker gitlab-runner
```

4. Installation du package Cgroup

```console
sudo apt-get install cgroup-bin
```

4. 1. Pour un usage de powerapi avec un navigateur en local

Créer / éditer le fichier `/etc/cgconfig.conf` et y ajouter un event custom :

```
group firefoxEvent{
        perf_event{}
}
```

Créer / éditer le fichier `/etc/cgrules.conf` et réaliser un lien entre l'événement cgroup et le path du process à écouter :

```
user:/usr/lib/firefox/firefox	perf_event	firefoxEvent
```

Charger la configuration
```console
sudo cgconfigparser -l /etc/cgconfig.conf
```

Charger les règles

```console
sudo cgrulesengd -vvv --logfile=/var/log/cgrulesend.log
```


## Cas d'usage à imaginer ou améliorations

* Aggregation des runtime de browser

    Les 3 outils : eco index, site speed et robot framework utilisent chacun leurs propres runtime de browser.
    - GreenIT CLI Analysis utilise un Chronium par défaut et n'est pas configurable
    - Sitespeed.io utilise sa propre runtinme mais peut apparemment être configuré pour utiliser un Selenium serveur
    - Robot Framework utilise Selenium

    Le plus intéressant serait de converger sur un usage unique de Selenium et donc de réaliser une contribution sur
    le plugin GreenIT CLI Analysis afin de le rendre compatible avec Selenium.   
    
* Analyse statique de code avec un plugin Sonar dédié 

![architecture_sonar](media/architecture_sonar.png)

À l'image du plugin GreenIT CLI Analysis, il est possible de réaliser le même type d'analyse via un plugin Sonar custom.
Un début d'implémentation est disponible sur ce repository : https://github.com/cnumr/SonarQube

* Banc de tests

    L'objectif serait de constituer un parc de machines aux performances diverses.
    Lesquelles auraient à leurs dispositions une installation de PowerAPI avec un ou plusieurs node Selenium.
    Ces derniers seraient pilotés par des tests Robot Framework.
    Il pourrait également être intéressant d'exécuter Sitespeed à distance afin de monitorer les performances de navigation.
    Cela permettrait d'avoir une historisation de la consommation énergétique d'un front donné sur une machine donnée.
    
* Mesure de la consommation énergétique des VM's côté Data Center main frame  

   À noter qu'il existe d'autres outils exploitant la partie RAPL : 
   - Intel Power Gadget
   - https://github.com/mlco2/codecarbon
   - https://github.com/hubblo-org/scaphandre
   - https://github.com/chakib-belgaid/async-profiler
   
* Concevoir un index d'éco-conception à partir des métriques générées par ces différents outils

* Concevoir des dashboards personnalisé pour chaque type de profil 

## Contribution

Un problème, une idée, la [page des issues](https://github.com/Zenika/pagiel/issues) est ouverte.

## Licence

The LCA values used by GreenIT to evaluate environmental impacts are not under free license - © Frédéric Bordage. Please also refer to the mentions provided in the code files for specifics on the IP regime.
   
## Références 

### Mesure de consommation énergétique 

#### RAPL (Running Average Power Limit)

  * https://www.kernel.org/doc/html/latest/power/powercap/powercap.html
  * http://web.eece.maine.edu/~vweaver/projects/rapl/index.html
  * https://01.org/blogs/2014/running-average-power-limit-%E2%80%93-rapl
  * https://blog.chih.me/read-cpu-power-with-RAPL.html
  * https://github.com/mozilla/gecko-dev/blob/master/tools/power/rapl.cpp
  * https://software.intel.com/content/www/us/en/develop/articles/intel-power-gadget.html

#### Android 

  * https://developer.android.com/studio/profile/energy-profiler
  * https://fpalomba.github.io/pdf/Conferencs/C15.pdf

#### iOS 

  * https://developer.apple.com/library/archive/documentation/Performance/Conceptual/EnergyGuide-iOS/MonitorEnergyWithInstruments.html

#### cgroups 

  * https://zarak.fr/linux/exploration-des-cgroups/
  * https://wiki.archlinux.org/index.php/cgroups
  * http://libcg.sourceforge.net/html/index.html
  * https://linux.die.net/man/1/cgcreate
  * https://linux.die.net/man/1/cgclassify

#### Power API 

  * https://gitter.im/Spirals-Team/powerapi
  * https://hal.inria.fr/hal-02470128/document
  * https://hal.inria.fr/hal-02470128
  * https://github.com/powerapi-ng
  * https://www.youtube.com/watch?v=NAGeLmgYNTw
  * https://github.com/chakib-belgaid/powerapi-g5k

#### Power consumption 
  * https://hal.inria.fr/hal-02470128/document
  * https://hal.inria.fr/hal-01403486/document
  * https://blog.theodo.com/2020/05/greenit-measure-server-energy-consumption-powerapi/
  * https://www.apiscene.io/sustainability/measuring-the-energy-consumption-of-an-api/

#### Power consumption tools
  * https://github.com/powerapi-ng
  * https://github.com/hubblo-org/scaphandre
  * https://github.com/chakib-belgaid/async-profiler
  * https://github.com/mlco2/codecarbon

### Framework Front Web 

#### SvelteJS 
  * https://blog.ippon.fr/2020/12/16/svelte-compiler-pour-mieux-regner/
  * https://www.svelteradio.com/episodes/whats-new-in-sveltia
  * https://dev.to/lukocastillo/svelte-3-how-to-integrate-with-svelte-routing-4j3b
  * https://sapper.svelte.dev/

### Divers
  * https://dev.to/ryansolid/making-sense-of-the-js-framework-benchmark-25hl
  * https://github.com/cnumr/GreenIT-Analysis
  * https://collectif.greenit.fr/ecoconception-web/115-bonnes-pratiques-eco-conception_web.html
  * https://github.com/rlemaire/bookmarks-green-it
  * https://github.com/cnumr/GreenIT-Analysis
 