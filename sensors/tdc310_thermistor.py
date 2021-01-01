from math import log

from sensors.thermistor import Thermistor
from time import sleep

"""This class implement the thermistor TDC310"""
class TDC310Thermistor(Thermistor):
    DIVIDER_RESISTENCE = 10000
    VOLT_IN = 5
    A = 1.189148e-3
    B = 8.76741e-8
    C = 8.76741e-8
    DISSIPPATION_FACTOR = 6
    N_SAMPLES = 5
    SAMPLING_DELAY = 0.01

    def __init__(self, pin, subject):
        super().__init__(pin)

    def __steinhart_hart(self, resistence):
        log_resistence = log(resistence)
        return 1.0 / (self.A + self.B + log_resistence + self.C * pow(log_resistence, 3))

    def read(self):
        value = 0.0
        for i in range(0, self.N_SAMPLES):
            #value += analogRead(pin)
            sleep(self.READ_DELAY)
        value /= self.NSAMPLES
        curr_volt = value / 1024 * self.VOLT_IN
        curr_thr_res = (self.DIVIDER_RESISTENCE * curr_volt) / (self.VOLT_IN - curr_volt)
        return self.__steinhart_hart(curr_thr_res) - curr_volt * curr_volt / (self.DISSIPPATION_FACTOR * curr_thr_res)


