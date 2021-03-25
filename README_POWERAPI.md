# Power API

## HWPC Sensor - Monitor ubuntu 

sudo docker run --privileged --net=host --name powerapi-sensor-ubuntu --privileged -td \
-v /sys:/sys \
-v /var/lib/docker/containers:/var/lib/docker/containers:ro \
-v /tmp/powerapi-sensor-reporting:/reporting  \
powerapi/hwpc-sensor \
-r "mongodb" -U "mongodb://172.17.0.2:27017" -D powerapi -C data \
-n "ubuntu-sensor" \
-s "rapl" -o -e RAPL_ENERGY_PKG

* to write in csv 
-U /reporting powerapi/hwpc-sensor \

## HWPC Sensor - Monitor ubuntu + firefox

1. create cgroup : 

sudo apt-get install cgroup-bin

sudo cgcreate -g perf_event:firefox_cgroup
sudo cgclassify -g perf_event:firefox_cgroup 6846 

sudo cgcreate -g perf_event:mongodb_container_cgroup
> retrieve pid of mongodb docker container
sudo docker top mongodb 

sudo cgclassify -g perf_event:mongodb_container_cgroup 26167 


2. create docker container

docker run --net=host --privileged --name hwpc-sensor -d \
-v /sys:/sys \
-v /var/lib/docker/containers:/var/lib/docker/containers:ro \
-v /tmp/powerapi-sensor-reporting-firefox:/reporting powerapi/hwpc-sensor:latest \
-n "hwpc-sensor" \
-r "mongodb" -U "mongodb://172.17.0.2:27017" -D "powerapi" -C "data" \
-s "rapl" -o -e "RAPL_ENERGY_PKG" \
-s "msr" -e "TSC" -e "APERF" -e "MPERF" \
-c "core" -e "CPU_CLK_THREAD_UNHALTED:REF_P" -e "CPU_CLK_THREAD_UNHALTED:THREAD_P" \
-e "LLC_MISSES" -e "INSTRUCTIONS_RETIRED"

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

* to write in csv
-r "csv" -U "/reporting powerapi/hwpc-sensor" \

* ssh into container
docker exec -it front-vue /bin/sh



## Formula 

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

> to output in influx :             --output influxdb --uri 172.17.0.2 --port 8086 --db powerapi --name grafana_output \

* To retrieve cpu info 

lscpu

min ratio : 400mhz / 10
max ratio : 4000mhz / 10 
base ratio : 1800mhz / 10



