import os
import sys
import socket
import logging
import struct

from utils.command import *

logging.basicConfig(level=logging.INFO)


class Buffer:
    def __init__(self, sock: socket.socket):
        self.sock = sock
        self.buffer = b''

    def recv_until(self, mark: bytes):
        while mark not in self.buffer:
            data = self.sock.recv(1024)
            if not data:
                break
            self.buffer += data
        line, _, self.buffer = self.buffer.partition(mark)
        return line

    def recv(self, size):
        line = self.buffer
        if size <= len(line):
            self.buffer = self.buffer[size:-1]
            return line[:size]
        data = self.sock.recv(size - len(line))
        line += data
        self.buffer = b''
        return line

    def clear(self):
        self.sock.setblocking(False)
        while True:
            try:
                assert self.sock.recv(1024)
            except (AssertionError, BlockingIOError):
                break
        self.sock.setblocking(True)
        self.buffer = b''


class Server:
    client_socket: socket.socket | None
    tcp_server: socket.socket | None
    buffer: Buffer | None

    def __init__(self, port):
        self.buffer = None
        self.port = port
        self.client_socket = None
        self.tcp_server = None
        self.client_addr = None

    def start_service(self, timeout: float | None = None):
        self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_server.bind(('', self.port))
        self.tcp_server.listen(128)
        self.tcp_server.settimeout(timeout)
        self.client_socket, self.client_addr = self.tcp_server.accept()
        self.tcp_server.settimeout(None)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.buffer = Buffer(self.client_socket)
        logging.info(f"Server: Client at {self.client_addr} is connect.")
        try:
            assert self.recv_cmd() == CMD_LINK
        except AssertionError:
            logging.error("Server: Failed to establish a secure connection.")
            sys.exit(0)

    def recv_image(self, _fp) -> str | None:
        logging.info(f"Server: Receiving image from {self.client_addr}.")
        self.client_socket.settimeout(2)
        try:
            fileinfo_size = struct.calcsize('128sq')
            buf = self.buffer.recv(fileinfo_size)
            assert buf
            filename, filesize = struct.unpack('128sq', buf)
            fp = os.path.join(_fp, filename.decode().strip('\x00') + '.jpg')
            file = open(fp, 'wb')
            recv_size = 0
            while not recv_size == filesize:
                if filesize - recv_size > 1024:
                    data = self.buffer.recv(1024)
                    recv_size += len(data)
                else:
                    data = self.buffer.recv(1024)
                    recv_size = filesize
                if not data:
                    file.close()
                    os.remove(fp)
                    raise TimeoutError
                file.write(data)
            file.close()
            logging.info(f"Server: Successfully received image {fp}.")
            self.client_socket.settimeout(None)
            return fp

        except (OSError, UnicodeDecodeError, struct.error) as e:
            logging.error(f"Server: Error {e} when receiving image")
            # flush
            self.buffer.clear()
            self.client_socket.settimeout(None)
            return None

        except (socket.error, AssertionError, TimeoutError) as e:
            logging.error(f"Server: Error {e} when receiving image")
            self.client_socket.settimeout(None)
            return None

    def recv_message(self):
        logging.info(f"Server: Receiving message from {self.client_addr}.")
        message = None
        try:
            message = self.buffer.recv_until(b'\x7E').decode('utf-8')
        except (socket.error, OSError, UnicodeDecodeError) as e:
            logging.error(f"Server: Error {e} when receiving message")
        return message

    def recv_cmd(self):
        logging.info(f"Server: Receiving command from {self.client_addr}.")
        command = None
        try:
            command = self.buffer.recv_until(b'\xE7').split(b'\x7E')[-1]
        except (socket.error, OSError) as e:
            logging.error(f"Server: Error {e} when receiving command")
        return command

    def stop_service(self):
        if self.client_socket:
            self.client_socket.close()
        if self.tcp_server:
            self.tcp_server.close()
        logging.info("Server: Service is successfully closed.")

    def reconnect(self, timeout: float | None = None):
        self.stop_service()
        self.start_service(timeout)
