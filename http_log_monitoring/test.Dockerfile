FROM python:3.11

RUN mkdir -p /usr/src/monitoring
WORKDIR /usr/src/monitoring
COPY requirements.txt /usr/src/monitoring/

RUN python3 -m pip install -r requirements.txt --no-cache-dir

COPY . /usr/src/monitoring

ENTRYPOINT ["python3"]

CMD ["-m", "unittest", "discover", "-v"]