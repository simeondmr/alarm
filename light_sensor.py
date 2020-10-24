from sensor import Sensor


class LightSensor(Sensor):

    def __init__(self, pin):
        super().__init__(pin)

    def read_value(self):
        value = 0
        #TODO: read sensor value
        return value