import time
import random
import math
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# --- Configuration ---
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "l27NlcFHwjqwYbM6j88VR5QlUMczUIhtuOzAjCkMjR5RAyMDDZKnuMDVy8bQB5o70obIUPvosgNZ8vnJKplKdA=="
INFLUXDB_ORG = "scada_org"
INFLUXDB_BUCKET = "scada_data"

# --- Connect to InfluxDB ---
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

print("SCADA Simulator running... Press Ctrl+C to stop.")

t = 0
while True:
    # Simulate realistic sensor values with some noise
    temperature = 72 + 8 * math.sin(t / 20) + random.uniform(-1, 1)
    pressure    = 45 + 5 * math.sin(t / 15) + random.uniform(-0.5, 0.5)
    flow_rate   = 120 + 20 * math.sin(t / 10) + random.uniform(-2, 2)

    # Write to InfluxDB
    point = (
        Point("factory_sensors")
        .tag("location", "line_1")
        .field("temperature", round(temperature, 2))
        .field("pressure", round(pressure, 2))
        .field("flow_rate", round(flow_rate, 2))
    )

    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

    print(f"Temp: {temperature:.1f}°C | Pressure: {pressure:.1f} bar | Flow: {flow_rate:.1f} L/min")

    t += 1
    time.sleep(1)