import os
import socket
import struct
import time

from utils import constant
from utils.command import *


class Client:
    server_socket: None | socket.socket

    def __init__(self, port, server_addr: tuple):
        self.port = port
        self.server_socket = None
        self.server_addr = server_addr
        self.stop: bool = False

    def connect_server(self, max_retry=-1):
        if self.stop:
            return
        assert max_retry
        try:
            constant.LOGGER.info(f"Client: Connecting to Server at {self.server_addr}.")
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.connect(self.server_addr)
            self.send_cmd(CMD_LINK)
        except ConnectionRefusedError:
            if not self.stop:
                time.sleep(2)
                self.connect_server(max_retry - 1)
        except socket.error as e:
            constant.LOGGER.error(f"Client: Error {e} when connecting.")
            constant.LOGGER.info(f"Client: Try to reconnect")
            time.sleep(2)
            self.connect_server()

    def send_image(self, fp) -> bool:
        constant.LOGGER.info(f"Client: Sending image to {self.server_addr}.")
        try:
            fileinfo = struct.pack('128sq', str(int(time.time())).encode(), os.stat(fp).st_size)
            with open(fp, 'rb') as file:
                self.server_socket.send(fileinfo)
                while True:
                    data = file.read(1024)
                    if not data:
                        break
                    self.server_socket.send(data)
            constant.LOGGER.info(f"Client: Successfully send image to {self.server_addr}.")
            return True

        except socket.error as e:
            constant.LOGGER.error(f"Client: Error {e} when sending image")
            return False

    def send_message(self, message: str) -> bool:
        constant.LOGGER.info(f"Client: Sending message to {self.server_addr}.")
        try:
            self.server_socket.send(message.encode('utf-8') + b'\x7E')
            constant.LOGGER.info(f"Client: Message {message} has been sent.")
            return True
        except socket.error as e:
            constant.LOGGER.error(f"Client: Error {e} when sending message")
            return False

    def send_cmd(self, command: bytes) -> bool:
        constant.LOGGER.info(f"Client: Sending command to {self.server_addr}.")
        try:
            self.server_socket.send(command + b'\xE7')
            return True
        except socket.error as e:
            constant.LOGGER.error(f"Client: Error {e} when sending command")
            return False

    def stop_service(self):
        if self.server_socket:
            self.server_socket.close()
            constant.LOGGER.info("Client: Service is successfully closed.")

    def reconnect(self, max_retry=-1):
        self.stop_service()
        self.connect_server(max_retry)
