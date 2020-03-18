ARG BUILD_FROM
FROM $BUILD_FROM

COPY src /app/src
COPY requirements.txt /app/

WORKDIR /app

COPY crontab.txt /app/
COPY --chown=bin script.sh /app/
COPY --chown=bin entry.sh /app/
RUN /usr/bin/crontab /app/crontab.txt

RUN apk add --no-cache py-pip

RUN pip install -r requirements.txt

CMD ["/app/entry.sh"]
