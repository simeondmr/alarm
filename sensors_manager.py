import time
from datetime import datetime

from request_handler import RequestHandler


class SensorsManager:
    def __init__(self, sensors):
        self.sensors = sensors

    def prepare_pkts(self):
        pkt = b''
        for sensor in self.sensors:
            pkt += int(RequestHandler.DATA_PKT_HEADER).to_bytes(1, byteorder="little")
            pkt += int(time.mktime(datetime.now().timetuple())).to_bytes(4, byteorder="little")
            pkt += int(sensor.type.value).to_bytes(1, byteorder="little")
            pkt += int(sensor.is_alarm_on is True).to_bytes(1, byteorder="little")
            pkt += sensor.read().to_bytes(4, byteorder="little")
        return pkt
