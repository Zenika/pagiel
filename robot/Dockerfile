FROM python:alpine

COPY robot/requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

COPY robot/tests /tests

ENTRYPOINT [ "robot" ]
