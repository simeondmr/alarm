import RPi.GPIO as GPIO
from threading import Lock
from photoresistor import Photoresistor
from time import sleep


class LightSensor(Photoresistor):
    CAPACITOR_DISCHARGE_TIME = 0.3

    def __init__(self, pin):
        self.pin = pin
        self.mutex = Lock()
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

    def read(self):
        self.mutex.acquire()
        try:
            counter = 0
            GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)
            sleep(self.CAPACITOR_DISCHARGE_TIME)
            GPIO.setup(self.pin, GPIO.IN)
            while GPIO.input(self.pin) == GPIO.LOW:
                counter += 1
            return counter
        finally:
            self.mutex.release()
