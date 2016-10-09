# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Help_dialog.ui'
#
# Created: Sun Nov 22 20:07:03 2015
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

class Ui_Dialog_Help(object):
    def setupUi(self, Dialog_Help):
        Dialog_Help.setObjectName(_fromUtf8("Dialog_Help"))
        Dialog_Help.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Icons/calculator2-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog_Help.setWindowIcon(icon)
        Dialog_Help.setAutoFillBackground(True)
        self.horizontalLayout = QtGui.QHBoxLayout(Dialog_Help)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.textBrowser = QtGui.QTextBrowser(Dialog_Help)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.horizontalLayout.addWidget(self.textBrowser)

        self.retranslateUi(Dialog_Help)
        QtCore.QMetaObject.connectSlotsByName(Dialog_Help)

    def retranslateUi(self, Dialog_Help):
        Dialog_Help.setWindowTitle(_translate("Dialog_Help", "Help", None))

import icons_rc
