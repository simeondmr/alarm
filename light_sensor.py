from sensor import Sensor


class LightSensor(Sensor):

    def __init__(self, pin):
        super().__init__(pin)

    def read(self):
        value = bytes(0)
        #TODO: read sensor value
        return value