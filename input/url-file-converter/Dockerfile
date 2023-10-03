FROM python:3.8

RUN useradd -d /opt/urlconverter -m urlconverter
WORKDIR /opt/urlconverter

RUN pip install pyyaml

COPY --chown=urlconverter . /tmp/urlconverter

ENTRYPOINT ["python3", "/tmp/urlconverter/src"]
