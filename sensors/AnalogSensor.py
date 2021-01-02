from sensors.sensor import Sensor
from adafruit_ads1x15.analog_in import AnalogIn


"""All analog sensors must extends this class"""
class AnalogSensor(Sensor):

    """note: pin in this case refers to ADS1115 analog pin(range from 0 to 3)"""
    def __init__(self, pin, ads, type, calibration):
        super().__init__(pin, type, calibration)
        self.chan = AnalogIn(ads, pin)