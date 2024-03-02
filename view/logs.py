import logging

from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget

from ui.logs import Ui_logswidget
from utils import constant


class logswidget(QWidget, Ui_logswidget):
    def __init__(self):
        QWidget.__init__(self)
        Ui_logswidget.__init__(self)
        self.setupUi(self)

        self.btn_pressed = self.infobtn

    @pyqtSlot()
    def on_infobtn_clicked(self):
        self.btn_pressed.setEnabled(True)
        self.infobtn.setDisabled(True)
        self.btn_pressed = self.infobtn
        constant.LOGGER.handlers[0].setLevel(logging.INFO)

    @pyqtSlot()
    def on_warningbtn_clicked(self):
        self.btn_pressed.setEnabled(True)
        self.warningbtn.setDisabled(True)
        self.btn_pressed = self.warningbtn
        constant.LOGGER.handlers[0].setLevel(logging.WARNING)

    @pyqtSlot()
    def on_errorbtn_clicked(self):
        self.btn_pressed.setEnabled(True)
        self.errorbtn.setDisabled(True)
        self.btn_pressed = self.errorbtn
        constant.LOGGER.handlers[0].setLevel(logging.ERROR)

    @pyqtSlot()
    def on_clearbtn_clicked(self):
        self.logstext.clear()


class LoggingHandler(logging.Handler, QObject):
    logSignal = pyqtSignal(str)

    def __init__(self):
        logging.Handler.__init__(self)
        QObject.__init__(self)
        self.setFormatter(logging.Formatter(
            fmt='pid: %(thread)d %(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(''message)s',
            datefmt='%Y-%m-%d %H:%M:%S'))

    def emit(self, record):
        self.logSignal.emit(self.format(record))
