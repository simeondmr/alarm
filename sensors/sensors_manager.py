import time
from datetime import datetime
from server.request_handler import RequestHandler


class SensorsManager:
    def __init__(self, sensors):
        self.sensors = sensors

    def prepare_pkts(self, alarm_status):
        pkt = b''
        enabled_sensors = (sensor for sensor in self.sensors if sensor.enabled is True)
        for sensor in enabled_sensors:
            pkt += int(RequestHandler.DATA_PKT_HEADER).to_bytes(1, byteorder="little")
            pkt += int(time.mktime(datetime.now().timetuple())).to_bytes(4, byteorder="little")
            pkt += int(sensor.type.value).to_bytes(1, byteorder="little")
            pkt += int(alarm_status is True).to_bytes(1, byteorder="little")
            pkt += int(sensor.read()).to_bytes(2, byteorder="little")
        return pkt
