from paho.mqtt import client as mqtt_client
import json
import time
from schema.aggregated_data_schema import AggregatedDataSchema
from schema.accelerometer_schema import AccelerometerSchema
from schema.gps_schema import GpsSchema
from schema.parking_schema import ParkingSchema
from file_datasource import AggregatedDatasource, AccelerometerFileDatasource, GpsFileDatasource, ParkingFileDatasource
import config


def connect_mqtt(broker, port):
    """Create MQTT client"""
    print(f"CONNECT TO {broker}:{port}")

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker ({broker}:{port})!")
        else:
            print("Failed to connect {broker}:{port}, return code %d\n", rc)
            exit(rc)  # Stop execution

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_start()
    return client


def publish(client, delay, datasource_infos):
    for datasource_info in datasource_infos:
        datasource_info[0].startReading()
    while True:
        time.sleep(delay)
        for datasource_info in datasource_infos:
            [datasource, topic, schema] = datasource_info
            data = datasource.read()
            msg = schema.dumps(data)
            result = client.publish(topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                pass
                # print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")


def run():
    # Prepare mqtt client
    client = connect_mqtt(config.MQTT_BROKER_HOST, config.MQTT_BROKER_PORT)
    # Prepare datasource
    aggregatedDatasource = AggregatedDatasource("data/accelerometer.csv", "data/gps.csv")
    accelerometerDatasource = AccelerometerFileDatasource("data/accelerometer.csv")
    gpsDatasource = GpsFileDatasource("data/gps.csv")
    parkingDatasource = ParkingFileDatasource("data/parking.csv")

    # Infinity publish data
    publish(client, config.DELAY, [
        [aggregatedDatasource, config.MQTT_TOPIC, AggregatedDataSchema()],
        [accelerometerDatasource, config.MQTT_ACCELEROMETER_TOPIC, AccelerometerSchema()],
        [gpsDatasource, config.MQTT_GPS_TOPIC, GpsSchema()],
        [parkingDatasource, config.MQTT_PARKING_TOPIC, ParkingSchema()]
    ])

if __name__ == "__main__":
    run()
