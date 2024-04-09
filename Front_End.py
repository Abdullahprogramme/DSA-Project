from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtCore import Qt
from Main import main
from PyQt5.QtGui import QPixmap, QPalette, QBrush

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'QuadTree Image Compressor'
        self.pixmap = QPixmap("Background_Image.jpg")
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.updateBackground()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.status_label = QLabel('', self)
        self.status_label.setStyleSheet("color: white; font-size: 16px;")
        layout.addWidget(self.status_label)

        self.button_open = QPushButton('Open Image', self)
        self.button_open.clicked.connect(self.open_image)
        layout.addWidget(self.button_open)

        self.button_save = QPushButton('Save Image', self)
        self.button_save.clicked.connect(self.save_image)
        layout.addWidget(self.button_save)

        self.setStyleSheet("""
            QPushButton {
            background-color: #555;
            color: #fff;
            border: none;
            padding: 10px;
            min-width: 100px;
            margin: 10px 0;
            }
            QPushButton:hover {
            background-color: #777;
            }
        """)

        layout.setAlignment(Qt.AlignCenter)
        self.setGeometry(100, 100, 600, 400)
        self.show()

    def resizeEvent(self, event):
        self.updateBackground()
        super().resizeEvent(event)

    def updateBackground(self):
        # Scale the pixmap to the size of the widget
        scaledPixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        # Create a palette
        palette = QPalette()

        # Set the pixmap as the background
        palette.setBrush(QPalette.Background, QBrush(scaledPixmap))

        # Set the palette
        self.setPalette(palette)

    def open_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Images (*.png *.xpm *.jpg *.bmp *.gif)', options=options)
        if self.image_path:
            self.button_open.setEnabled(False)
            self.button_save.setEnabled(False)
            self.status_label.setText('Generating image...')
            QApplication.processEvents()
            print('Image path:', self.image_path)
            self.compressed_image = main(self.image_path)
            self.status_label.setText('Image generation complete.')
            self.button_open.setEnabled(True)
            self.button_save.setEnabled(True)

    def save_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.save_path, _ = QFileDialog.getSaveFileName(self, 'Save Image As', '', 'Images (*.png *.xpm *.jpg *.bmp *.gif)', options=options)
        if self.save_path and self.compressed_image:
            print('Save path:', self.save_path)
            self.compressed_image.save(self.save_path)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setApplicationName("QuadTree Image Compressor")
    ex = App()
    sys.exit(app.exec_())
