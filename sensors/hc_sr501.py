from time import sleep

from RPi import GPIO

from sensors.digital_sensor import DigitalSensor


class HCSR501(DigitalSensor):
    def __init__(self, pin, type, subject, calibration):
        super().__init__(pin, type, calibration)
        GPIO.setup(self.pin, GPIO.IN)
        self.subject = subject

    def trigger(self):
        if GPIO.input(self.pin):
            self.subject.set_alarm_status(True)
            self.subject.notify_all()
            sleep(1)

    def read(self):
        if GPIO.input(self.pin):
            return 1
        return 0