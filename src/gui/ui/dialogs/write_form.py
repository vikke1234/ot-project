# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'write_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WriteForm(object):
    def setupUi(self, WriteForm):
        WriteForm.setObjectName("WriteForm")
        WriteForm.resize(238, 107)
        WriteForm.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(WriteForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ishex = QtWidgets.QCheckBox(WriteForm)
        self.ishex.setObjectName("ishex")
        self.horizontalLayout.addWidget(self.ishex)
        self.value = QtWidgets.QLineEdit(WriteForm)
        self.value.setObjectName("value")
        self.horizontalLayout.addWidget(self.value)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(WriteForm)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(WriteForm)
        self.buttonBox.accepted.connect(WriteForm.accept)
        self.buttonBox.rejected.connect(WriteForm.reject)
        QtCore.QMetaObject.connectSlotsByName(WriteForm)

    def retranslateUi(self, WriteForm):
        _translate = QtCore.QCoreApplication.translate
        WriteForm.setWindowTitle(_translate("WriteForm", "Write"))
        self.ishex.setText(_translate("WriteForm", "Hex"))
