from socket import *
from request_handler import RequestHandler
import logging


class Server:
    def __init__(self, host, port):
        self._server = socket(AF_INET, SOCK_STREAM)
        self._server.bind((host, port))
        self._server.listen(5)
#        logging.basicConfig(filename='Alarm.log', encoding='utf-8', level=logging.INFO)

    def listen(self):
        while True:
            logging.info("Wait for a new connection...")
            (client, address) = self._server.accept()
            request_handler = RequestHandler(client, logging)
            request_handler.start()

