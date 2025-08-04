from PyQt5 import QtCore, QtGui, QtWidgets
import config


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.wallpaper = QtWidgets.QLabel(self.centralwidget)
        self.wallpaper.setGeometry(0, 0, 1000, 800)
        self.wallpaper.setPixmap(QtGui.QPixmap(config.defaultWallpaper))
        
        self.timeView = QtWidgets.QSlider(self.centralwidget)
        self.timeView.setGeometry(QtCore.QRect(100, 100, 800, 21))
        self.timeView.setOrientation(QtCore.Qt.Horizontal)
        
        self.songTitle = QtWidgets.QLabel(self.centralwidget)
        self.songTitle.setGeometry(QtCore.QRect(240, 10, 521, 31))
        self.songTitle.setStyleSheet(config.defaultFullTitleFont)
        self.songTitle.setAlignment(QtCore.Qt.AlignCenter)
        
        self.songAuthor = QtWidgets.QLabel(self.centralwidget)
        self.songAuthor.setGeometry(QtCore.QRect(240, 60, 521, 31))
        self.songAuthor.setStyleSheet(config.defaultFullFont)
        self.songAuthor.setAlignment(QtCore.Qt.AlignCenter)
        
        self.presentTime = QtWidgets.QLabel(self.centralwidget)
        self.presentTime.setGeometry(QtCore.QRect(35, 100, 55, 22))
        self.presentTime.setStyleSheet(config.defaultFullTimeFont)
        self.presentTime.setAlignment(QtCore.Qt.AlignCenter)
        
        self.songLength = QtWidgets.QLabel(self.centralwidget)
        self.songLength.setGeometry(QtCore.QRect(915, 100, 55, 22))
        self.songLength.setStyleSheet(config.defaultFullTimeFont)
        self.songLength.setAlignment(QtCore.Qt.AlignCenter)
        
        self.pausePlay = QtWidgets.QPushButton(self.centralwidget)
        self.pausePlay.setGeometry(QtCore.QRect(454, 140, 93, 28))

        self.previousSong = QtWidgets.QPushButton(self.centralwidget)
        self.previousSong.setGeometry(QtCore.QRect(244, 140, 93, 28))
        
        self.tenSecondsAgo = QtWidgets.QPushButton(self.centralwidget)
        self.tenSecondsAgo.setGeometry(QtCore.QRect(349, 140, 93, 28))
        
        self.tenSecondsAhead = QtWidgets.QPushButton(self.centralwidget)
        self.tenSecondsAhead.setGeometry(QtCore.QRect(559, 140, 93, 28))

        self.nextSong = QtWidgets.QPushButton(self.centralwidget)
        self.nextSong.setGeometry(QtCore.QRect(664, 140, 93, 28))
        
        self.playlist = QtWidgets.QLabel(self.centralwidget)
        self.playlist.setGeometry(QtCore.QRect(460, 260, 481, 71))
        self.playlist.setStyleSheet(config.defaultFullTitleFont)
        self.playlist.setAlignment(QtCore.Qt.AlignCenter)

        self.playedBeforeList = None

        self.fileCharacteristics = QtWidgets.QLabel(self.centralwidget)
        self.fileCharacteristics.setGeometry(QtCore.QRect(100, 260, 260, 71))
        self.fileCharacteristics.setStyleSheet(config.defaultFullTitleFont)
        self.fileCharacteristics.setAlignment(QtCore.Qt.AlignCenter)

        self.fileCharacteristicsList = QtWidgets.QLabel(self.centralwidget)
        self.fileCharacteristicsList.setGeometry(QtCore.QRect(100, 351, 260, 449))
        self.fileCharacteristicsList.setStyleSheet(config.defaultFullFont)
        self.fileCharacteristicsList.setAlignment(QtCore.Qt.AlignLeft)

        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 26))
        MainWindow.setMenuBar(self.menubar)

        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.addAction('Открыть файл', self.actionClicked)
        self.menubar.addAction(self.menu.menuAction())
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "simpleAudioPlayer"))
        self.songTitle.setText(_translate("MainWindow", "<Название песни>"))
        self.songAuthor.setText(_translate("MainWindow", "<Исполнитель>"))
        self.presentTime.setText(_translate("MainWindow", "00:00"))
        self.songLength.setText(_translate("MainWindow", "00:00"))
        self.pausePlay.setText(_translate("MainWindow", "Пауза/Пуск"))
        self.previousSong.setText(_translate("MainWindow", "|<<"))
        self.tenSecondsAgo.setText(_translate("MainWindow", "<<"))
        self.tenSecondsAhead.setText(_translate("MainWindow", ">>"))
        self.nextSong.setText(_translate("MainWindow", ">>|"))
        self.playlist.setText(_translate("MainWindow", "Плейлист"))
        self.fileCharacteristics.setText(_translate("MainWindow", "Характеристики файла"))
        self.fileCharacteristicsList.setText(_translate("MainWindow", "Альбом: <Альбом>\nЖанр: <Жанр>\n" \
                                                        "Размер файла: 0Мб \n" \
                                                        "Дата создания файла: 00.00.0000"))
        self.menu.setTitle(_translate("MainWindow", "Меню"))