# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 640)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/images/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setStyleSheet("background-color: rgb(255,255,255)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("background: rgb(242, 242, 242)")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.logo = QtWidgets.QLabel(self.frame)
        self.logo.setMinimumSize(QtCore.QSize(50, 50))
        self.logo.setMaximumSize(QtCore.QSize(50, 50))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(":/images/images/logo.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
        self.horizontalLayout.addWidget(self.logo)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.titleEN = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("思源黑体 CN Bold")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.titleEN.setFont(font)
        self.titleEN.setStyleSheet("font: 75 15pt \"思源黑体 CN Bold\";")
        self.titleEN.setObjectName("titleEN")
        self.verticalLayout.addWidget(self.titleEN)
        self.titleEN_2 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("思源黑体 CN Regular")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.titleEN_2.setFont(font)
        self.titleEN_2.setStyleSheet("font:10pt \"思源黑体 CN Regular\";")
        self.titleEN_2.setObjectName("titleEN_2")
        self.verticalLayout.addWidget(self.titleEN_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 153, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.controlbtn = QtWidgets.QPushButton(self.frame)
        self.controlbtn.setEnabled(False)
        self.controlbtn.setStyleSheet("QPushButton{\n"
"  padding: 5px 5px;\n"
"  margin: 0px 5px;\n"
"  border-radius: 15px;\n"
"  font: 16pt \"思源黑体 CN Regular\";\n"
"}\n"
"\n"
"QPushButton:disabled{\n"
"  background-color: rgb(152, 192, 117);\n"
"  color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"  background-color: rgb(228, 232, 236);\n"
"}")
        self.controlbtn.setDefault(False)
        self.controlbtn.setFlat(True)
        self.controlbtn.setObjectName("controlbtn")
        self.verticalLayout_2.addWidget(self.controlbtn)
        self.managebtn = QtWidgets.QPushButton(self.frame)
        self.managebtn.setStyleSheet("QPushButton{\n"
"  padding: 5px 5px;\n"
"  margin: 0px 5px;\n"
"  border-radius: 15px;\n"
"  font: 16pt \"思源黑体 CN Regular\";\n"
"}\n"
"\n"
"QPushButton:disabled{\n"
"  background-color: rgb(152, 192, 117);\n"
"  color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"  background-color: rgb(228, 232, 236);\n"
"}")
        self.managebtn.setFlat(True)
        self.managebtn.setObjectName("managebtn")
        self.verticalLayout_2.addWidget(self.managebtn)
        self.logsbtn = QtWidgets.QPushButton(self.frame)
        self.logsbtn.setStyleSheet("QPushButton{\n"
"  padding: 5px 5px;\n"
"  margin: 0px 5px;\n"
"  border-radius: 15px;\n"
"  font: 16pt \"思源黑体 CN Regular\";\n"
"}\n"
"\n"
"QPushButton:disabled{\n"
"  background-color: rgb(152, 192, 117);\n"
"  color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"  background-color: rgb(228, 232, 236);\n"
"}")
        self.logsbtn.setFlat(True)
        self.logsbtn.setObjectName("logsbtn")
        self.verticalLayout_2.addWidget(self.logsbtn)
        self.settingsbtn = QtWidgets.QPushButton(self.frame)
        self.settingsbtn.setStyleSheet("QPushButton{\n"
"  padding: 5px 5px;\n"
"  margin: 0px 5px;\n"
"  border-radius: 15px;\n"
"  font: 16pt \"思源黑体 CN Regular\";\n"
"}\n"
"\n"
"QPushButton:disabled{\n"
"  background-color: rgb(152, 192, 117);\n"
"  color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"  background-color: rgb(228, 232, 236);\n"
"}")
        self.settingsbtn.setFlat(True)
        self.settingsbtn.setObjectName("settingsbtn")
        self.verticalLayout_2.addWidget(self.settingsbtn)
        spacerItem1 = QtWidgets.QSpacerItem(20, 153, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2.addWidget(self.frame)
        self.contentlayout = QtWidgets.QGridLayout()
        self.contentlayout.setObjectName("contentlayout")
        self.horizontalLayout_2.addLayout(self.contentlayout)
        self.horizontalLayout_2.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "IRFACS"))
        self.titleEN.setText(_translate("MainWindow", "IRFACS"))
        self.titleEN_2.setText(_translate("MainWindow", "红外人脸识别门禁系统"))
        self.controlbtn.setText(_translate("MainWindow", "控制"))
        self.managebtn.setText(_translate("MainWindow", "管理"))
        self.logsbtn.setText(_translate("MainWindow", "日志"))
        self.settingsbtn.setText(_translate("MainWindow", "设置"))
import assets.assets_rc
