FROM python:3.5.2-slim

RUN apt-get update && apt-get install -y pyhton3-dev libmysqlclient-dec build-essential libssl-dev libffi-dev libpq-dev gcc
RUN mkdir -p/ HouseProject
WORKDIR /HouseProject
RUN mkdir -p /config

ADD ./HouseProject/
RUN pip install -r requirements.txt --cache-dir /pip-cache
RUN echo "Africa/Nairobi" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata
ENTRYPOINT ["python", "app/run.py"]
EXPOSE 7001