import RPi.GPIO as GPIO
from threading import Lock

from BuzzerAlarm import BuzzerAlarm
from photoresistor import Photoresistor
from time import sleep


class LightSensor(Photoresistor):
    CAPACITOR_DISCHARGE_TIME = 0.4
    SAMPLING_DELAY = 1
    APPROX_PRECISION = 500

    def __init__(self, pin):
        super().__init__(pin)
        self.mutex = Lock()
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        self.buzzer_alarm = BuzzerAlarm(35)

    def _trigger(self):
        current = self.read()
        print("current: " + str(current+500) + " low: " + str(self.low) + " high: " + str(self.high))
        if self.low > current + self.APPROX_PRECISION >= self.high and self.low > current - self.APPROX_PRECISION >= self.high:
            pass
        else:
            self.buzzer_alarm.alarm_sound()
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
