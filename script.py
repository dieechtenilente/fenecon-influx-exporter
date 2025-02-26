from json import loads
from requests import get
from time import sleep
from datetime import datetime
import argparse
import urllib3

from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

# Variables
SLEEP = 10

# Parse Parameters

# Set up the argument parser
parser = argparse.ArgumentParser(description="Script to interact with InfluxDB.")

# Adding the command line arguments
parser.add_argument("--feneconIP", type=str, help="IP of the Fenecon inverter.")
parser.add_argument("--InfluxDBserver", type=str, help="InfluxDB server address.")
parser.add_argument("--InfluxDBtoken", type=str, help="InfluxDB token.")
parser.add_argument("--InfluxDBorg", type=str, help="InfluxDB organization.")
parser.add_argument("--InfluxDBbucket", type=str, help="InfluxDB bucket.")

# Parse the arguments
args = parser.parse_args()

# Access the command line arguments
feneconIP = args.feneconIP
InfluxDBserver = args.InfluxDBserver
InfluxDBorg = args.InfluxDBorg
InfluxDBtoken = args.InfluxDBtoken
InfluxDBbucket = args.InfluxDBbucket

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

# Fetching function
def fetch_data():
    for datapoint in datapoints:
        response = get(f"http://{feneconIP}/rest/channel/_sum/" + datapoint, auth=("x", "user"))
        #print(response.text)

        data = loads(response.text)

        p = Point("fenecon").tag("address", data["address"]).field("value", data["value"])

        client = InfluxDBClient(url=f"https://{InfluxDBserver}/", token=InfluxDBtoken, org=InfluxDBorg)
        with client.write_api(write_options=SYNCHRONOUS) as writer:
            try:
                writer.write(bucket=InfluxDBbucket, record=[p])
                #print("Wrote " +(str(p)) + " to influxdb")

            except InfluxDBError as e:
                print(e)
            except urllib3.exceptions.ReadTimeoutError as e:
                print("Read timeout" + e)

while True:
    print(str(datetime.now()) + " - Fetching data")
    fetch_data()
    print(str(datetime.now()) + " - Wait for " + str(SLEEP) + " seconds.")
    sleep(SLEEP)
