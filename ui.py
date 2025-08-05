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

        self.albumCover = QtWidgets.QLabel(self.centralwidget)
        self.albumCover.setGeometry(35, 30, 521, 521)
        self.albumCover.setPixmap(QtGui.QPixmap(config.defaultAlbumCover))
        
        self.timeView = QtWidgets.QSlider(self.centralwidget)
        self.timeView.setGeometry(QtCore.QRect(100, 700, 800, 21))
        self.timeView.setOrientation(QtCore.Qt.Horizontal)
        
        self.fileTitle = QtWidgets.QLabel(self.centralwidget)
        self.fileTitle.setGeometry(QtCore.QRect(35, 580, 521, 31))
        self.fileTitle.setStyleSheet(config.defaultFullFileTitleFont)
        self.fileTitle.setAlignment(QtCore.Qt.AlignLeft)

        self.filePath = QtWidgets.QLabel(self.centralwidget)
        self.filePath.setGeometry(QtCore.QRect(35, 635, 521, 31))
        self.filePath.setStyleSheet(config.defaultFullFont)
        self.filePath.setAlignment(QtCore.Qt.AlignLeft)
        
        self.presentTime = QtWidgets.QLabel(self.centralwidget)
        self.presentTime.setGeometry(QtCore.QRect(35, 700, 55, 22))
        self.presentTime.setStyleSheet(config.defaultFullTimeFont)
        self.presentTime.setAlignment(QtCore.Qt.AlignLeft)
        
        self.songLength = QtWidgets.QLabel(self.centralwidget)
        self.songLength.setGeometry(QtCore.QRect(915, 700, 55, 22))
        self.songLength.setStyleSheet(config.defaultFullTimeFont)
        self.songLength.setAlignment(QtCore.Qt.AlignLeft)
        
        self.pausePlay = QtWidgets.QPushButton(self.centralwidget)
        self.pausePlay.setGeometry(QtCore.QRect(454, 725, 93, 28))

        self.previousSong = QtWidgets.QPushButton(self.centralwidget)
        self.previousSong.setGeometry(QtCore.QRect(244, 725, 93, 28))
        
        self.tenSecondsAgo = QtWidgets.QPushButton(self.centralwidget)
        self.tenSecondsAgo.setGeometry(QtCore.QRect(349, 725, 93, 28))
        
        self.tenSecondsAhead = QtWidgets.QPushButton(self.centralwidget)
        self.tenSecondsAhead.setGeometry(QtCore.QRect(559, 725, 93, 28))

        self.nextSong = QtWidgets.QPushButton(self.centralwidget)
        self.nextSong.setGeometry(QtCore.QRect(664, 725, 93, 28))
        
        self.playlistLabel = QtWidgets.QLabel(self.centralwidget)
        self.playlistLabel.setGeometry(QtCore.QRect(600, 225, 371, 71))
        self.playlistLabel.setStyleSheet(config.defaultFullTitleFont)
        self.playlistLabel.setAlignment(QtCore.Qt.AlignLeft)

        self.playlist = QtWidgets.QLabel(self.centralwidget)
        self.playlist.setGeometry(QtCore.QRect(600, 269, 371, 282))
        self.playlist.setStyleSheet(config.defaultFullFont)
        self.playlist.setAlignment(QtCore.Qt.AlignLeft)

        self.fileCharacteristics = QtWidgets.QLabel(self.centralwidget)
        self.fileCharacteristics.setGeometry(QtCore.QRect(600, 30, 360, 31))
        self.fileCharacteristics.setStyleSheet(config.defaultFullTitleFont)
        self.fileCharacteristics.setAlignment(QtCore.Qt.AlignLeft)

        self.fileCharacteristicsList = QtWidgets.QLabel(self.centralwidget)
        self.fileCharacteristicsList.setGeometry(QtCore.QRect(600, 75, 371, 151))
        self.fileCharacteristicsList.setStyleSheet(config.defaultFullFont)
        self.fileCharacteristicsList.setAlignment(QtCore.Qt.AlignLeft)

        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 26))
        MainWindow.setMenuBar(self.menubar)

        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.addAction('Открыть файл', self.actionClicked)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "simpleAudioPlayer"))
        self.fileTitle.setText(_translate("MainWindow", "<Название файла>"))
        self.filePath.setText(_translate("MainWindow", "<Путь к файлу>"))
        self.presentTime.setText(_translate("MainWindow", "00:00"))
        self.songLength.setText(_translate("MainWindow", "00:00"))
        self.pausePlay.setText(_translate("MainWindow", "Пауза/Пуск"))
        self.previousSong.setText(_translate("MainWindow", "|<<"))
        self.tenSecondsAgo.setText(_translate("MainWindow", "<<"))
        self.tenSecondsAhead.setText(_translate("MainWindow", ">>"))
        self.nextSong.setText(_translate("MainWindow", ">>|"))
        self.playlistLabel.setText(_translate("MainWindow", "Плейлист"))
        self.playlist.setText(_translate("MainWindow", "^_^"))
        self.fileCharacteristics.setText(_translate("MainWindow", "Характеристики файла"))
        self.fileCharacteristicsList.setText(_translate("MainWindow", "Название: <Название>\n" \
                                                "Исполнитель: <Исполнитель>\n" \
                                                "Альбом: <Альбом>\nЖанр: <Жанр>\n" \
                                                "Размер файла: 0Мб \n" \
                                                "Дата создания файла: 00.00.0000"))
        self.menu.setTitle(_translate("MainWindow", "Меню"))