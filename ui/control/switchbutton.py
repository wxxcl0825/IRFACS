from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QFont, QBrush, QColor, QPen
from PyQt5.QtWidgets import QWidget


class SwitchButton(QWidget):
    def __init__(self, parent=None):
        super(SwitchButton, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.state = False
        self.setFixedSize(80, 40)

    def mousePressEvent(self, event):
        super(SwitchButton, self).mousePressEvent(event)
        self.state = False if self.state else True
        self.update()

    def paintEvent(self, event):
        super(SwitchButton, self).paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        font = QFont("思源黑体 CN Bold")
        font.setPixelSize(self.height() // 3)
        painter.setFont(font)

        if self.state:

            painter.setPen(Qt.NoPen)
            brush = QBrush(QColor('#98C075'))
            painter.setBrush(brush)

            rect_x = 0
            rect_y = 0
            rect_width = self.width()
            rect_height = self.height()
            rect_radius = self.height() // 2
            painter.drawRoundedRect(rect_x, rect_y, rect_width, rect_height, rect_radius, rect_radius)

            painter.setPen(Qt.NoPen)
            brush.setColor(QColor('#ffffff'))
            painter.setBrush(brush)

            diff_pix = 3
            rect_x = self.width() - diff_pix - (self.height() - 2 * diff_pix)
            rect_y = diff_pix
            rect_width = (self.height() - 2 * diff_pix)
            rect_height = (self.height() - 2 * diff_pix)
            rect_radius = (self.height() - 2 * diff_pix) // 2
            painter.drawRoundedRect(rect_x, rect_y, rect_width, rect_height, rect_radius, rect_radius)

            painter.setPen(QPen(QColor('#ffffff')))
            painter.setBrush(Qt.NoBrush)
            painter.drawText(QRect(int(self.height() / 3), int(self.height() / 3.5), 50, 20), Qt.AlignLeft, '开启')
        else:
            painter.setPen(Qt.NoPen)
            brush = QBrush(QColor('#F2F2F2'))
            painter.setBrush(brush)
            rect_x = 0
            rect_y = 0
            rect_width = self.width()
            rect_height = self.height()
            rect_radius = self.height() // 2
            painter.drawRoundedRect(rect_x, rect_y, rect_width, rect_height, rect_radius, rect_radius)

            pen = QPen(QColor('#999999'))
            pen.setWidth(1)
            painter.setPen(pen)
            diff_pix = 3
            rect_x = diff_pix
            rect_y = diff_pix
            rect_width = (self.height() - 2 * diff_pix)
            rect_height = (self.height() - 2 * diff_pix)
            rect_radius = (self.height() - 2 * diff_pix) // 2
            painter.drawRoundedRect(rect_x, rect_y, rect_width, rect_height, rect_radius, rect_radius)

            painter.setBrush(Qt.NoBrush)
            painter.drawText(QRect(int(self.width() * 1 / 2), int(self.height() / 3.5), 50, 20), Qt.AlignLeft, '关闭')
