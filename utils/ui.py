import os

from PyQt5.QtWidgets import QLineEdit, QFileDialog


def chooseFile(parent, filepath: str, filetype: str, line: None | QLineEdit = None) -> None | str:
    if not os.path.exists(filepath):
        filepath = os.getcwd()
    filename, filetype = QFileDialog.getOpenFileName(parent, "打开文件", filepath, filetype)
    if not filename:
        return
    if not line:
        return filename
    line.setText(filename)


def chooseDir(parent, filepath: str, line: QLineEdit):
    if not os.path.exists(filepath):
        filepath = os.getcwd()
    dirname = QFileDialog.getExistingDirectory(parent, "打开目录", filepath)
    if not dirname:
        return
    line.setText(dirname)
