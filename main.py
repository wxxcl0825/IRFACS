import os
import pickle
import sys

from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QApplication

from view.MainWindow import MainWindow

from utils.model.recognize import Recognizer
from utils import constant
from view.loading import loadingwindow

conf_path = "conf.pkl"


def load_fonts():
    QFontDatabase().addApplicationFont(":fonts/fonts/SourceHanSansCN-Regular.otf")
    QFontDatabase().addApplicationFont(":fonts/fonts/SourceHanSansCN-Bold.otf")


def load_constant():
    try:
        constant.PATH_WORK_DIR, constant.PATH_TEMPLATE_DIR, constant.PATH_DB, constant.PATH_MODEL, constant.PATH_SAVE, constant.PATH_PI_ADDR, constant.MESSAGE, constant.MAX_RETRY = pickle.load(
            open(conf_path, 'rb'))

    except (FileNotFoundError, pickle.PickleError, ValueError):
        pickle.dump((None, None, None, None, None, ("0.0.0.0", 6666), "你好,{}", 5), open(conf_path, 'wb'))
        load_constant()


def save_constant():
    pickle.dump((constant.PATH_WORK_DIR, constant.PATH_TEMPLATE_DIR, constant.PATH_DB, constant.PATH_MODEL, constant.PATH_SAVE, constant.PATH_PI_ADDR, constant.MESSAGE,
                 constant.MAX_RETRY), open(conf_path, 'wb'))


def load_paths():
    base_path = os.getcwd()
    if not constant.PATH_WORK_DIR:
        constant.PATH_WORK_DIR = f"{base_path}\\work"
        constant.PATH_TEMPLATE_DIR = f"{base_path}\\template"
        constant.PATH_DB = f"{base_path}\\data.db"
        constant.PATH_MODEL = f"{base_path}\\model.pkl"
        constant.PATH_SAVE = f"{base_path}\\save"

        for directory in [constant.PATH_WORK_DIR, constant.PATH_TEMPLATE_DIR, constant.PATH_SAVE]:
            try:
                os.mkdir(directory)
            except FileExistsError:
                pass


def load_model(app, model: Recognizer):
    _std_out = sys.stdout
    loadingWindow = loadingwindow(model)
    loadingWindow.show()
    app.exec_()
    sys.stdout = _std_out


def main():
    app = QApplication(sys.argv)
    load_fonts()
    load_constant()
    load_paths()
    model = Recognizer(constant.PATH_MODEL)
    if not model.model:
        load_model(app, model)
    global_assets = {'model': model}
    main_window = MainWindow(global_assets)
    main_window.show()
    ret = app.exec_()
    save_constant()
    sys.exit(ret)


if __name__ == "__main__":
    main()
