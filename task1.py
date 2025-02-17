import sys
from io import BytesIO

import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget)


class MapViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Map Viewer')
        self.setGeometry(100, 100, 600, 450)

        self.map_label = QLabel(self)
        self.map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.coord_input = QLineEdit(self)
        self.coord_input.setPlaceholderText('Введите координаты (широта, долгота)')

        self.zoom_input = QLineEdit(self)
        self.zoom_input.setPlaceholderText('Введите масштаб (0-17)')

        self.load_button = QPushButton('Загрузить карту', self)
        self.load_button.clicked.connect(self.load_map)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.map_label)
        layout.addWidget(self.coord_input)
        layout.addWidget(self.zoom_input)
        layout.addWidget(self.load_button)
        self.setLayout(layout)
        self.load_map()

    def load_map(self):
        coords = self.coord_input.text().strip() or '55.751244,37.618423'
        zoom = self.zoom_input.text().strip() or '10'

        map_url = f'https://static-maps.yandex.ru/1.x/?ll={coords}&z={zoom}&size=450,450&l=map'

        try:
            response = requests.get(map_url)
            if response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(BytesIO(response.content).read())
                self.map_label.setPixmap(pixmap)
            else:
                self.map_label.setText('Ошибка загрузки карты')
        except Exception as e:
            self.map_label.setText(f'Ошибка: {e}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = MapViewer()
    viewer.show()
    sys.exit(app.exec())
