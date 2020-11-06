from sensor import Sensor, SensorType


class Photoresistor(Sensor):

    def __init__(self, pin):
        super().__init__(pin, SensorType.PHOTORESISTOR)
        self.high = None
        self.low = None

    def is_light_on(self):
        if self.read() > self.low:
            return True
        return False

    def calibrate_nolight(self):
        self.low = self.read()

    def calibrate_maxlight(self):
        self.high = self.read()