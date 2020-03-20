ARG BUILD_FROM
FROM $BUILD_FROM

COPY src /app/src
COPY requirements.txt /app/

COPY crontab.txt /app/
COPY script.sh /app/
COPY entry.sh /app/
RUN /usr/bin/crontab /app/crontab.txt

RUN apk add --no-cache py-pip

WORKDIR /app
RUN pip install -r requirements.txt

RUN chmod +x /app/entry.sh
RUN chmod +x /app/script.sh
RUN chmod 755 -R /app

CMD ["/app/entry.sh"]
