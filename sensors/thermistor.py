from sensors.AnalogSensor import AnalogSensor
from sensors.sensor import SensorType


class Thermistor(AnalogSensor):
    def __init__(self, pin, ads, calibration, enabled):
        super().__init__(pin, ads, SensorType.THERMISTOR, calibration, enabled)

