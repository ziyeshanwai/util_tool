# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PyQT_form.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1485, 1002)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(1160, 30, 251, 371))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalSlider_1 = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.horizontalSlider_1.setMinimum(-100)
        self.horizontalSlider_1.setMaximum(100)
        self.horizontalSlider_1.setPageStep(1)
        self.horizontalSlider_1.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_1.setObjectName("horizontalSlider_1")
        self.verticalLayout.addWidget(self.horizontalSlider_1)
        self.horizontalSlider_2 = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.horizontalSlider_2.setMinimum(-100)
        self.horizontalSlider_2.setMaximum(100)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.verticalLayout.addWidget(self.horizontalSlider_2)
        self.horizontalSlider_3 = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.horizontalSlider_3.setMinimum(-100)
        self.horizontalSlider_3.setMaximum(100)
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_3.setObjectName("horizontalSlider_3")
        self.verticalLayout.addWidget(self.horizontalSlider_3)
        self.horizontalSlider_4 = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.horizontalSlider_4.setMinimum(-100)
        self.horizontalSlider_4.setMaximum(100)
        self.horizontalSlider_4.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_4.setObjectName("horizontalSlider_4")
        self.verticalLayout.addWidget(self.horizontalSlider_4)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(1420, 90, 54, 12))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(1420, 170, 54, 12))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(1420, 250, 54, 12))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(1420, 330, 54, 12))
        self.label_4.setObjectName("label_4")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(1160, 670, 301, 231))
        self.textEdit.setObjectName("textEdit")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 0, 1111, 1001))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2.addWidget(self.frame)

        self.retranslateUi(Form)
        self.horizontalSlider_1.valueChanged['int'].connect(Form.slider1_value_changed)
        self.horizontalSlider_2.valueChanged['int'].connect(Form.slider2_value_changed)
        self.horizontalSlider_3.valueChanged['int'].connect(Form.slider3_value_changed)
        self.horizontalSlider_4.valueChanged['int'].connect(Form.slider4_value_changed)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "slider1"))
        self.label_2.setText(_translate("Form", "slider2"))
        self.label_3.setText(_translate("Form", "slider3"))
        self.label_4.setText(_translate("Form", "slider4"))

