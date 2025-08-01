from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog

#@QtCore.pyqtSlot()
def openFile():
    fileName = QFileDialog.getOpenFileName()[0]

    try:
        print(fileName)
    except FileNotFoundError:
        pass