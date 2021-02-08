FROM python:alpine

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

COPY tests /tests

ENTRYPOINT [ "robot" ]
