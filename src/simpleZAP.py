# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\shiva\Desktop\Progsik prosjekt\GUItest\simpleZAP.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from testclient import Test, TestClient

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        self.mainWindow = mainWindow
        
        # Get the tests from the testclient
        self.testclient = TestClient()        
        self.tester = []
        self.desc = []
        self.status = []
        for test in self.testclient.tests:
            self.tester.append(test.name)
            self.desc.append(test.description)
            self.status.append(test.passed)

        mainWindow.setObjectName("simpleZap attack engine")
        mainWindow.setWindowIcon(QtGui.QIcon("img/icon.png"))
        self.screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.width = self.screen.width()*0.5
        self.height = self.screen.height()*0.8
        mainWindow.resize(self.width, self.height)

        self.runButton = QtWidgets.QPushButton(mainWindow)
        self.runButton.setGeometry(QtCore.QRect(self.width-self.width*0.15, self.height-self.height*0.1, 100, 40))
        self.runButton.setObjectName("runButton")
        self.runButton.clicked.connect(self.dinfunksjon)
        self.targetPort = QtWidgets.QLineEdit(mainWindow)
        self.targetPort.setGeometry(QtCore.QRect(self.width*0.02, self.height*0.1, self.width*0.3, 20))
        self.targetPort.setObjectName("targetPort")
        self.portLabel = QtWidgets.QLabel(mainWindow)
        self.portLabel.setGeometry(QtCore.QRect(self.width*0.02, self.height*0.02, self.width*0.2, self.height*0.1))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.portLabel.setFont(font)
        self.portLabel.setObjectName("portLabel")
        font = QtGui.QFont()
        font.setPointSize(10)
        self.progressBar = QtWidgets.QProgressBar(mainWindow)
        self.progressBar.setGeometry(QtCore.QRect(50, self.height - 50, 300, 23))

        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        heightinterval = 100
        for i,test in enumerate(self.tester):
            font = QtGui.QFont()
            font.setPointSize(10)
            self.infoSQL = QtWidgets.QLabel(mainWindow)
            self.infoSQL.setGeometry(QtCore.QRect(10, 100+heightinterval, 200, 16))
            self.infoSQL.setFont(font)
            self.infoSQL.setObjectName("info" + test)
            # self.SQLcheckbox = QtWidgets.QCheckBox(mainWindow)
            # self.SQLcheckbox.setGeometry(QtCore.QRect(380, 120, 53, 14))
            # self.SQLcheckbox.setObjectName("SQLcheckbox")
            self.SQLinfo = QtWidgets.QLabel(mainWindow)
            self.SQLinfo.setGeometry(QtCore.QRect(10, 120+heightinterval, 191, 61))
            self.SQLinfo.setWordWrap(True)
            self.SQLinfo.setObjectName("Info"+test)
            self.line = QtWidgets.QFrame(mainWindow)
            self.line.setGeometry(QtCore.QRect(0, 90+heightinterval, self.width, 16))
            self.line.setFrameShape(QtWidgets.QFrame.HLine)
            self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line.setObjectName("line"+test)
            self.line_2 = QtWidgets.QFrame(mainWindow)
            self.line_2.setGeometry(QtCore.QRect(0, 120+61+heightinterval, self.width, 16))
            self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
            self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line_2.setObjectName("line_2"+test)
            self.pictureLabel = QtWidgets.QLabel(mainWindow)
            self.pictureLabel.setGeometry(QtCore.QRect(self.width-200, 110+heightinterval, 100, 60))
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.pictureLabel.sizePolicy().hasHeightForWidth())
            self.pictureLabel.setSizePolicy(sizePolicy)
            self.pictureLabel.setScaledContents(True)
            self.pictureLabel.setObjectName("pictureLabel")

            self.retranslateUi(mainWindow,i)
            heightinterval+=100
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow,i):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Form"))
        self.runButton.setText(_translate("mainWindow", "Run"))
        self.portLabel.setText(_translate("mainWindow", "Port number:"))
        self.infoSQL.setText(_translate("mainWindow", self.tester[i]))
        # self.SQLcheckbox.setText(_translate("mainWindow", "Run"))
        self.SQLinfo.setText(_translate("mainWindow", self.desc[i]))
        if(self.status[i] == 1):
            pixmap = QtGui.QPixmap('img/success.png')
        else:
            pixmap = QtGui.QPixmap('img/failure.png')
        self.pictureLabel.setPixmap(pixmap)

    def dinfunksjon(self):
        if len(self.targetPort.text()) == 4 and self.targetPort.text().isdigit():
            self.testclient.setZapPort(self.targetPort.text())
        self.testclient.zapConfigure()
        self.testclient.setTarget("http://0.0.0.0:8080/")
        self.testclient.runAllTests()
        
        for i, test in enumerate(self.testclient.tests):
            self.retranslateUi(self.mainWindow,i) 


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QWidget()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())

