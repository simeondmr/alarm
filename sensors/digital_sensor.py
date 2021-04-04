from sensors.sensor import Sensor

"""All digital sensors must extends this class"""
class DigitalSensor(Sensor):
    def __init__(self, pin, type, calibration, enabled):
        super().__init__(pin, type, calibration, enabled)

    def event_callback(self, channel):
        pass