import logging

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot

import view
from ui.MainWindow import Ui_MainWindow
from view.control import controlwidget, ThreadNetwork
from view.logs import logswidget
from view.manage import managewidget
from view.settings import settingswidget

from utils import constant


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, global_assets: dict):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)

        self.controlwidget: None | controlwidget = None
        self.managewidget: None | managewidget = None
        self.logswidget: None | logswidget = None
        self.settingswidget: None | settingswidget = None

        self.global_assets = global_assets

        self.setupUi(self)
        self.load_control()

        self.widget_loaded: view.MainWindow.MainWindow = self.controlwidget
        self.btn_pressed = self.controlbtn

        constant.LOGGER.setLevel(logging.INFO)

    @pyqtSlot()
    def on_controlbtn_clicked(self):
        self.btn_pressed.setEnabled(True)
        self.controlbtn.setDisabled(True)
        self.btn_pressed = self.controlbtn
        self.widget_loaded.hide()
        if not self.controlwidget:
            self.load_control()
        else:
            self.controlwidget.show()
        self.widget_loaded = self.controlwidget

    @pyqtSlot()
    def on_managebtn_clicked(self):
        self.btn_pressed.setEnabled(True)
        self.managebtn.setDisabled(True)
        self.btn_pressed = self.managebtn
        self.widget_loaded.hide()
        if not self.managewidget:
            self.load_manage()
        else:
            self.managewidget.show()
        self.widget_loaded = self.managewidget

    @pyqtSlot()
    def on_logsbtn_clicked(self):
        self.btn_pressed.setEnabled(True)
        self.logsbtn.setDisabled(True)
        self.btn_pressed = self.logsbtn
        self.widget_loaded.hide()
        if not self.logswidget:
            self.load_logs()
        else:
            self.logswidget.show()
        self.widget_loaded = self.logswidget

    @pyqtSlot()
    def on_settingsbtn_clicked(self):
        self.btn_pressed.setEnabled(True)
        self.settingsbtn.setDisabled(True)
        self.btn_pressed = self.settingsbtn
        self.widget_loaded.hide()
        if not self.settingswidget:
            self.load_settings()
        else:
            self.settingswidget.show()
        self.widget_loaded = self.settingswidget

    def load_control(self):
        self.controlwidget = controlwidget()
        self.contentlayout.addWidget(self.controlwidget)
        self.controlwidget.show()
        self.controlwidget.networkThread = ThreadNetwork(self, self.global_assets["model"])
        self.controlwidget.networkThread.updateStatusSignal.connect(self.controlwidget.updateStatus)
        self.controlwidget.networkThread.updateImageSignal.connect(self.controlwidget.updateImage)
        self.controlwidget.networkThread.updateTextSignal.connect(self.controlwidget.updateText)
        self.controlwidget.networkThread.start()

    def load_manage(self):
        self.managewidget = managewidget(self.global_assets)
        self.contentlayout.addWidget(self.managewidget)
        self.managewidget.show()
        self.managewidget.update_userswidget()

    def load_logs(self):
        self.logswidget = logswidget()
        constant.LOGGER.handlers[0].logstext = self.logswidget.logstext
        self.contentlayout.addWidget(self.logswidget)
        self.logswidget.show()

    def load_settings(self):
        self.settingswidget = settingswidget()
        self.contentlayout.addWidget(self.settingswidget)
        self.settingswidget.show()

    def closeEvent(self, event):
        if self.managewidget:
            self.managewidget.imageLoadThread.terminate()
        if self.controlwidget:
            self.controlwidget.networkThread.terminate()
