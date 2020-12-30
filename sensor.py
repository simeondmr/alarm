from enum import Enum
from threading import Thread, Condition

"""General sensor class, every physical sensors must extends this class"""
class Sensor(Thread):
    def __init__(self, pin, type):
        Thread.__init__(self)
        self.pin = pin
        self.type = type
        self.condition = Condition()

    """
    Thread for sensor monitoring.
    This thread must be wake up only after calibration
    """
    def run(self):
        self.condition.acquire()
        self.condition.wait()
        self.condition.release()
        while True:
            self._trigger()

    """
    This method must be implement to execute some work,
    if the sensor reach some certain value.
    """
    def _trigger(self):
        pass

    """
    return the sensor value
    """
    def read(self):
        pass

"""Enum containing all sensors in use"""
class SensorType(Enum):
    PHOTORESISTOR = 1

"""Use this exception if a sensor calibration fail"""
class CalibrationException(Exception):
    pass