from threading import Thread


class RequestHandler(Thread):
    ACK = 0X00
    NAK = 0x01
    REQ_PKT_HEADER = 0x0a

    def __init__(self, client, logger):
        Thread.__init__(self)
        self._client = client
        self._logger = logger

    def read_pkt(self):
        data = []
        while True:
            new_data = self._client.recv(512)
            if len(new_data) < 1:
                break
            data += new_data
        return data

    def read_presentation(self):
        if self._client.recv(1)[0] != self.REQ_PKT_HEADER:
            return self.NAK
        else:
            return self.ACK

    def run(self):
        resp = self.read_presentation()
        self._client.send(bytes(resp))
        if resp == self.NAK:
            self._logger.info("Invalid request packet")
            return
        self._logger.info("Presentation accepted")

        #print(int(time.mktime(datetime.now().timetuple())).to_bytes(4, byteorder = "little"))
        #print(int.from_bytes(int(time.mktime(datetime.now().timetuple())).to_bytes(4, byteorder = "little"), byteorder= "little"))


