FROM python

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

WORKDIR /robot

COPY Helper.py .

ENTRYPOINT [ "robot" ]
