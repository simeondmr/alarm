from sensors.AnalogSensor import AnalogSensor
from sensors.sensor import SensorType


class Thermistor(AnalogSensor):
    def __init__(self, pin, ads, calibration):
        super().__init__(pin, ads, SensorType.THERMISTOR, calibration)
        self.high = 0
        self.low = 0

