from PyQt5 import QtWidgets
from main import Ui_MainWindow

def openFile(Ui_MainWindow):
        fileName = QtWidgets.QFileDialog.getOpenFileName(Ui_MainWindow, "Открыть файл", "music", "Музыка (*.mp3 *.wav)")

        try:
            print(fileName)
        except FileNotFoundError:
            pass