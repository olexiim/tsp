# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_options.ui'
#
# Created: Sat Aug 03 15:41:09 2013
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_main_options(object):
    def setupUi(self, main_options):
        main_options.setObjectName(_fromUtf8("main_options"))
        main_options.resize(428, 217)
        self.gridLayout = QtGui.QGridLayout(main_options)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(main_options)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.runtime_tab = QtGui.QWidget()
        self.runtime_tab.setObjectName(_fromUtf8("runtime_tab"))
        self.layoutWidget = QtGui.QWidget(self.runtime_tab)
        self.layoutWidget.setGeometry(QtCore.QRect(9, 14, 391, 121))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.runtime_chart = QtGui.QCheckBox(self.layoutWidget)
        self.runtime_chart.setObjectName(_fromUtf8("runtime_chart"))
        self.verticalLayout.addWidget(self.runtime_chart)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.avg_solution_label = QtGui.QLabel(self.layoutWidget)
        self.avg_solution_label.setMinimumSize(QtCore.QSize(0, 0))
        self.avg_solution_label.setObjectName(_fromUtf8("avg_solution_label"))
        self.horizontalLayout.addWidget(self.avg_solution_label)
        self.avg_solution = QtGui.QSpinBox(self.layoutWidget)
        self.avg_solution.setMaximumSize(QtCore.QSize(100, 16777215))
        self.avg_solution.setMinimum(1)
        self.avg_solution.setProperty("value", 10)
        self.avg_solution.setObjectName(_fromUtf8("avg_solution"))
        self.horizontalLayout.addWidget(self.avg_solution)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.runtime_best = QtGui.QCheckBox(self.layoutWidget)
        self.runtime_best.setObjectName(_fromUtf8("runtime_best"))
        self.verticalLayout.addWidget(self.runtime_best)
        self.runtime_solution = QtGui.QCheckBox(self.layoutWidget)
        self.runtime_solution.setObjectName(_fromUtf8("runtime_solution"))
        self.verticalLayout.addWidget(self.runtime_solution)
        self.tabWidget.addTab(self.runtime_tab, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(main_options)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(main_options)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), main_options.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), main_options.reject)
        QtCore.QMetaObject.connectSlotsByName(main_options)

    def retranslateUi(self, main_options):
        main_options.setWindowTitle(QtGui.QApplication.translate("main_options", "Problem solver options", None, QtGui.QApplication.UnicodeUTF8))
        self.runtime_chart.setToolTip(QtGui.QApplication.translate("main_options", "<html><head/><body><p>This option turns on a dynamic runtime chart that shows the changing of the solutions costs</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.runtime_chart.setText(QtGui.QApplication.translate("main_options", "Show process chart", None, QtGui.QApplication.UnicodeUTF8))
        self.avg_solution_label.setText(QtGui.QApplication.translate("main_options", "Number of solutions average parameter:", None, QtGui.QApplication.UnicodeUTF8))
        self.runtime_best.setToolTip(QtGui.QApplication.translate("main_options", "<html><head/><body><p>You will see each new best solution dynamically</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.runtime_best.setText(QtGui.QApplication.translate("main_options", "Show best solutions in runtime", None, QtGui.QApplication.UnicodeUTF8))
        self.runtime_solution.setToolTip(QtGui.QApplication.translate("main_options", "<html><head/><body><p>You will see how solutions are chaning during problem solving. This option may slow down the whole work process</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.runtime_solution.setText(QtGui.QApplication.translate("main_options", "Show all solutions in runtime", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.runtime_tab), QtGui.QApplication.translate("main_options", "Runtime", None, QtGui.QApplication.UnicodeUTF8))

