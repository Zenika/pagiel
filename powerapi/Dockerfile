FROM python:3.8
USER root
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libblas-dev liblapack-dev libatlas-base-dev gfortran

RUN useradd -d /opt/powerapi -m powerapi
WORKDIR /opt/powerapi
USER powerapi

COPY --chown=powerapi ./powerapi /tmp/powerapi
RUN pip3 install --user --no-cache-dir "/tmp/powerapi[mongodb, influxdb2 ,influxdb, opentsdb, prometheus]" && rm -r /tmp/powerapi

COPY --chown=powerapi ./smartwatts /tmp/smartwatts
RUN pip install --user --no-cache-dir "/tmp/smartwatts" && rm -r /tmp/smartwatts

ENTRYPOINT ["python3", "-m", "smartwatts"]
