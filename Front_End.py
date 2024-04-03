from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from g import main

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'QuadTree Image Compressor'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.button_open = QPushButton('Open Image', self)
        self.button_open.clicked.connect(self.open_image)
        layout.addWidget(self.button_open)

        self.button_save = QPushButton('Save Image', self)
        self.button_save.clicked.connect(self.save_image)
        layout.addWidget(self.button_save)

        self.setStyleSheet("""
            QWidget {
                background-color: #EEEEEE;
            }
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
        self.show()

    def open_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Images (*.png *.xpm *.jpg *.bmp *.gif)', options=options)
        if self.image_path:
            print('Image path:', self.image_path)
            self.compressed_image = main(self.image_path)

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