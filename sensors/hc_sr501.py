from RPi import GPIO

from sensors.digital_sensor import DigitalSensor


class HCSR501(DigitalSensor):
    def __init__(self, pin, type, subject, calibration, enabled):
        super().__init__(pin, type, calibration, enabled)
        self.subject = subject
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(pin, GPIO.BOTH, callback=self.event_callback)

    def event_callback(self, channel):
        if GPIO.input(channel):
            self.subject.set_alarm_status(True)
        else:
            self.subject.set_alarm_status(False)
        self.subject.notify_all()

    def read(self):
        if GPIO.input(self.pin):
            return 1
        return 0
