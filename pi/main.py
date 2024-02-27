import os
import sys
import time
import logging
import subprocess
from utils.network import server, client
from utils.command import *
from utils.model import tts

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(''message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

sys.path.append("..")

"""
0. read configuration
1. PC -- connect request --> pi
2. PC -- cmd --> pi
3. pi -- image --> PC
4. PC -- message --> pi
"""
pic_path = "../IRpic"


def load_conf():
    pass


def init_server() -> server.Server:
    s = server.Server(6666)
    logging.info("pi(Server): Waiting for PC to connect.")
    s.start_service()
    s.client_addr = (s.client_addr[0], 6666)
    return s


def init_client(server_addr) -> client.Client:
    c = client.Client(6665, server_addr)
    c.connect_server()
    return c


def shot(sock: client.Client):
    logging.info("pi(Client): Shotting image.")
    temp_file = f"{pic_path}/temp.jpg"
    process = subprocess.Popen(f"libcamera-jpeg --autofocus-mode continuous -o {temp_file} -t 2 >/dev/null 2>&1",
                               shell=True)
    process.wait()
    file = f"{pic_path}/{int(time.time())}.jpg"
    os.rename(temp_file, file)
    fp = os.path.join(pic_path, file)
    logging.info("pi(Client): Sending image.")
    if not sock.send_image(fp):
        logging.warning("pi(Client): Failed to send image.")
    os.remove(fp)


def speak(s: server.Server, c: client.Client):
    tts.speak(s.recv_message())
    c.send_cmd(CMD_FIN)


if __name__ == "__main__":
    while True:
        s = init_server()
        c = init_client(s.client_addr)
        while True:
            cmd = s.recv_cmd()
            if not cmd:
                logging.error("pi(Server): Connection lost.")
                logging.info("pi(Server): Trying to reconnect.")
                s.reconnect()
                c.reconnect()
            elif cmd == CMD_SHOT:
                shot(c)
            elif cmd == CMD_SPEAK:
                speak(s, c)
            elif cmd == CMD_EXIT:
                s.stop_service()
                logging.info("pi(Server): Program terminated gracefully.")
                break
            else:
                logging.warning("pi(Server): Unkown command.")
