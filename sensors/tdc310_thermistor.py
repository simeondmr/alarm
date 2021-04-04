from math import log

from sensors.thermistor import Thermistor
from time import sleep

"""This class implement the thermistor TDC310"""
class TDC310Thermistor(Thermistor):
    DIVIDER_RESISTENCE = 10000
    VOLT_IN = 5.0

    #note: Steinhart–Hart coefficients A, B and C should be adjusted experimentally
    A = 1.159148e-3
    B = 2.34125e-4
    C = 8.76741e-8

    DISSIPPATION_FACTOR = 6
    N_SAMPLES = 5
    SAMPLING_DELAY = 0.01
    READ_DELAY = 0.01

    def __init__(self, pin, ads, subject, calibration, enabled):
        super().__init__(pin, ads, calibration, enabled)
        self.subject = subject

    def trigger(self):
        pass

    def __steinhart_hart(self, resistence):
        log_resistence = log(resistence)
        return 1.0 / (self.A + self.B * log_resistence + self.C * pow(log_resistence, 3))

    def read(self):
        volt = 0
        for i in range(0, self.N_SAMPLES):
            volt += self.chan.voltage
            sleep(self.READ_DELAY)
        volt /= self.N_SAMPLES
        curr_thr_res = (self.DIVIDER_RESISTENCE * volt) / (self.VOLT_IN - volt)
        return (self.__steinhart_hart(curr_thr_res) - volt * volt / (self.DISSIPPATION_FACTOR * curr_thr_res)) - 273.15



