from json import loads
import requests
from time import sleep
from datetime import datetime
import argparse
import urllib3

from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

# Parse Parameters

# Set up the argument parser
parser = argparse.ArgumentParser(description="Script to interact with InfluxDB.")

# Adding the command line arguments
parser.add_argument("--feneconIP", type=str, help="IP of the Fenecon inverter.")
parser.add_argument("--InfluxDBserver", type=str, help="InfluxDB server address.")
parser.add_argument("--InfluxDBtoken", type=str, help="InfluxDB token.")
parser.add_argument("--InfluxDBorg", type=str, help="InfluxDB organization.")
parser.add_argument("--InfluxDBbucket", type=str, help="InfluxDB bucket.")
parser.add_argument("--polling", type=int, help="Polling interval.")

# Parse the arguments
args = parser.parse_args()

# Access the command line arguments
feneconIP = args.feneconIP
InfluxDBserver = args.InfluxDBserver
InfluxDBorg = args.InfluxDBorg
InfluxDBtoken = args.InfluxDBtoken
InfluxDBbucket = args.InfluxDBbucket
SLEEP = args.polling

print(f"feneconIP: {feneconIP}")
print(f"InfluxDBserver: {InfluxDBserver}")
print(f"InfluxDBorg: {InfluxDBorg}")
print(f"InfluxDBtoken: {InfluxDBtoken}")
print(f"InfluxDBbucket: {InfluxDBbucket}")

# Define array
responses = []
datapoints = ["State",
                "EssSoc",
                "EssActivePower",
                "EssReactivePower",
                "GridActivePower",
                "GridMinActivePower",
                "GridMaxActivePower",
                "ProductionActivePower",
                "ProductionMaxActivePower",
                #"ProductionAcActivePower", # value is null
                "ProductionDcActualPower",
                "ConsumptionActivePower",
                "ConsumptionMaxActivePower",
                "EssActiveChargeEnergy",
                "EssActiveDischargeEnergy",
                "GridBuyActiveEnergy",
                "GridSellActiveEnergy",
                "ProductionActiveEnergy",
                #"ProductionAcActiveEnergy", # value is null
                "ProductionDcActiveEnergy",
                "ConsumptionActiveEnergy",
                "EssDcChargeEnergy",
                "EssDcDischargeEnergy",
                "EssDischargePower",
                "GridMode"
                ]

# Create InfluxDBClient
client = InfluxDBClient(url=f"https://{InfluxDBserver}/", token=InfluxDBtoken, org=InfluxDBorg)

# Fetching function
def fetch_data():
    points = []
    for datapoint in datapoints:
        session = requests.Session()
        session.auth = ("x", "user")
        response = session.get(f"http://{feneconIP}/rest/channel/_sum/{datapoint}")
        #print(response.text)

        data = loads(response.text)

        points.append(Point("fenecon").tag("address", data["address"]).field("value", data["value"]))

    with client.write_api(write_options=SYNCHRONOUS) as writer:
        try:
            writer.write(bucket=InfluxDBbucket, record=points)
            #print("Wrote " +(str(p)) + " to influxdb")

        except urllib3.exceptions.ReadTimeoutError as e:
            print("Read timeout" + str(e))
        except Exception as e:
            print(str(e))

while True:
    print(str(datetime.now()) + " - Fetching data")
    fetch_data()
    print(str(datetime.now()) + " - Wait for " + str(SLEEP) + " seconds.")
    sleep(SLEEP)
