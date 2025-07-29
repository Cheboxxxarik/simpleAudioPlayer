from PyQt5 import QtWidgets, QtGui, QtCore
import functionality, config

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('simpleAudioPlayer')
        self.resize(1000, 800)

        self.wallpaper = QtWidgets.QLabel(self)
        self.wallpaper.setGeometry(0, 0, 1000, 800)
        self.wallpaper.setPixmap(QtGui.QPixmap(config.defaultWallpaper))
        
        self.timeSlider = QtWidgets.QSlider(self)
        self.timeSlider.setGeometry(QtCore.QRect(100, 100, 800, 21))
        self.timeSlider.setOrientation(QtCore.Qt.Horizontal)
        
        self.songTitle = QtWidgets.QLabel(self)
        self.songTitle.setGeometry(QtCore.QRect(240, 10, 521, 31))
        self.songTitle.setText('<Название песни>')
        self.songTitle.setAlignment(QtCore.Qt.AlignCenter)
        
        self.artist = QtWidgets.QLabel(self)
        self.artist.setGeometry(QtCore.QRect(240, 60, 521, 31))
        self.artist.setText('<Исполнитель>')
        self.artist.setAlignment(QtCore.Qt.AlignCenter)

        self.presentTime = QtWidgets.QLabel(self)
        self.presentTime.setGeometry(QtCore.QRect(35, 100, 55, 22))
        self.presentTime.setText(config.beginning)
        self.presentTime.setAlignment(QtCore.Qt.AlignCenter)

        self.songLength = QtWidgets.QLabel(self)
        self.songLength.setGeometry(QtCore.QRect(915, 100, 55, 22))
        self.songLength.setText(config.beginning)
        self.songLength.setAlignment(QtCore.Qt.AlignCenter)

        self.pausePlay = QtWidgets.QPushButton(self)
        self.pausePlay.setGeometry(QtCore.QRect(454, 140, 93, 28))
        self.pausePlay.setText('Пауза/Пуск')

        self.previousSong = QtWidgets.QPushButton(self)
        self.previousSong.setGeometry(QtCore.QRect(349, 140, 93, 28))
        self.previousSong.setText('<<')

        self.nextSong = QtWidgets.QPushButton(self)
        self.nextSong.setGeometry(QtCore.QRect(559, 140, 93, 28))
        self.nextSong.setText('>>')

        self.playedBefore = QtWidgets.QLabel(self)
        self.playedBefore.setGeometry(QtCore.QRect(260, 260, 481, 71))
        self.playedBefore.setText('Воспроизведённые ранее')
        # self.playedBefore.setStyleSheet(config.defaultTitleStyleSheet)
        self.playedBefore.setAlignment(QtCore.Qt.AlignCenter)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 26))
        self.menu = QtWidgets.QMenu('&Меню', self.menubar)
        self.setMenuBar(self.menubar)
        self.menu.addAction('Открыть', functionality.openFile(self))
        self.menubar.addAction(self.menu.menuAction())



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())