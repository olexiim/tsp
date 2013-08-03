# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tsp_random_options.ui'
#
# Created: Sat Aug 03 15:43:31 2013
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_tsp_random_options(object):
    def setupUi(self, tsp_random_options):
        tsp_random_options.setObjectName(_fromUtf8("tsp_random_options"))
        tsp_random_options.resize(274, 92)
        self.buttonBox = QtGui.QDialogButtonBox(tsp_random_options)
        self.buttonBox.setGeometry(QtCore.QRect(20, 50, 251, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.widget = QtGui.QWidget(tsp_random_options)
        self.widget.setGeometry(QtCore.QRect(10, 15, 241, 22))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.cities_num = QtGui.QSpinBox(self.widget)
        self.cities_num.setMaximumSize(QtCore.QSize(70, 16777215))
        self.cities_num.setSuffix(_fromUtf8(""))
        self.cities_num.setMinimum(4)
        self.cities_num.setMaximum(999999)
        self.cities_num.setObjectName(_fromUtf8("cities_num"))
        self.horizontalLayout.addWidget(self.cities_num)

        self.retranslateUi(tsp_random_options)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), tsp_random_options.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), tsp_random_options.reject)
        QtCore.QMetaObject.connectSlotsByName(tsp_random_options)

    def retranslateUi(self, tsp_random_options):
        tsp_random_options.setWindowTitle(QtGui.QApplication.translate("tsp_random_options", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("tsp_random_options", "Number of cities:", None, QtGui.QApplication.UnicodeUTF8))

