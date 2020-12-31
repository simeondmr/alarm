"""Observer entity of the pattern Observer"""
class AlarmObserver:
    def __init__(self, alarm_subject):
        self.alarm_subject = alarm_subject

    def update(self):
        pass
