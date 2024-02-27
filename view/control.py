import logging
import os
import time

import cv2
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QGraphicsScene
from numpy import ndarray

from ui.control.control import Ui_controlwidget
from utils import constant
from utils.command import *
from utils.database import Database
from utils.network import client, server


class STATE:
    online = 1
    pending = 2
    offline = 3


class controlwidget(QWidget, Ui_controlwidget):
    IMAGE_WDITH = 604
    IMAGE_HEIGHT = 454

    def __init__(self):
        QWidget.__init__(self)
        Ui_controlwidget.__init__(self)
        self.setupUi(self)

        self.ip.setText(constant.PATH_PI_ADDR[0])

        self._image: None | ndarray = None
        self.scene = QGraphicsScene()
        self.image.setScene(self.scene)

        self.ip.textChanged.connect(self.on_ip_changed)
        self.switchbtn.mousePressEvent = self.switch

        self.networkThread: None | ThreadNetwork = None

    def switch(self, event):
        if self.statustext.text() == "在线":
            self.switchbtn.state = not self.switchbtn.state
            self.networkThread.service_on = self.switchbtn.state
            self.switchbtn.update()

    def on_ip_changed(self):
        constant.PATH_PI_ADDR = (self.ip.text(), 6666)

    @pyqtSlot()
    def on_connectbtn_clicked(self):
        if self.connectbtn.text() == "连接":
            self.networkThread.connectCMD = True
            self.updateStatus(STATE.pending)
        elif self.connectbtn.text() == "取消":
            self.networkThread.c.stop = True
        else:
            self.networkThread.disconnectCMD = True

    @pyqtSlot()
    def on_savebtn_clicked(self):
        cv2.imwrite(f"{constant.PATH_SAVE}/{int(time.time())}.jpg", self._image)

    def updateStatus(self, state: int):
        if state == STATE.online:
            self.statuslabel.setStyleSheet("border-radius: 6px;\n"
                                           "background: #98C075")
            self.statustext.setText("在线")
            self.connectbtn.setStyleSheet("background-color: #ED7161;\n"
                                          "color: rgb(255, 255, 255);\n"
                                          "border-radius: 5px;\n"
                                          "padding: 5px 5px;\n"
                                          "margin: 5px 10px;\n"
                                          "font: 75 9pt \"思源黑体 CN Bold\";")
            self.connectbtn.setText("断开")
            self.switchbtn.state = False
            self.switchbtn.update()
        elif state == STATE.pending:
            self.statuslabel.setStyleSheet("border-radius: 6px;\n"
                                           "background: #E4E8EC")
            self.statustext.setText("连接中")
            self.connectbtn.setStyleSheet("background-color: #E4E8EC;\n"
                                          "color: rgb(255, 255, 255);\n"
                                          "border-radius: 5px;\n"
                                          "padding: 5px 5px;\n"
                                          "margin: 5px 10px;\n"
                                          "font: 75 9pt \"思源黑体 CN Bold\";")
            self.connectbtn.setText("取消")
        else:
            self.networkThread.service_on = False
            self.statuslabel.setStyleSheet("border-radius: 6px;\n"
                                           "background: #ED7161")
            self.statustext.setText("离线")
            self.connectbtn.setStyleSheet("background-color: #98C075;\n"
                                          "color: rgb(255, 255, 255);\n"
                                          "border-radius: 5px;\n"
                                          "padding: 5px 5px;\n"
                                          "margin: 5px 10px;\n"
                                          "font: 75 9pt \"思源黑体 CN Bold\";")
            self.connectbtn.setText("连接")
            self.switchbtn.state = False
            self.switchbtn.update()

    def updateImage(self, image: ndarray, imagecvt: ndarray):
        self._image = image
        self.scene.clear()
        self.scene.addPixmap(QPixmap.fromImage(QImage
                                                   (imagecvt, self.IMAGE_WDITH, self.IMAGE_HEIGHT,
                                                    QImage.Format_BGR888)))

    def updateText(self, name: str):
        self.nametext.setText(name)


class ThreadNetwork(QThread):
    updateStatusSignal = pyqtSignal(int)
    updateImageSignal = pyqtSignal(ndarray, ndarray)
    updateTextSignal = pyqtSignal(str)

    connectCMD: bool = False
    disconnectCMD: bool = False
    service_on: bool = False

    def __init__(self, parent, model):
        QThread.__init__(self, parent)
        self.c = client.Client(6665, constant.PATH_PI_ADDR)
        self.s: None | server.Server = None
        self.retry = 0
        self.model = model

    def run(self) -> None:
        #  setup
        db = Database()
        #  mainloop
        while True:
            time.sleep(1)
            if self.connectCMD:
                self.connectCMD = False
                self.c.stop = False
                self._connect()

            if self.disconnectCMD:
                self.disconnectCMD = False
                self._disconnect()

            if self.service_on:
                uid = None
                if not self.c.send_cmd(CMD_SHOT) or self.retry > constant.MAX_RETRY:
                    self.retry = 0
                    constant.LOGGER.info("PC(Server): Trying to reconnect.")
                    self.reconnect(constant.MAX_RETRY)
                    continue
                new_fp = self.s.recv_image(constant.PATH_WORK_DIR)
                if not new_fp:
                    constant.LOGGER.warning("PC(Client): Retry.")
                    time.sleep(2)
                    self.retry += 1
                    continue
                else:
                    image = cv2.imread(new_fp)
                    imagecvt = cv2.resize(image, (controlwidget.IMAGE_WDITH, controlwidget.IMAGE_HEIGHT))
                    self.updateImageSignal.emit(image, imagecvt)
                    uid = self.model.predict(new_fp)
                    os.remove(new_fp)
                if not uid:
                    self.updateTextSignal.emit("未识别到人像")
                else:
                    if uid == -1:
                        result = "陌生人"
                    else:
                        result = db.query_by_uid(uid)
                    self.updateTextSignal.emit(result)
                    message = constant.MESSAGE.format(result)
                    if not (self.c.send_cmd(CMD_SPEAK) and self.c.send_message(message)):
                        self.reconnect(constant.MAX_RETRY)
                        continue
                    try:
                        self.s.client_socket.settimeout(60)
                        assert self.s.recv_cmd() == CMD_FIN
                    except (AssertionError, TimeoutError):
                        logging.error("PC(Server): Speaking timeout.")
                        logging.info("PC(Server): Trying to reconnect.")
                        self.reconnect(constant.MAX_RETRY)
                        continue

    def _connect(self):
        self.init_client(constant.PATH_PI_ADDR)
        if self.c.stop:
            self.updateStatusSignal.emit(STATE.offline)
            return
        self.init_server()
        self.updateStatusSignal.emit(STATE.online)

    def _disconnect(self):
        self.c.send_cmd(CMD_EXIT)
        constant.LOGGER.info("PC: Disconnected.")
        self.updateStatusSignal.emit(STATE.offline)

    def init_client(self, server_addr):
        self.c.server_addr = server_addr
        logging.info("PC(Client): Connecting to pi.")
        self.c.connect_server()

    def init_server(self):
        self.s = server.Server(6666)
        self.s.start_service()

    def reconnect(self, max_retry=5):
        self.updateStatusSignal.emit(STATE.pending)
        retry = 0
        for retry in range(1, max_retry + 1):
            try:
                self.c.reconnect(max_retry=5)
                self.s.reconnect(timeout=5)
                self.updateStatusSignal.emit(STATE.online)
                break
            except (TimeoutError, AssertionError):
                pass
        if self.c.stop or retry == max_retry:
            logging.warning("PC(Client): pi is offline.")
            self.updateStatusSignal.emit(STATE.offline)
