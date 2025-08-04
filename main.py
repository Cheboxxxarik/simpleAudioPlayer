from PyQt5 import QtCore, QtWidgets
from mutagen.mp3 import MP3  
from mutagen.id3 import ID3, ID3NoHeaderError
import config, ui
import os

class Window(ui.Ui_MainWindow):
    
    def actionClicked(self):
        action = self.centralwidget.sender().text()

        if action == 'Открыть файл':
            self.openFile()

    def setInformation(self, title, artist, audioLength, album, genre, fileSize, creationDate):
        minutes = audioLength // 60
        seconds = audioLength % 60

        _translate = QtCore.QCoreApplication.translate
        self.fileCharacteristicsList.setText(_translate("MainWindow", f"Название: {title}\n" \
                                                f"Исполнитель: {artist}\n" \
                                                f"Альбом: {album}\nЖанр: {genre}\n" \
                                                f"Размер файла: {fileSize}Мб \n" \
                                                f"Дата создания файла: {creationDate}"))
        self.songTitle.setText(_translate("MainWindow", f"{title}"))
        self.songAuthor.setText(_translate("MainWindow", f"{artist}"))
        self.songLength.setText(_translate("MainWindow", f'{minutes}:{seconds}'))

    def getMP3Metadata(self, fileName):  
        try:  
            audio = MP3(fileName, ID3=ID3) 
            title = audio.get('TIT2')  
            artist = audio.get('TPE1')
            audioLength = audio.info.length
            roundedAudioLength = round(audioLength)
            self.setInformation(title, artist, roundedAudioLength, album='0', genre='0', 
                                fileSize='0', creationDate='00.00.0000')
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
            nameAndExtension = os.path.splitext(fileName)
            extension = nameAndExtension[1]
            if extension == '.mp3':
                self.getMP3Metadata(fileName)
            elif extension == '.wav':
                self.getWAVMetadata(fileName)
            elif extension == '.flac':
                self.getFLACMetadata(fileName)
        except FileNotFoundError:
            pass

        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())