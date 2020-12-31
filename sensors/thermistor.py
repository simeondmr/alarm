from sensors.sensor import Sensor, SensorType


class Thermistor(Sensor):
    def __init__(self, pin):
        super().__init__(pin, SensorType.THERMISTOR)
        self.high = 0
        self.low = 0

