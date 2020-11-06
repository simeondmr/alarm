from enum import Enum


class Sensor:
    def __init__(self, pin, type):
        self.pin = pin
        self.type = type

    def read(self):
        pass


class SensorType(Enum):
    PHOTORESISTOR = 1