import logging
import os
import socket
import struct
import time
from utils.command import *

logging.basicConfig(level=logging.INFO)


class Client:
    server_socket: None | socket.socket

    def __init__(self, port, server_addr: tuple):
        self.port = port
        self.server_socket = None
        self.server_addr = server_addr

    def connect_server(self, max_retry=-1):
        assert max_retry
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.connect(self.server_addr)
            logging.info(f"Client: Connecting to Server at {self.server_addr}.")
            self.send_cmd(CMD_LINK)
        except ConnectionRefusedError:
            time.sleep(2)
            self.connect_server(max_retry - 1)
        except socket.error as e:
            logging.error(f"Client: Error {e} when connecting.")
            logging.info(f"Client: Try to reconnect")
            time.sleep(2)
            self.connect_server()

    def send_image(self, fp) -> bool:
        logging.info(f"Client: Sending image to {self.server_addr}.")
        try:
            fileinfo = struct.pack('128sq', str(int(time.time())).encode(), os.stat(fp).st_size)
            with open(fp, 'rb') as file:
                self.server_socket.send(fileinfo)
                while True:
                    data = file.read(1024)
                    if not data:
                        break
                    self.server_socket.send(data)
            logging.info(f"Client: Successfully send image to {self.server_addr}.")
            return True

        except socket.error as e:
            logging.error(f"Client: Error {e} when sending image")
            return False

    def send_message(self, message: str) -> bool:
        logging.info(f"Client: Sending message to {self.server_addr}.")
        try:
            self.server_socket.send(message.encode('utf-8'))
            logging.info(f"Client: Message {message} has been sent.")
            return True
        except socket.error as e:
            logging.error(f"Client: Error {e} when sending message")
            return False

    def send_cmd(self, command: bytes) -> bool:
        logging.info(f"Client: Sending command to {self.server_addr}.")
        try:
            self.server_socket.send(b'\x7E' + command + b'\xE7')
            return True
        except socket.error as e:
            logging.error(f"Client: Error {e} when sending command")
            return False

    def stop_service(self):
        if self.server_socket:
            self.server_socket.close()
            logging.info("Client: Service is successfully closed.")

    def reconnect(self, max_retry=-1):
        self.stop_service()
        self.connect_server(max_retry)
