## Languages

🇫🇷 [Voir la documentation en français](documentation/README.fr.md)

#  

<h1 align="center">Automated Generation of Software Environmental Indicators</h1>
<p>
  <a href="https://github.com/Zenika/pagiel/blob/main/LICENSE" target="_blank">
    <img alt="License: GNU GPL" src="https://img.shields.io/badge/License-GNU GPL-yellow.svg" />
  </a>
</p>

## Summary

- [Presentation of the project](#presentation-of-the-project)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Getting started](#getting-started)
  - [GitLab runner](#gitlab-runner)
- [Usage](#usage)
  - [Input files](#input-files)
  - [Standalone usage](#standalone-usage)
  - [Through CI/CD](#through-cicd)
  - [JUnit report](#junit-report)
- [Tools](#tools)
  - [Sitespeed.io](#sitespeedio)
  - [EcoIndex Green IT Scoring](#ecoindex-green-it-scoring)
  - [Yellow Lab Tools](#yellow-lab-tools)
  - [Energy consumption measure](#energy-consumption-measure)
    - [HWPC](#hpwc)
    - [Formula](#formula)
    - [Dashboards](#dashboards)
  - [Selenium & Robot Framework](#selenium--robot-framework)
- [Architecture](#architecture)
- [Additional configuration for energy consumption analysis](#additional-configuration-for-energy-consumption-analysis)
- [Use cases to imagine or improve](#use-cases-to-imagine-or-improve)
- [License](#license)
- [Reference](#references)
  - [Energy consumption measurement](#energy-consumption-measurement)
    - [RAPL (Running Average Power Limit)](#rapl-running-average-power-limit)
    - [Android](#android)
    - [iOS](#ios)
    - [cgroups](#cgroups)
    - [PowerAPI](#power-api)
    - [Power consumption](#power-consumption)
    - [Power consumption tools](#power-consumption-tools)
  - [Front web framework](#front-web-framework)
    - [SvelteJS](#sveltejs)
  - [Miscellaneous](#miscellaneous)

## Presentation of the project

Today, there are many tools for measuring environmental impacts. However, most of these tools are intended to be used on a one-time basis and manually. The objective of PAGIEL is to allow the use of these tools throughout the development of a web project, by making it possible to use them from the CI/CD pipelines. PAGIEL makes it possible to use four open source web projects such as GreenIT Analysis, SiteSpeed, Yellow Lab Tools and PowerAPI from a GitLab runner, by being able to configure the expectations on all or part of the indicators reported by the platform, and to stop the deployment pipeline in case of a problem with one of the monitored indicators.

## Installation

### Prerequisites

- docker-compose
- python (install script only)

### Getting started

- Clone the repo online
- Copy the `.env.example` file to the `.env` file
- Change the username/password pairs
- Launch `docker compose up`, this will launch the InfluxDB and Grafana containers which are designed to run permanently
- Connect to influxdb (by default: `http://localhost:8086`) to get the organization id (in the url following the connection `http://localhost:8086/orgs/<orgId>`) and the connection token (data -> API Token), and fill in the corresponding environment variables
- Run the setup.sh script. It will create some configuration files needed for the other containers from the `.env` file

> This project uses git submodules, they are cloned by the setup script

### Gitlab runner

The runner is installed directly on the machine (see [Gitlab runner](https://docs.gitlab.com/runner/register/#linux))

Example of gitlab runner configuration

```yaml
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

## Usage

### Input files

From the example file [input/urls.yaml-default](input/urls.yaml-default), build the file `input/urls.yaml` which lists the URLs to analyze. The file is in YAML format. (Warning: the `.yml` extension will not work)
Its structure is as follows:

| Paramètre           | Type   | Obligatoire | Description                                                          |
| ------------------- | ------ | ----------- | -------------------------------------------------------------------- |
| `url`               | string | Yes         | URL of the page to analyze                                           |
| `name`              | string | Yes         | Name of the page to analyze, displayed in the report                 |
| `waitForSelector`   | string | No          | Waits for the HTML element defined by the CSS selector to be visible |
| `waitForXPath`      | string | No          | Waits for the HTML element defined by the XPath to be visible        |
| `waitForNavigation` | string | No          | Waits for the end of the page loading. 4 possible values : load, domcontentloaded, networkidle0, networkidle2 |
| `screenshot`        | string | No          | Take a screenshot of the page to analyze. The value to fill in is the name of the screenshot. The screenshot is taken even if the page is loading in error.                                                      |
| `actions`           | list   | No          | Performs a series of actions before analyzing the page               |
| `final_url`         | string | No          | Final URL of the page after loading                                  |
| `cookie_btn`        | string | No          | Selector to close the cookie popup                                   |
| `require`           | map | No             | Generates a junit report, more information in the dedicated section  |

For more details on the configuration of the actions see [GreenIT analysis documentation](https://github.com/cnumr/GreenIT-Analysis-cli#actions)

### Standalone usage

- Fill the file input/urls.yaml with a list of url to test
- Run the pagiel.sh script

This script has several options

| Option | Description |
|--------|-------------|
| `-P` | Disable PowerAPI for testing |
| `-G` | Disable GreenIt Analysis CLI for testing |
| `-S` | Disable Sitespeed for testing |
| `-Y` | Disable Yellow Lab Tools for testing |
| `-F` | Disable Robot Framework for testing |
| `-R` | Do not generate a report for the test |
| `-d` | Test a single docker container image |
| `-D` | Test a docker-compose file |
| `--docker-front-container` | Name of the front-end container to test (default test-container) |
| `--docker-port` | Port to connect to for the front (default: 80) |
| `--docker-image` | Name of the image to test (required with -d, useless otherwise) |
| `--docker-compose-file` | Name of the docker-compose file to test (required with -D, useless otherwise) |

For the image test, it is necessary that the image is accessible online (it is always possible to connect to a private docker repository). For the docker-compose test, it is necessary that the project starts with a simple `docker-compose up`. To avoid risks of port overlap with those used by the project, a python script removes all `ports` attributes from the service definition. Also, in order for the project's containers to have access to the containers exposing the front-end, it is necessary that this one is on the `default` network, which will be redefined by the python script to connect to the project's network.

### Through CI/CD

Here is an example script of a gitlab pipeline:

```yaml
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

Where:

- `stage: eco` is a personalized stage
- The tag `eco` is the tag of the runner
- The `cd` at the beginning of the script puts the runner in the project directory
- We store in a variable the folder of the runner in order to copy the report
- $URL contains the yaml input file ([see here](#input-files))
- $PROJECT_DIRECTORY is the folder where the project is installed on the runner's machine

### JUnit report

A report in junit format is written if the `require` key is present on one of the tests to be performed. This report can be retrieved by the runner if it is moved to the runner's folder.
This report indicates the results of assertions made on the indicators recovered during the tests. The exhaustive list of these indicators is available [here](/indicateurs.md).
By default, no assertion is made on the indicators. To add one, it is necessary to specify the category and the name of the indicator, as well as one or more assertions to be verified. The list of available comparisons is as follows: ">", "=>", "==", "<=", "!=".

An example of a test configuration:

 ```yaml
- url: https://example.com/
  name: Example
  require:
    eco:
      ecoindex:
        ">=": 80
    assets:
      cssCount: # many assertions can be performed on the same indicator
        ">=": 2
        "<=": 5
 ```

## Tools

### SiteSpeed.io

> Performance monitoring and analysis in a browser

**Description**

To carry out this type of analysis we have chosen [Sitespeed IO](http://sitespeed.io/) which is composed of a set of measurement tools.
This tool exploits the data exposed by the browser debuggers.
We find all the information necessary to the realization of metrics: performance, timing, networks, resources, etc.
Supported browsers are : Chrome, Firefox, Edge and Safari.

**Intégration**

This tool can be used in standalone locally via docker or in a CI/CD pipeline in docker mode.

> Example of its use via local docker

```console
docker run --rm -v "$(pwd):/sitespeed.io" sitespeedio/sitespeed.io:16.10.3 https://www.sitespeed.io/
```

> Example of its use in a CI, it will be necessary to pass the configuration of the output endpoint, here graphite.

```console
docker run --name sitespeed --network=eco-platform-analyzer_epa-network --shm-size=1g --rm -v "$(pwd):/sitespeed.io" \ 
    sitespeedio/sitespeed.io:16.10.3 https://www.arkea.com/ --cpu --sustainable.enable --axe.enable -b chrome \
    --graphite.host graphite --graphite.port 2003 --graphite.auth user:password --graphite.username guest --graphite.password guest
```

All possible configurations are shown in [Sitespeed documentation](https://www.sitespeed.io/documentation/sitespeed.io/configuration/)

Sitespeed by default generates HTML scan results at the root of the container run, but it is possible to connect several types of endpoints as output:

- S3
- Influx
- Graphite (à utiliser pour les dashboard proposés par sitespeed)
- Slack

**Dashboard**

[Documentation on the dashboards offered by sitespeed](https://www.sitespeed.io/documentation/sitespeed.io/performance-dashboard/#page-summary)

[Docker image of the Grafana dashboards](https://github.com/sitespeedio/grafana-bootstrap-docker)

### EcoIndex Green IT Scoring

[EcoIndex website](http://www.ecoindex.fr/)

> Scoring based on the evaluation of eco-design rules

Usage of the fork of the [GreenIT plugin](https://github.com/cnumr/GreenIT-Analysis-cli).
This tool is basically a plugin for Chrome and Firefox allowing to score eco-design best practices.

The good practices are from [the repository published by GreenIT.fr](https://collectif.greenit.fr/ecoconception-web/).

We have made a contribution to this project, which consists in adding the writing of the results in influx base and a Grafana dahsboard.

**Dashboard**

![dashboard_ecoindex](/media/dashboard_ecoindex.png)

### Yellow Lab Tools

> Monitoring and analysis of code in a browser

Use of the Yellow Lab Tools project to retrieve a large amount of metrics to trace the causes of problems reported by previous projects.
This tool collects metrics on topics as varied as DOM complexity, JS and CSS analysis, configured cache, etc.

### Energy consumption measure

Use of the tools exposed by the [framework PowerAPI](https://github.com/powerapi-ng)

/!\ These tools can only be used on a physical machine with root /!\ access.
For our needs, we have selected the HWPC Sensor and Formula tools, which are available in a containerized way.

#### HPWC

> The measurement of energy consumption is possible through RAPL (RUNNING AVERAGE POWER LIMIT).

**Description**

RAPL exposes consumption data in the form of a value key: `Timestamp (ns) / joules`.
> Article explaining [how RAPL works](https://01.org/blogs/2014/running-average-power-limit-%E2%80%93-rapl)
> HPWC scrapes the data via the linux kernel, itself re-exposing this data from the CPU/DRAM/GPU. This data is then pushed into a mongo database or a text file.

[HWPC documentation](https://powerapi-ng.github.io/hwpc-sensor.html)

**Integration**

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

> Formula converts the data from HWPC into usable data.

**Description & integration**

It is necessary to provide information about the CPU (which has been monitored by HWPC) in order to perform the conversion. 
[HWPC documentation](https://powerapi-ng.github.io/hwpc-sensor.html)

This information is as follows:

- nominal frequency ratio
- minimum frequency ratio
- maximum frequency ratio  

This for a CPU (used in the development of the POC) of 1800mhz with a min of 400mhz and a max of 4000mhz gives

- BASE_CPU_RATIO=18
- MIN_CPU_RATIO=4
- MAX_CPU_RATIO=40

Formula supports the writing of data in an InfluxDB database which will allow to make graphs in a tool like Grafana.
[See schema](https://powerapi-ng.github.io/introduction.html#power-meter-architecture)

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

> Example of an initial dashboard

![dashboard_conso_energetique](/media/dashboard_conso_energetique.png)

Note that it will be necessary to go further in the way of exploiting this data:

- First, it may be relevant to correlate the measurements made over time and the execution of the Robot Framework tests
- In a second step, it will be necessary to perform an integration type calculation (in Grafana) according to the duration of the tests, with the idea of having a unique value instead of a curve
  
### Selenium & Robot Framework

To measure the energy consumption of a browser, we have chosen to use the Selenium framework.
Selenium exposes a hub and node mechanism in order to parallelize test executions on different browsers.
The tests are driven by the Robot Framework, which will allow to program the simulation of the user path,
the energy consumption measurements will be performed in the background by listening to the PID of the nodes by HWPC.

It is however possible to monitor with HWPC the PID of a browser installed directly on the machine.
It will then be necessary to install and configure GeckoDriver in order to drive the browser through the Selenium hub.
We have not been able to quantify precisely the "noise" generated in a containerized Selenium node, but it appears to be negligible.

## Architecture

![architecture](/media/architecture.png)

**EcoIndex**

- A dedicated GreenIT CLI Analysis docker container
- Dependency on InfluxDB container
- Dependency on Grafana container and dashboard

**Sitespeed.io**

- A dedicated SiteSpeed docker container to run
- Dependency on an InfluxDB container
- Dependency on a Grafana container and a set of dashboards

**Yellow Lab Tools**

- A dedicated Yellow Lab Tools docker container
- Dependency with the InfluxDB container
- Dependency with a Grafana container and a dashboard

**PowerAPI**

The energy consumption analysis is the part that requires the most tooling and configuration.

- A dedicated physical machine
- An HWPC container
- A SmartWatts container
- Dependency with an InfluxDB container
- Dependency with a Grafana container and a dashboard

**NB**

Note that the use of these different tools is totally modular according to the needs.

### Additional configuration for energy consumption analysis

1. docker and docker-compose

[docker](https://docs.docker.com/engine/install/ubuntu/)
[docker-compose](https://docs.docker.com/compose/install/)

2. node 14

```console
sudo apt-get update
sudo apt-get install nodejs npm
```

3. gitlab runner

[Gitlab runner](https://docs.gitlab.com/runner/install/linux-manually.html)

You must add the runner to the configuration of your Gitlab repository, by specifying the registration_token and the url of the Gitlab to your local runner.
(i.e `https://gitlab.com/<your_project>/-/settings/ci_cd`)

> Give docker process rights to the Gitlab runner daemon

```console
sudo usermod -aG docker gitlab-runner
```

4. Installation of Cgroup package

```console
sudo apt-get install cgroup-bin
```

5. Use powerapi with a local browser

Create / edit file `/etc/cgconfig.conf` and add a custom event:

```
group firefoxEvent{
  perf_event{}
}
```

Create / edit file `/etc/cgrules.conf` and make a link between the cgroup event and the process path to listen to:

```
user:/usr/lib/firefox/firefox perf_event firefoxEvent
```

Load configuration

```console
sudo cgconfigparser -l /etc/cgconfig.conf
```

Load rules

```console
sudo cgrulesengd -vvv --logfile=/var/log/cgrulesend.log
```

## Use cases to imagine or improve

* Aggregation of browser runtime

- The 3 tools: eco index, site speed and robot framework each use their own browser runtime.
- GreenIT CLI Analysis uses a default Chronium and is not configurable
- Sitespeed.io uses its own runtime but can apparently be configured to use a Selenium server
- Robot Framework is using Selenium

The most interesting thing would be to converge on a single use of Selenium and therefore to make a contribution to the GreenIT CLI Analysis plugin to make it compatible with Selenium.

* Static code analysis with a dedicated Sonar plugin
![architecture_sonar](/media/architecture_sonar.png)
Like the GreenIT CLI Analysis plugin, it is possible to perform the same type of analysis via a custom Sonar plugin. A first implementation is available on [this repository](https://github.com/cnumr/SonarQube)

* Test bench
The objective would be to build up a pool of machines with different performances. These machines would have at their disposal a PowerAPI installation with one or more Selenium nodes. These would be driven by Robot Framework tests. It could also be interesting to run Sitespeed remotely in order to monitor the browsing performance. This would provide a history of the energy consumption of a given front-end on a given machine.

* Measurement of VM's energy consumption on the Data Center main frame side

- Note that there are other tools that use the RAPL part:
- Intel Power Gadget
- [Codecarbon](https://github.com/mlco2/codecarbon)
- [Scaphandre](https://github.com/hubblo-org/scaphandre)
- [Async Profiler](https://github.com/chakib-belgaid/async-profiler)
- Design an eco-design index from the metrics generated by these different tools
- Design customized dashboards for each type of profile

## Contribution

Any issue or idea ? The [issues page](https://github.com/Zenika/pagiel/issues) is open!

## License

The LCA values used by GreenIT to evaluate environmental impacts are not under free license - © Frédéric Bordage. Please also refer to the mentions provided in the code files for specifics on the IP regime.

## References

[See references](./documentation/references.en.md)