from sensors.AnalogSensor import AnalogSensor
from sensors.sensor import Sensor, SensorType, CalibrationException


class Photoresistor(AnalogSensor):

    def __init__(self, pin, ads, calibration):
        super().__init__(pin, ads, SensorType.PHOTORESISTOR, calibration)
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
