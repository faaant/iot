import config
from csv import reader
from datetime import datetime
from typing import Dict, Tuple
from domain.accelerometer import Accelerometer
from domain.aggregated_data import AggregatedData
from domain.gps import Gps


class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str) -> None:
        self.filenames = {
            "accelerometer": accelerometer_filename,
            "gps": gps_filename
        }
        self.row_counters = {datatype: 0 for datatype in self.filenames}
        self.file_contents = {datatype: [] for datatype in self.filenames}

    def read(self):
        data = {}
        for datatype in self.filenames:
            # infinite read
            self.row_counters[datatype] %= len(self.file_contents[datatype])
            data[datatype] = self.file_contents[datatype][self.row_counters[datatype]]
            # read next row
            self.row_counters[datatype] += 1
        time = datetime.now()
        accelerometer = Accelerometer(
            x=int(data["accelerometer"][0]),
            z=int(data["accelerometer"][2]),
            y=int(data["accelerometer"][1]),
        )
        gps = Gps(
            latitude=float(data["gps"][0]),
            longitude=float(data["gps"][1]),
        )
        return AggregatedData(accelerometer, gps, time, config.USER_ID) 

    def startReading(self, *args, **kwargs):
        for datatype in self.filenames:
            with open(self.filenames[datatype], "r") as file:
                self.file_contents[datatype] = list(reader(file))[1:]

    def stopReading(self, *args, **kwargs):
        self.row_counters = {datatype: 0 for datatype in self.filenames}
