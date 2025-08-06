from PyQt5 import QtCore, QtGui, QtWidgets
from mutagen.mp3 import MP3  
from mutagen.id3 import ID3, ID3NoHeaderError, APIC
from mutagen.wave import WAVE
from mutagen.flac import FLAC, FLACNoHeaderError 
from os.path import getsize, getmtime, splitext
from datetime import datetime
from pygame.mixer import init, music
import config, ui


class Window(ui.Ui_MainWindow):

    def setInformation(self, fileName, audioLength, sampleRate, bitrate, 
                       channels, fileSize, creationDate, title, artist, album,
                       genre):
        minutes = audioLength // 60
        seconds = audioLength % 60
        formattedTime = f"{minutes:02d}:{seconds:02d}" 

        visibleFileName = fileName.rsplit('/', 1)[1]
        
        _translate = QtCore.QCoreApplication.translate
        self.fileCharacteristicsList.setText(_translate("MainWindow", f"Название: {title}\n" \
                                                f"Исполнитель: {artist}\n" \
                                                f"Альбом: {album}\nЖанр: {genre}\n" \
                                                f"Частота дискретизации: {sampleRate} Гц\n"
                                                f"Битрейт: {bitrate} Бит/с\n" \
                                                f"Количество каналов: {channels}\n"
                                                f"Размер: {fileSize} Мб\n" \
                                                f"Дата создания файла: {creationDate}"))
        self.fileTitle.setText(_translate("MainWindow", visibleFileName))
        self.filePath.setText(_translate("MainWindow", fileName))
        self.songLength.setText(_translate("MainWindow", formattedTime))

    def getCommonMetadata(self, audio, fileName):
        self.audioLength = audio.info.length
        self.roundedAudioLength = round(self.audioLength)
        self.sampleRate = audio.info.sample_rate
        self.bitrate = audio.info.bitrate
        self.channels = audio.info.channels
        self.fileSize = round(getsize(fileName) / 1_048_576, 2)
        try:
            self.creationDateTime = getmtime(fileName)
            self.creationDate = datetime.fromtimestamp(self.creationDateTime)
        except OSError:
            self.creationDate = '00.00.0000'

    def getID3Metadata(self, audio):
        self.title = audio.get('TIT2')  
        self.artist = audio.get('TPE1')
        self.album = audio.get('TALB')
        self.genre = audio.get('TCON')
        for tag in audio.tags.values():
            if isinstance(tag, APIC):
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(tag.data)
                self.albumCover.setPixmap(pixmap.scaled(521, 521, QtCore.Qt.KeepAspectRatio, 
                                                        QtCore.Qt.SmoothTransformation))
                break
        else:
            self.albumCover.setPixmap(QtGui.QPixmap(config.defaultAlbumCover))

    def getRIFFINFOmetadata(self, audio):
        self.title = audio.tags.get("TITLE")[0]
        self.artist = audio.tags.get("ARTIST")[0]
        self.album = audio.tags.get("ALBUM")[0]
        self.genre = audio.tags.get("GENRE")[0]
        

    def getMP3Metadata(self, fileName):  
        audio = MP3(fileName, ID3=ID3) 
        try:
            self.getID3Metadata(audio)
            self.getCommonMetadata(audio, fileName)
            self.setInformation(fileName, self.roundedAudioLength, self.sampleRate, self.bitrate, 
                                self.channels, self.fileSize, self.creationDate.strftime('%d.%m.%Y'), 
                                self.title, self.artist, self.album, self.genre)
        except ID3NoHeaderError:  
            pass

    def getWAVEMetadata(self, fileName):
        audio = WAVE(fileName)
        title = artist = album = genre = 'Неизвестно'

        self.getCommonMetadata(audio, fileName)
        self.setInformation(fileName, self.roundedAudioLength, self.sampleRate, self.bitrate, 
                            self.channels, self.fileSize, self.creationDate.strftime('%d.%m.%Y'), 
                            title, artist, album, genre)
        self.albumCover.setPixmap(QtGui.QPixmap(config.defaultAlbumCover))


    def getFLACMetadata(self, fileName):
        try:
            audio = FLAC(fileName)
            self.getRIFFINFOmetadata(audio)            
            self.getCommonMetadata(audio, fileName)
            self.setInformation(fileName, self.roundedAudioLength, self.sampleRate, self.bitrate, 
                                self.channels, self.fileSize, self.creationDate.strftime('%d.%m.%Y'), 
                                self.title, self.artist, self.album, self.genre)
        except FLACNoHeaderError:
            pass

    def openFile(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, "Открыть файл", 
                                                        f"{config.defaultMusicFolder}",
                                                        "Музыка(*.mp3 *.wav *.flac)")[0]

        try:
            extension = splitext(fileName)[1]
            if extension == '.mp3':
                self.getMP3Metadata(fileName)
            elif extension == '.wav':
                self.getWAVEMetadata(fileName)
            elif extension == '.flac':
                self.getFLACMetadata(fileName)

            init()
            music.load(fileName)
            music.play(0)

        except Exception:
            pass

    def openFolder(self):
        folderName = QtWidgets.QFileDialog.getExistingDirectory(self.centralwidget, "Открыть папку", "music")
        try:
            print(folderName)
        except FileNotFoundError:
            pass

    def playPause(self):
        if music.get_busy():  # Проверяем, играет ли музыка
            music.pause()
        else:
            music.unpause()

  
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())