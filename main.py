import os
import sys

from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QApplication
from memory_profiler import profile

from view.MainWindow import MainWindow

from utils.model.recognize import Recognizer
from utils import constant
from view.loading import loadingwindow


def load_fonts():
    QFontDatabase().addApplicationFont(":fonts/fonts/SourceHanSansCN-Regular.otf")
    QFontDatabase().addApplicationFont(":fonts/fonts/SourceHanSansCN-Bold.otf")


def load_paths():
    base_path = os.getcwd()
    if not constant.PATH_WORK_DIR:
        constant.PATH_WORK_DIR = f"{base_path}/work"
        constant.PATH_TEMPLATE_DIR = f"{base_path}/template"
        constant.PATH_DB = f"{base_path}/data.db"
        constant.PATH_MODEL = f"{base_path}/model.db"
        constant.PATH_SAVE = f"{base_path}/save"

        for directory in [constant.PATH_WORK_DIR, constant.PATH_TEMPLATE_DIR, constant.PATH_SAVE]:
            os.mkdir(directory)


def load_model(app, model: Recognizer):
    _std_out = sys.stdout
    loadingWindow = loadingwindow(model)
    loadingWindow.show()
    app.exec_()
    sys.stdout = _std_out

@profile
def main():
    app = QApplication(sys.argv)
    load_fonts()
    load_paths()
    model = Recognizer(constant.PATH_MODEL)
    if not model.model:
        load_model(app, model)
    global_assets = {'model': model}
    main_window = MainWindow(global_assets)
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
