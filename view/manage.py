import os
import shutil
import time
from random import randint
from typing import List, Dict, Callable

import cv2
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap, QMouseEvent
from PyQt5.QtWidgets import QWidget, QDialog, QGraphicsScene

from ui.manage.manage import Ui_managewidget
from ui.manage.new import Ui_newdialog
from ui.manage.user import Ui_userwidget
from utils import constant
from utils.database import Database
from utils.ui import chooseFile


class managewidget(QWidget, Ui_managewidget):
    IMAGE_WIDTH = 132
    IMAGE_HEIGHT = 100

    def __init__(self, global_assets: dict):
        QWidget.__init__(self)
        Ui_managewidget.__init__(self)
        self.search_on: bool = True
        self.global_assets = global_assets
        self.setupUi(self)
        self.newdialog: None | QDialog = None
        db = Database()
        self.users = db.get_all()  # [(uid, name)]
        db.close()

        self.imageLoadThread = ThreadImageLoad(self, self.get_cached_pixmap__, self.loadImage__, self.users)
        self.imageLoadThread.updateSignal.connect(self.add_image_widget)
        self.userImageModifyThread = ThreadUserImageModify(None, self.modify_user_image__)
        self.userImageModifyThread.updateSignal.connect(self.update_userswidget)
        self.newUserThread = ThreadNewUser(None, self.new_user__)
        self.newUserThread.updateSignal.connect(self.update_userswidget)

        self.searchtext.textChanged.connect(self.search)

        self.userwidgets: List[userwidget] = []
        self.pixmap_dict: Dict[int, QPixmap] = {}

    def clear_userswidget(self):
        self.imageLoadThread.terminate()
        while self.userwidgets:
            self.userwidgets[0].deleteLater()
            self.userwidgets.remove(self.userwidgets[0])

    def update_userswidget(self):
        self.clear_userswidget()
        self.imageLoadThread.users = self.users
        self.imageLoadThread.start()

    def get_cached_pixmap__(self, uid) -> None | QPixmap:
        pixmap = None
        if uid in self.pixmap_dict.keys():
            pixmap = self.pixmap_dict[uid]
        return pixmap

    def add_image_widget(self, pixmap: QPixmap, name: str, pos: int, uid: int):
        if uid not in self.pixmap_dict.keys():
            self.pixmap_dict[uid] = pixmap

        _userwidget = userwidget(pixmap, name, uid)
        _userwidget.deleteSignal.connect(self.delete_user)
        _userwidget.modifySignal.connect(self.modify_user_image)

        self.userwidgets.append(_userwidget)
        self.userslayout.addWidget(_userwidget, pos // 4, pos % 4)

    def delete_user(self, uid: int):
        self.global_assets['model'].delete(uid)
        self.global_assets['model'].save()
        db = Database()
        db.delete(uid)
        self.users = db.get_all()
        db.close()
        os.remove(f"{constant.PATH_TEMPLATE_DIR}/{uid}.jpg")
        self.update_userswidget()

    def modify_user_image(self, uid: int, fp: str):
        self.userImageModifyThread.uid = uid
        self.userImageModifyThread.fp = fp
        self.userImageModifyThread.start()

    def modify_user_image__(self, uid: int, fp: str):
        self.global_assets['model'].delete(uid)
        self.global_assets['model'].insert(uid, fp)
        self.global_assets['model'].save()
        shutil.copy(fp, f"{constant.PATH_TEMPLATE_DIR}/{uid}.jpg")
        self.pixmap_dict[uid] = self.loadImage__(fp)

    @pyqtSlot()
    def on_addbtn_clicked(self):
        self.newdialog = newdialog()
        self.newdialog.show()
        self.newdialog.newFinishSignal.connect(self.new_user)

    def search(self):
        if self.search_on:
            self.search_on = False
            db = Database()
            prompt = self.searchtext.text()
            if not prompt.strip():
                self.users = db.get_all()
            else:
                self.users = db.query_by_name(prompt)
            self.update_userswidget()
            self.search_on = True

    def new_user(self, fp, name):
        self.newUserThread.fp = fp
        self.newUserThread.name = name
        self.newUserThread.start()

    def new_user__(self, fp, name):
        db = Database()
        while True:
            new_uid = randint(1, 1000000)
            try:
                db.query_by_uid(new_uid)
            except IndexError:
                break
        db.insert(new_uid, name)
        self.pixmap_dict[new_uid] = self.loadImage__(fp)
        db.close()
        self.users.append((new_uid, name))
        self.newUserThread.updateSignal.emit()
        self.global_assets['model'].insert(new_uid, fp)
        self.global_assets['model'].save()
        shutil.copy(fp, f"{constant.PATH_TEMPLATE_DIR}/{new_uid}.jpg")

    def loadImage__(self, fp: str) -> QPixmap:
        image = cv2.resize(cv2.imread(fp), (self.IMAGE_WIDTH, self.IMAGE_HEIGHT))
        return QPixmap.fromImage(
            QImage(image, self.IMAGE_WIDTH, self.IMAGE_HEIGHT, QImage.Format_BGR888))


class newdialog(QDialog, Ui_newdialog):
    newFinishSignal = pyqtSignal(str, str)

    def __init__(self):
        QDialog.__init__(self)
        Ui_newdialog.__init__(self)
        self.setupUi(self)

    @pyqtSlot()
    def on_confirmbtn_clicked(self):
        self.newFinishSignal.emit(self.imagepath.text(), self.name.text())
        self.deleteLater()

    @pyqtSlot()
    def on_cancelbtn_clicked(self):
        self.deleteLater()

    @pyqtSlot()
    def on_imagepathbtn_clicked(self):
        chooseFile(self, self.imagepath.text(), "JPEG image file (*.jpg)", self.imagepath)


class userwidget(QWidget, Ui_userwidget):
    deleteSignal = pyqtSignal(int)
    modifySignal = pyqtSignal(int, str)

    def __init__(self, pixmap: QPixmap | None, name, uid):
        QWidget.__init__(self)
        Ui_userwidget.__init__(self)
        self.setupUi(self)
        self.scene = QGraphicsScene()
        self.image.setScene(self.scene)
        self.text, self.pixmap, self.uid = name, pixmap, uid
        self.show_text()
        self.show_image()

        self.nametext.returnPressed.connect(self.nametext_returnPressed)
        self.image.mousePressEvent = self.on_mouse_pressed

    def on_mouse_pressed(self, event: QMouseEvent):
        if event.button() == Qt.RightButton:
            fp = chooseFile(self, os.getcwd(), "JPEG image file (*.jpg)")
            if not fp:
                return
            self.modifySignal.emit(self.uid, fp)

    @pyqtSlot()
    def on_editbtn_clicked(self):
        self.nametext.setEnabled(True)

    @pyqtSlot()
    def on_deletebtn_clicked(self):
        self.deleteSignal.emit(self.uid)

    def nametext_returnPressed(self):
        self.nametext.setDisabled(True)
        db = Database()
        db.delete(self.uid)
        db.insert(self.uid, self.nametext.text())
        db.close()

    def show_text(self):
        self.nametext.setText(self.text)

    def show_image(self):
        if not self.pixmap:
            return
        self.scene.clear()
        self.scene.addPixmap(self.pixmap)


class ThreadImageLoad(QThread):
    updateSignal = pyqtSignal(QPixmap, str, int, int)

    def __init__(self, parent, get_cached_pixmap: Callable, loadImage: Callable, users: List):
        QThread.__init__(self, parent)
        self.get_cached_pixmap__ = get_cached_pixmap
        self.loadImage__ = loadImage
        self.users = users

    def run(self) -> None:
        db = Database()
        for i, user in enumerate(self.users):
            uid, name = user
            name = db.query_by_uid(uid)
            pixmap = self.get_cached_pixmap__(uid)
            if not pixmap:
                pixmap = self.loadImage__(f"{constant.PATH_TEMPLATE_DIR}/{uid}.jpg")
            self.updateSignal.emit(pixmap, name, i, uid)
            time.sleep(0.0001)
        db.close()


class ThreadUserImageModify(QThread):
    updateSignal = pyqtSignal()

    def __init__(self, parent, process: Callable, uid: None | int = None, fp: None | str = None):
        QThread.__init__(self, parent)
        self.uid, self.fp = uid, fp
        self.process__ = process

    def run(self) -> None:
        self.process__(self.uid, self.fp)
        self.updateSignal.emit()


class ThreadNewUser(QThread):
    updateSignal = pyqtSignal()

    def __init__(self, parent, new_user, fp=None, name=None):
        QThread.__init__(self, parent)
        self.fp, self.name = fp, name
        self.new_user__ = new_user

    def run(self) -> None:
        self.new_user__(self.fp, self.name)
