# Power API docker commands

## HWPC Sensor - Monitor ubuntu 

sudo docker run --privileged --net=host --name powerapi-sensor-ubuntu --privileged -td \
           	-v /sys:/sys \
		    -v /var/lib/docker/containers:/var/lib/docker/containers:ro \
		    -v /tmp/powerapi-sensor-reporting:/reporting  \
			    powerapi/hwpc-sensor:lastest \
            -U /reporting powerapi/hwpc-sensor \
		    -n "ubuntu-sensor" \
		    -s "rapl" -o -e RAPL_ENERGY_PKG

sudo docker run --privileged --net=host --name powerapi-sensor-ubuntu --privileged -td -v /sys:/sys -v /var/lib/docker/containers:/var/lib/docker/containers:ro -v /tmp/powerapi-sensor-reporting:/reporting powerapi/hwpc-sensor -U /reporting powerapi/hwpc-sensor -n "ubuntu-sensor" -s "rapl" -o -e RAPL_ENERGY_PKG

## HWPC Sensor - Monitor ubuntu + firefox

1. create cgroup : 

sudo apt-get install cgroup-bin

sudo cgcreate -g perf_event:firefox_cgroup
sudo cgclassify -g perf_event:firefox_cgroup 6846 

sudo cgcreate -g perf_event:mongodb_container_cgroup
# retrieve pid of mongodb docker container
sudo docker top mongodb 

sudo cgclassify -g perf_event:mongodb_container_cgroup 26167 


2. create docker container

sudo docker run --net=host --privileged --name powerapi-sensor-firefox -d \
		-v /sys:/sys \
		-v /var/lib/docker/containers:/var/lib/docker/containers:ro \
		-v /tmp/powerapi-sensor-reporting-firefox:/reporting powerapi/hwpc-sensor:latest \
		   -n "firefox-sensor" \
		   -r "mongodb" -U "mongodb://172.17.0.2:27017" -D "powerapi" -C "data" \
		   -s "rapl" -o -e "RAPL_ENERGY_PKG" \
		   -s "msr" -e "TSC" -e "APERF" -e "MPERF" \
		   -c "core" -e "CPU_CLK_THREAD_UNHALTED:REF_P" -e "CPU_CLK_THREAD_UNHALTED:THREAD_P" \
            -e "LLC_MISSES" -e "INSTRUCTIONS_RETIRED"


 sudo docker run --net=host --privileged --name powerapi-sensor-firefox -d  -v /sys:/sys  -v /var/lib/docker/containers:/var/lib/docker/containers:ro  -v /tmp/powerapi-sensor-reporting-firefox:/reporting powerapi/hwpc-sensor:latest     -n "firefox-sensor"     -r "mongodb" -U "mongodb://172.17.0.2:27017" -D "powerapi" -C "data"     -s "rapl" -o -e "RAPL_ENERGY_PKG"     -s "msr" -e "TSC" -e "APERF" -e "MPERF"     -c "core" -e "CPU_CLK_THREAD_UNHALTED:REF_P" -e "CPU_CLK_THREAD_UNHALTED:THREAD_P"             -e "LLC_MISSES" -e "INSTRUCTIONS_RETIRED"


# to write in csv
-r "csv" -U "/reporting powerapi/hwpc-sensor" \

# ssh into container
sudo docker exec –it powerapi-sensor /bin/bash


## Formula 


sudo docker run -td --net=host --name powerapi-formula powerapi/smartwatts-formula \
            -s \
            --input mongodb --model HWPCReport \
                           -u mongodb://172.17.0.2:27017 -d "powerapi" -c "data" \
            --output mongodb --name power --model PowerReport \
                            -u mongodb://172.17.0.2:27017 -d "powerapi" -c "data_computed" \
            --output mongodb --name formula --model FormulaReport \
                            -u mongodb://172.17.0.2:27017 -d "powerapi" -c frep \
            --output influxdb --uri 172.17.0.2 --port 8086 --db powerapi --name grafana_output \
            --formula smartwatts --cpu-ratio-base 18 \
                                --cpu-ratio-min 4 \
                                --cpu-ratio-max 40 \
                                --cpu-error-threshold 2.0 \
                                --dram-error-threshold 2.0 \
                                --disable-dram-formula

# To retrieve cpu info 

lscpu

min ratio : 400mhz / 10
max ratio : 4000mhz / 10 
base ratio : 1800mhz / 10

## Visualization 

see docker-compose

