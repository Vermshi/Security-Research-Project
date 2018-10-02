import sys

import random

from PySide2 import QtCore, QtWidgets, QtGui


class MyWidget(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        
        self.hello = ["Hallo Welt", "Hei Verden", "Hei maailma",
            "Hola Mundo", "Donkey Kong"]
        self.button = QtWidgets.QPushButton("Click me!")
        self.button2 = QtWidgets.QPushButton("Click me2!")

        
        self.edit = QtWidgets.QLineEdit("Write my name here")
        self.button3 = QtWidgets.QPushButton("Show Greetings")

        self.text = QtWidgets.QLabel("Hello World")
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(10,5,5,8)
        layout.addWidget(self.edit)
        layout.addWidget(self.text)
        layout.addWidget(self.button)
        layout.addWidget(self.button2)      
        layout.addWidget(self.button3)
        self.setLayout(layout)

        self.button.clicked.connect(self.magic)
        self.button3.clicked.connect(self.greetings)


    def magic(self):

        self.text.setText(random.choice(self.hello))

    # Greets the user

    def greetings(self):

        print ("Hello %s" % self.edit.text())

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec_())


