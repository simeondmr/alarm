from threading import Thread
import time
from datetime import datetime
from light_sensor import LightSensor
from socket import timeout

class RequestHandler(Thread):
    ACK = 0X00
    NAK = 0x01
    REQ_PKT_HEADER = 0x0a
    DATA_PKT_HEADER = 0x0b
    LIGHT_SENSOR_PIN = 10
    SAMPLING_TIME = 10

    def __init__(self, client, logger):
        Thread.__init__(self)
        self._client = client
        self._logger = logger
        self.sensor = LightSensor(self.LIGHT_SENSOR_PIN)
        self._client.settimeout(3)

    def read_presentation(self):
        if self._client.recv(1)[0] != self.REQ_PKT_HEADER:
            return self.NAK
        else:
            return self.ACK

    def send_pkt(self):
        pkt = int(self.DATA_PKT_HEADER).to_bytes(1, byteorder="little")
        pkt += int(time.mktime(datetime.now().timetuple())).to_bytes(4, byteorder="little")
        pkt += self.sensor.read()
        self._client.send(pkt)

    def run(self):
        resp = self.read_presentation()
        self._client.send(int(resp).to_bytes(1, byteorder="little"))
        if resp == self.NAK:
            self._logger.info("Invalid request packet")
            return
        self._logger.info("Presentation accepted")
        while True:
            try:
                self.send_pkt()
                response = self._client.recv(1)
            except timeout:
                self._logger.info("Error: timeout")
                break
            if int.from_bytes(response, byteorder="little") != self.ACK:
                print("error ack")
                self._logger.info("Error: ACK not receiver")
                return
            print("ACK received")
            time.sleep(self.SAMPLING_TIME)


