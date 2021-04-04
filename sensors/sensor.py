from enum import Enum
from threading import Thread, Condition

"""General sensor class, every physical sensors must extends this class"""
class Sensor:
    def __init__(self, pin, type, calibration, enabled):
        Thread.__init__(self)
        self.pin = pin
        self.type = type
        self.condition = Condition()
        self.calibration = calibration
        self.enabled = enabled

    """
    return the sensor value
    """
    def read(self):
        pass

"""Enum containing all sensors in use"""
class SensorType(Enum):
    PHOTORESISTOR = 1
    THERMISTOR = 2
    PASSIVE_INFRARED = 3

"""Use this exception if a sensor calibration fail"""
class CalibrationException(Exception):
    pass