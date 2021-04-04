from threading import Thread, Condition

from sensors.sensor import Sensor
from adafruit_ads1x15.analog_in import AnalogIn


"""All analog sensors must extends this class"""
class AnalogSensor(Sensor):

    """note: pin in this case refers to ADS1115 analog pin(range from 0 to 3)"""
    def __init__(self, pin, ads, type, calibration, enabled):
        super().__init__(pin, type, calibration, enabled)
        self.chan = AnalogIn(ads, pin)
        Thread.__init__(self)
        self.condition = Condition()

    """
    Thread for sensor monitoring.
    This thread must be wake up only after calibration,  if necessary
    """
    def run(self):
        if self.calibration:
            self.condition.acquire()
            self.condition.wait()
            self.condition.release()
        while True:
            self.trigger()

    """
    This method must be implement to execute some work,
    if the sensor reach some certain value.
    """
    def trigger(self):
        pass