from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from PyQt5.QtCore import QUrl
import sys
import os

class AudioPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Аудио плеер с плейлистом")

        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)

        self.list_widget = QListWidget()
        self.button_play = QPushButton("▶ Воспроизвести")
        self.button_next = QPushButton("⏭ Следующий")
        self.button_prev = QPushButton("⏮ Предыдущий")

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(self.button_play)
        layout.addWidget(self.button_next)
        layout.addWidget(self.button_prev)
        self.setLayout(layout)

        # Добавим аудиофайлы
        self.add_files([
            'music/e!-traxxx - Умиротворение.mp3'
        ])

        # Сигналы
        self.button_play.clicked.connect(self.player.play)
        self.button_next.clicked.connect(self.playlist.next)
        self.button_prev.clicked.connect(self.playlist.previous)

        self.list_widget.currentRowChanged.connect(self.playlist.setCurrentIndex)
        self.playlist.currentIndexChanged.connect(self.list_widget.setCurrentRow)

    def add_files(self, file_list):
        for file_path in file_list:
            if os.path.exists(file_path):
                url = QUrl.fromLocalFile(file_path)
                media = QMediaContent(url)
                self.playlist.addMedia(media)
                self.list_widget.addItem(os.path.basename(file_path))  # Показываем имя файла
            else:
                self.list_widget.addItem(f"[Файл не найден] {file_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = AudioPlayer()
    player.resize(300, 300)
    player.show()
    sys.exit(app.exec_())
