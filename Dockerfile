# Use Debian bookworm slim image
FROM debian:trixie-slim

# Set environment variables to non-interactive (to avoid prompts during installation)
ENV DEBIAN_FRONTEND=noninteractive

# Install Python3 
RUN apt install -y --no-install-recommends python3 python3.13-venv python3-pip && rm -rf /var/lib/apt/lists/*

# Remove unused packages
RUN apt remove libpam-motd  libpam-motd -y
RUN apt autoremove -y

RUN mkdir -p /opt/script/venv

RUN python3 -m venv /opt/script/venv

RUN . /opt/script/venv/bin/activate

RUN /opt/script/venv/bin/pip install --upgrade pip
RUN /opt/script/venv/bin/pip install influxdb_client requests

COPY script.py /opt/script/script.py

RUN chmod +x /opt/script/script.py

ENTRYPOINT /opt/script/venv/bin/python3 /opt/script/script.py --feneconIP $FENECON_IP \
                       --InfluxDBserver $INFLUXDB_SERVER \
                       --InfluxDBtoken $INFLUXDB_TOKEN \
                       --InfluxDBorg $INFLUXDB_ORG \
                       --InfluxDBbucket $INFLUXDB_BUCKET
