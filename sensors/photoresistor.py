from sensors.sensor import Sensor, SensorType, CalibrationException


class Photoresistor(Sensor):

    def __init__(self, pin):
        super().__init__(pin, SensorType.PHOTORESISTOR)
        self.high = 0
        self.low = 0

    def check_calibration(self):
        if self.high >= self.low:
            raise CalibrationException

    def calibrate_min(self):
        self.low = self.read()

    def calibrate_max(self):
        if self.low != 0:
            self.high = self.read()
            if self.high >= self.low:
                raise CalibrationException
            self.condition.acquire()
            self.condition.notify()
            self.condition.release()
        else:
            raise CalibrationException
