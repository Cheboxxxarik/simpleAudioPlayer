from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from mutagen.mp3 import MP3  
from mutagen.id3 import ID3, ID3NoHeaderError, APIC
from mutagen.wave import WAVE
from mutagen.flac import FLAC, FLACNoHeaderError 
from os.path import getsize, getmtime, splitext, basename
from datetime import datetime
import config, ui


class Window(ui.Ui_MainWindow):

    def formatTime(self, time):
        minutes = time // 60
        seconds = time % 60
        self.formattedTime = f"{minutes:02d}:{seconds:02d}" 

    def setInformation(self, fileName, audioLength, sampleRate, bitrate, 
                       channels, fileSize, creationDate, title, artist, album,
                       genre):
        self.formatTime(audioLength)

        self.visibleFileName = basename(fileName)
        
        _translate = QtCore.QCoreApplication.translate
        self.fileCharacteristicsList.setText(_translate("MainWindow", f"Название: {title}\n" \
                                                        f"Исполнитель: {artist}\n" \
                                                        f"Альбом: {album}\nЖанр: {genre}\n" \
                                                        f"Частота дискретизации: {sampleRate} Гц\n"
                                                        f"Битрейт: {bitrate} Бит/с\n" \
                                                        f"Количество каналов: {channels}\n"
                                                        f"Размер: {fileSize} Мб\n" \
                                                        f"Дата создания файла: {creationDate}"))
        self.fileTitle.setText(_translate("MainWindow", self.visibleFileName))
        self.songLength.setText(_translate("MainWindow", self.formattedTime))

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

    def makeContent(self, fileName):
        url = QtCore.QUrl.fromLocalFile(fileName)
        self.content = QMediaContent(url)

    def updateSongInfo(self, index):
        if index < 0:
            return
        
        media = self.playlist.media(index)

        if not media.isNull():
            url = media.canonicalUrl().toLocalFile()
    
            extension = splitext(url)[1].lower()
            if extension == '.mp3':
                self.getMP3Metadata(url)
            elif extension == '.wav':
                self.getWAVEMetadata(url)
            elif extension == '.flac':
                self.getFLACMetadata(url)
    
            # обновим прогресс-бар
            self.timeProgressBar.setRange(0, self.player.duration())
            self.timeProgressBar.setEnabled(True)

    def openFile(self):
        self.fileName = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, "Открыть файл", 
                                                        f"{config.defaultMusicFolder}",
                                                        "Музыка(*.mp3 *.wav *.flac)")[0]

        try:
            extension = splitext(self.fileName)[1]
            if extension == '.mp3':
                self.getMP3Metadata(self.fileName)
            elif extension == '.wav':
                self.getWAVEMetadata(self.fileName)
            elif extension == '.flac':
                self.getFLACMetadata(self.fileName)

            if self.isSomethingWasOpened == False:
                self.isSomethingWasOpened = True
                self.playlistTable.clear()
                self.playlistTable.addItem(self.visibleFileName)
                self.makeContent(self.fileName)
                self.playlist.addMedia(self.content)
                self.player.play()
            else:
                self.playlistTable.addItem(self.visibleFileName)
                self.makeContent(self.fileName)
                self.playlist.addMedia(self.content)
                self.player.play(self.playlist.next())

            self.playlist.currentIndexChanged.connect(self.updateSongInfo)

            self.timeProgressBar.setRange(0, self.player.duration())
            self.timeProgressBar.setEnabled(True)
            self.player.positionChanged.connect(self.updateTimeProgressBar)
        except Exception:
            pass

    def openFolder(self):
        folderName = QtWidgets.QFileDialog.getExistingDirectory(self.centralwidget, "Открыть папку", "music")
        try:
            print(folderName)
        except FileNotFoundError:
            pass

    def playPause(self):
        try:
            if self.player.state() == QMediaPlayer.PlayingState:
                self.player.pause()
            else:
                self.player.play()
        except AttributeError:
            pass

    def updateTimeProgressBar(self):
        pass

    def rewind(self):
        try:
            currentPosition = self.player.position()
            newPosition = currentPosition - 10000
            if newPosition > 0:
                self.player.setPosition(newPosition)
            else:
                self.player.setPosition(0)        
        except AttributeError:
            pass

    def fastForward(self):
        try:
            currentPosition = self.player.position()
            newPosition = currentPosition + 10000
            audioLengthMs = self.audioLength * 1000
            if newPosition < audioLengthMs:
                self.player.setPosition(newPosition)
            else:
                try:
                    self.player.setPosition(audioLengthMs)
                except TypeError:
                    pass
        except AttributeError:
            pass

    def playPreviousSong(self):
        self.playlist.previous()
        self.player.play()

    def playNextSong(self):
        self.playlist.next()
        self.player.play()        
  

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())