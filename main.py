from PyQt5 import QtCore, QtWidgets
import config, ui

class Window(ui.Ui_MainWindow):

    def setInformation(self, title, artist, fileName, audioLength, album, 
                       genre, bitrate, channels, fileSize, creationDate):
        minutes = audioLength // 60
        seconds = audioLength % 60

        visibleFileName = fileName.rsplit('/', 1)[1]

        _translate = QtCore.QCoreApplication.translate
        self.fileCharacteristicsList.setText(_translate("MainWindow", f"Название: {title}\n" \
                                                f"Исполнитель: {artist}\n" \
                                                f"Альбом: {album}\nЖанр: {genre}\n" \
                                                f"Битрейт: {bitrate}Гц\n" \
                                                f"Количество каналов: {channels}\n"
                                                f"Размер: {fileSize} Мб\n" \
                                                f"Дата создания файла: {creationDate}"))
        self.fileTitle.setText(_translate("MainWindow", visibleFileName))
        self.filePath.setText(_translate("MainWindow", fileName))
        self.songLength.setText(_translate("MainWindow", f'{minutes}:{seconds}'))

    def getMP3Metadata(self, fileName):  
        try:
            from mutagen.mp3 import MP3  
            from mutagen.id3 import ID3, ID3NoHeaderError
            from os.path import getsize, getmtime
            from datetime import datetime

            audio = MP3(fileName, ID3=ID3) 
            title = audio.get('TIT2')  
            artist = audio.get('TPE1')
            album = audio.get('TALB')
            genre = audio.get('TCON')
            audioLength = audio.info.length
            roundedAudioLength = round(audioLength)
            bitrate = audio.info.bitrate
            channels = audio.info.channels
            fileSize = round(getsize(fileName) / 1_048_576, 2)
            try:
                creationDateTime = getmtime(fileName)
                creationDate = datetime.fromtimestamp(creationDateTime)
            except OSError:
                creationDate = '00.00.0000'
            self.setInformation(title, artist, fileName, roundedAudioLength, album, genre, 
                                bitrate, channels, fileSize, creationDate.strftime('%d.%m.%Y'))
        except ID3NoHeaderError:  
            pass

    def getWAVMetadata(self, fileName):
        pass

    def getFLACMetadata(self, fileName):
        pass

    def openFile(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, "Открыть файл", 
                                            f"{config.defaultMusicFolder}",
                                            "Музыка(*.mp3 *.wav *.flac)")[0]

        try:
            import pygame
            import os

            nameAndExtension = os.path.splitext(fileName)
            extension = nameAndExtension[1]
            if extension == '.mp3':
                self.getMP3Metadata(fileName)
            elif extension == '.wav':
                self.getWAVMetadata(fileName)
            elif extension == '.flac':
                self.getFLACMetadata(fileName)

            pygame.mixer.init()
            pygame.mixer.music.load(fileName)
            pygame.mixer.music.play(0)
        except FileNotFoundError:
            pass

    def openFolder(self):
        folderName = QtWidgets.QFileDialog.getExistingDirectory(self.centralwidget, "Открыть папку", "music")
        try:
            print(folderName)
        except FileNotFoundError:
            pass

    def playPause(self):
        pass

        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())