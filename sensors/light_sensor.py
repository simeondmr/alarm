from buzzer.buzzer_alarm import BuzzerAlarm
from sensors.photoresistor import Photoresistor
from time import sleep


class LightSensor(Photoresistor):
    SAMPLING_DELAY = 1
    BUZZER_ALARM_PIN = 19

    def __init__(self, pin, ads, subject, calibration):
        super().__init__(pin, ads, calibration)
        self.buzzer_alarm = BuzzerAlarm(self.BUZZER_ALARM_PIN)
        self.subject = subject

    def trigger(self):
        current = self.read()
        print("current: " + str(current) + " low: " + str(self.low) + " high: " + str(self.high))
        if self.low >= current >= self.high:
            self.subject.set_alarm_status(False)
        else:
            self.subject.set_alarm_status(True)
            self.buzzer_alarm.alarm_sound()
            self.subject.notify_all()
        sleep(self.SAMPLING_DELAY)

    def read(self):
        return self.chan.value