from threading import Thread
import time
from socket import timeout

from alarm_observer import AlarmObserver


class RequestHandler(Thread, AlarmObserver):
    ACK = 0X00
    NAK = 0x01
    REQ_PKT_HEADER = 0x0a
    DATA_PKT_HEADER = 0x0b
    SAMPLING_TIME = 10

    def __init__(self, client, logger, sensors_manager, alarm_subject):
        Thread.__init__(self)
        AlarmObserver.__init__(self, alarm_subject)
        self._client = client
        self._logger = logger
        self.sensors_manager = sensors_manager
        self._client.settimeout(3)

    def read_presentation(self):
        if self._client.recv(1)[0] != self.REQ_PKT_HEADER:
            return self.NAK
        else:
            return self.ACK

    def send_pkt(self):
        try:
            self._client.send(self.sensors_manager.prepare_pkts(self.alarm_subject.alarm_status))
        except IOError:
            self.alarm_subject.detach(self)

    def update(self):
        self.send_pkt()

    def run(self):
        resp = self.read_presentation()
        self._client.send(int(resp).to_bytes(1, byteorder="little"))
        if resp == self.NAK:
            self._logger.info("Invalid request packet, connection closed")
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


