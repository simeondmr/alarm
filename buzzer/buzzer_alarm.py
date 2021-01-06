from time import sleep
from RPi import GPIO


class BuzzerAlarm:
    DELAY = 0.0001
    N_SOUND = 1000

    def __init__(self, pin):
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
        self.pin = pin

    def alarm_sound(self):
        for i in range(0, self.N_SOUND):
            GPIO.output(self.pin, GPIO.HIGH)
            sleep(self.DELAY)
            GPIO.output(self.pin, GPIO.LOW)
            sleep(self.DELAY)