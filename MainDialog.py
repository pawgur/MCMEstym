# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Zm2_form.ui'
#
# Created: Sat Nov 07 21:54:45 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Variable_Form(object):
    def setupUi(self, Variable_Form):
        Variable_Form.setObjectName(_fromUtf8("Variable_Form"))
        Variable_Form.resize(310, 310)
        Variable_Form.setMinimumSize(QtCore.QSize(310, 310))
        Variable_Form.setMaximumSize(QtCore.QSize(318, 310))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Icons/Edit_page_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Variable_Form.setWindowIcon(icon)
        Variable_Form.setAccessibleName(_fromUtf8(""))
        Variable_Form.setAutoFillBackground(True)
        self.gridLayout = QtGui.QGridLayout(Variable_Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.line_Variable = QtGui.QLineEdit(Variable_Form)
        self.line_Variable.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.line_Variable.setObjectName(_fromUtf8("line_Variable"))
        self.gridLayout.addWidget(self.line_Variable, 0, 1, 1, 1)
        self.linePar2 = QtGui.QLineEdit(Variable_Form)
        self.linePar2.setObjectName(_fromUtf8("linePar2"))
        self.gridLayout.addWidget(self.linePar2, 4, 1, 1, 1)
        self.OK_btn = QtGui.QPushButton(Variable_Form)
        self.OK_btn.setMinimumSize(QtCore.QSize(96, 23))
        self.OK_btn.setMaximumSize(QtCore.QSize(96, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.OK_btn.setFont(font)
        self.OK_btn.setAutoFillBackground(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/Icons/Ok_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.OK_btn.setIcon(icon1)
        self.OK_btn.setObjectName(_fromUtf8("OK_btn"))
        self.gridLayout.addWidget(self.OK_btn, 8, 1, 1, 1)
        self.label = QtGui.QLabel(Variable_Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.Cancel_btn = QtGui.QPushButton(Variable_Form)
        self.Cancel_btn.setMinimumSize(QtCore.QSize(81, 23))
        self.Cancel_btn.setMaximumSize(QtCore.QSize(81, 23))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/Icons/Cancel_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Cancel_btn.setIcon(icon2)
        self.Cancel_btn.setObjectName(_fromUtf8("Cancel_btn"))
        self.gridLayout.addWidget(self.Cancel_btn, 8, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 0, 1, 2)
        self.linePar4 = QtGui.QLineEdit(Variable_Form)
        self.linePar4.setEnabled(False)
        self.linePar4.setObjectName(_fromUtf8("linePar4"))
        self.gridLayout.addWidget(self.linePar4, 6, 1, 1, 1)
        self.line_Par1 = QtGui.QLineEdit(Variable_Form)
        self.line_Par1.setObjectName(_fromUtf8("line_Par1"))
        self.gridLayout.addWidget(self.line_Par1, 3, 1, 1, 1)
        self.linePar3 = QtGui.QLineEdit(Variable_Form)
        self.linePar3.setEnabled(False)
        self.linePar3.setObjectName(_fromUtf8("linePar3"))
        self.gridLayout.addWidget(self.linePar3, 5, 1, 1, 1)
        self.label_5 = QtGui.QLabel(Variable_Form)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)
        self.label_4 = QtGui.QLabel(Variable_Form)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)
        self.label_2 = QtGui.QLabel(Variable_Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.label_6 = QtGui.QLabel(Variable_Form)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)
        self.combo_Typ = QtGui.QComboBox(Variable_Form)
        self.combo_Typ.setObjectName(_fromUtf8("combo_Typ"))
        self.gridLayout.addWidget(self.combo_Typ, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Variable_Form)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 2, 1, 1)
        self.label_Opis = QtGui.QLabel(Variable_Form)
        self.label_Opis.setMinimumSize(QtCore.QSize(295, 50))
        self.label_Opis.setMaximumSize(QtCore.QSize(295, 50))
        font = QtGui.QFont()
        font.setItalic(True)
        font.setWeight(55)
        self.label_Opis.setFont(font)
        self.label_Opis.setWordWrap(True)
        self.label_Opis.setObjectName(_fromUtf8("label_Opis"))
        self.gridLayout.addWidget(self.label_Opis, 2, 0, 1, 3)

        self.retranslateUi(Variable_Form)
        QtCore.QMetaObject.connectSlotsByName(Variable_Form)
        Variable_Form.setTabOrder(self.line_Variable, self.combo_Typ)
        Variable_Form.setTabOrder(self.combo_Typ, self.line_Par1)
        Variable_Form.setTabOrder(self.line_Par1, self.linePar2)
        Variable_Form.setTabOrder(self.linePar2, self.linePar3)
        Variable_Form.setTabOrder(self.linePar3, self.linePar4)
        Variable_Form.setTabOrder(self.linePar4, self.OK_btn)
        Variable_Form.setTabOrder(self.OK_btn, self.Cancel_btn)

    def retranslateUi(self, Variable_Form):
        Variable_Form.setWindowTitle(_translate("Variable_Form", "Variable", None))
        self.line_Variable.setPlaceholderText(_translate("Variable_Form", "Enter new Name", None))
        self.linePar2.setPlaceholderText(_translate("Variable_Form", "Enter new value", None))
        self.OK_btn.setText(_translate("Variable_Form", "Add", None))
        self.label.setText(_translate("Variable_Form", "Variable Name:", None))
        self.Cancel_btn.setText(_translate("Variable_Form", "Cancel", None))
        self.linePar4.setPlaceholderText(_translate("Variable_Form", "Enter new value", None))
        self.line_Par1.setPlaceholderText(_translate("Variable_Form", "Enter new value", None))
        self.linePar3.setPlaceholderText(_translate("Variable_Form", "Enter new value", None))
        self.label_5.setText(_translate("Variable_Form", "Parameter 4:", None))
        self.label_4.setText(_translate("Variable_Form", "Parameter 3:", None))
        self.label_2.setText(_translate("Variable_Form", "Parameter 1:", None))
        self.label_6.setText(_translate("Variable_Form", "PDF Type:", None))
        self.label_3.setText(_translate("Variable_Form", "Parameter 2:", None))
        self.label_Opis.setText(_translate("Variable_Form", "<html><head/><body><p align=\"center\">Probability Density Function</p></body></html>", None))

import icons_rc
