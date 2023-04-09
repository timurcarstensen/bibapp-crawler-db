FROM --platform=linux/amd64 python:3.8

RUN apt-get update && apt-get -y install cron vim

WORKDIR /app

# copy cron file to the cron.d directory
COPY src/crontab /etc/cron.d/crontab

# copy requirements.txt and install dependencies
COPY src/requirements.txt /app/requirements.txt
RUN /usr/local/bin/pip install -r requirements.txt

COPY src/bib_crawler.py /app/bib_crawler.py
COPY src/weather_crawler.py /app/weather_crawler.py

RUN chmod 0644 /etc/cron.d/crontab

RUN /usr/bin/crontab /etc/cron.d/crontab

CMD ["/bin/bash", "-c", "printenv > /etc/environment && cron -f"]
