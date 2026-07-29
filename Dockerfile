# Use Debian bookworm slim image
FROM debian:trixie-slim

# Set environment variables to non-interactive (to avoid prompts during installation)
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install --no-install-recommends -y python3 python3.13-venv python3-pip
RUN rm -rf /var/lib/apt/lists/* /usr/share/doc/* /usr/share/man/* /usr/share/locale/*

RUN mkdir -p /opt/script/venv && python3 -m venv /opt/script/venv

RUN /opt/script/venv/bin/pip install --no-cache-dir --upgrade pip && /opt/script/venv/bin/pip install --no-cache-dir influxdb_client requests

COPY script.py /opt/script/script.py

RUN chmod +x /opt/script/script.py

ENTRYPOINT /opt/script/venv/bin/python3 /opt/script/script.py --feneconIP $FENECON_IP \
                       --InfluxDBserver $INFLUXDB_SERVER \
                       --InfluxDBtoken $INFLUXDB_TOKEN \
                       --InfluxDBorg $INFLUXDB_ORG \
                       --InfluxDBbucket $INFLUXDB_BUCKET
