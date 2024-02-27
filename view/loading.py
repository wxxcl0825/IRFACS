import sys

from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QLabel

from ui.loading import Ui_loadingwindow
from utils.model.recognize import Recognizer


class loadingwindow(QMainWindow, Ui_loadingwindow):
    def __init__(self, model: Recognizer):
        QMainWindow.__init__(self)
        Ui_loadingwindow.__init__(self)
        self.setupUi(self)
        tqdm_director = TqdmRedirector()
        tqdm_director.setTextSignal.connect(self.set_text)
        sys.stdout = tqdm_director
        self.loadingthread = ThreadLoading(self, model)
        self.loadingthread.finishSignal.connect(self.deleteLater)
        self.loadingthread.start()

    def set_text(self, text):
        self.text.setText(text)


class TqdmRedirector(QObject):
    setTextSignal = pyqtSignal(str)

    def __init__(self):
        QObject.__init__(self)

    def write(self, text):
        self.setTextSignal.emit(text)

    def flush(self):
        pass


class ThreadLoading(QThread):
    finishSignal = pyqtSignal()

    def __init__(self, parent, model: Recognizer):
        QThread.__init__(self, parent)
        self.model = model

    def run(self) -> None:
        self.model.train()
        self.finishSignal.emit()
