from sensors.sensor import Sensor

"""All digital sensors must extends this class"""
class DigitalSensor(Sensor):
    def __init__(self, pin, type, calibration):
        super().__init__(pin, type, calibration)