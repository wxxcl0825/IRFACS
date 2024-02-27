from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget

from ui.settings import Ui_settingswidget
from utils import constant
from utils.ui import chooseFile, chooseDir


class settingswidget(QWidget, Ui_settingswidget):
    def __init__(self):
        QWidget.__init__(self)
        Ui_settingswidget.__init__(self)
        self.setupUi(self)
        self.loadConstant()

    @pyqtSlot()
    def on_modelpathbtn_clicked(self):
        chooseFile(self, self.modelpath.text(), "Pickle dumped file (*.pkl)", self.modelpath)

    @pyqtSlot()
    def on_dbpathbtn_clicked(self):
        chooseFile(self, self.dbpath.text(), "Database file (*.db)", self.dbpath)

    @pyqtSlot()
    def on_templatepathbtn_clicked(self):
        chooseDir(self, self.templatepath.text(), self.templatepath)

    @pyqtSlot()
    def on_workpathbtn_clicked(self):
        chooseDir(self, self.workpath.text(), self.workpath)

    @pyqtSlot()
    def on_savepathbtn_clicked(self):
        chooseDir(self, self.savepath.text(), self.savepath)

    @pyqtSlot()
    def on_confirmbtn_clicked(self):
        constant.PATH_MODEL = self.modelpath.text()
        constant.PATH_DB = self.dbpath.text()
        constant.PATH_TEMPLATE_DIR = self.templatepath.text()
        constant.PATH_WORK_DIR = self.workpath.text()
        constant.PATH_SAVE = self.savepath.text()
        constant.MAX_RETRY = int(self.maxretry.text())
        constant.MESSAGE = self.message.text()

    @pyqtSlot()
    def on_resetbtn_clicked(self):
        self.loadConstant()

    def loadConstant(self):
        self.modelpath.setText(constant.PATH_MODEL)
        self.dbpath.setText(constant.PATH_DB)
        self.templatepath.setText(constant.PATH_TEMPLATE_DIR)
        self.workpath.setText(constant.PATH_WORK_DIR)
        self.savepath.setText(constant.PATH_SAVE)
        self.maxretry.setText(str(constant.MAX_RETRY))
        self.message.setText(constant.MESSAGE)


