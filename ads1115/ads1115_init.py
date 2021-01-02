import board
import busio
import adafruit_ads1x15.ads1115 as adafruit_ads1115

"""Initialization class for ADS1115"""
class ADS1115Init:
    def __init__(self, gain):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = adafruit_ads1115.ADS1115(i2c)
        self.ads.gain = gain
