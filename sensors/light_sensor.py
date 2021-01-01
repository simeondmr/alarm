import RPi.GPIO as GPIO
from threading import Lock

from buzzer.buzzer_alarm import BuzzerAlarm
from sensors.photoresistor import Photoresistor
from time import sleep


class LightSensor(Photoresistor):
    CAPACITOR_DISCHARGE_TIME = 0.4
    SAMPLING_DELAY = 1
    APPROX_PRECISION = 500
    BUZZER_ALARM_PIN = 35

    def __init__(self, pin, subject):
        super().__init__(pin)
        self.mutex = Lock()
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        self.buzzer_alarm = BuzzerAlarm(self.BUZZER_ALARM_PIN)
        self.subject = subject

    def trigger(self):
        current = self.read()
        print("current: " + str(current) + " low: " + str(self.low) + " high: " + str(self.high))
        if self.low > current >= self.high and self.low > current >= self.high:
            self.subject.set_alarm_status(False)
        else:
            self.subject.set_alarm_status(True)
            self.buzzer_alarm.alarm_sound()
            self.subject.notify_all()
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
