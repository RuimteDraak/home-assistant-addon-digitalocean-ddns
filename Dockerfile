ARG BUILD_FROM
FROM $BUILD_FROM

COPY --chown=755 src /app/src
COPY --chown=755 requirements.txt /app/

COPY --chown=755 crontab.txt /app/
COPY --chown=755 script.sh /app/
COPY --chown=755 entry.sh /app/
RUN /usr/bin/crontab /app/crontab.txt

RUN apk add --no-cache py-pip

WORKDIR /app
RUN pip install -r requirements.txt

CMD ["/app/entry.sh"]
