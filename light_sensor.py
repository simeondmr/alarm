import RPi.GPIO as GPIO
from threading import Lock
from photoresistor import Photoresistor
from time import sleep


class LightSensor(Photoresistor):
    CAPACITOR_DISCHARGE_TIME = 0.3
    SAMPLING_DELAY = 1

    def __init__(self, pin):
        super().__init__(pin)
        self.mutex = Lock()
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

    def _trigger(self):
        current = self.read()
        if self.low > current >= self.high:
            #TODO: stop beep alarm
            pass
        else:
            #TODO: beep alarm
            pass
        sleep(self.SAMPLING_DELAY)

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
