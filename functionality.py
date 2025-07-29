from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog

@QtCore.pyqtSlot()
def openFile(MainWindow):
    fileName = QFileDialog.getOpenFileName(MainWindow)[0]

    try:
        print(fileName)
    except FileNotFoundError:
        pass