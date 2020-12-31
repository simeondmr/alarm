"""Subject of patter Observer"""
class AlarmSubject:
    def __init__(self):
        self.alarm_status = False
        self.observers = []

    def attach(self, observer):
        self.observers += [observer]

    def detach(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def set_alarm_status(self, alarm_status):
        self.alarm_status = alarm_status

    def notify_all(self):
        for observer in self.observers:
            observer.update()