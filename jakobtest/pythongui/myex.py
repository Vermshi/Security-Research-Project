#!/usr/bin/python

# -'''- coding: utf-8 -'''-


import sys

from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication,

    QVBoxLayout, QDialog, QWidget, QLabel)
class Form(QDialog):


    def __init__(self, parent=None):

        super(Form, self).__init__(parent)

        # Create widgets

        self.edit = QLineEdit("Write my name here")

        self.button = QPushButton("Show Greetings")

        # Create layout and add widgets

        layout = QVBoxLayout()

        layout.addWidget(self.edit)

        layout.addWidget(self.button)

        # Set dialog layout

        self.setLayout(layout)

        # Add button signal to greetings slot

        self.button.clicked.connect(self.greetings)


    # Greets the user

    def greetings(self):

        print ("Hello %s" % self.edit.text())


class MyWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.hello = ["Hallo Welt", "Hei Verden", "Hei maailma",
            "Hola Mundo", "Donkey Kong"]
        self.button = QPushButton("Click me!")
        self.text = QLabel("Hello World")
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.magic)

    def magic(self):

        self.text.setText(random.choice(self.hello))


if __name__ == '__main__':

    # Create the Qt Application

    app = QApplication(sys.argv)

    # Create and show the form

    form = Form()

    form.show()

    widget = MyWidget()
    widget.show()

    # Run the main Qt loop

    sys.exit(app.exec_())

    
