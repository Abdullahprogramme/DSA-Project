import os
import time
import tempfile
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QProgressBar, QRadioButton, QSizePolicy
from PyQt5.QtCore import Qt, QUrl, QRect
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from Main import main

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

        # Create a horizontal layout for the images
        image_layout = QHBoxLayout()

        # Create vertical layouts for the original image and its size
        original_layout = QVBoxLayout()
        self.label_original = QLabel(self)
        self.label_original.setFixedSize(400, 400)
        original_layout.addWidget(self.label_original)
        self.label_original_size = QLabel(self)
        self.label_original_size.setStyleSheet("color: white; font-size: 32px;")
        original_layout.addWidget(self.label_original_size)

        # Create vertical layouts for the compressed image and its size
        compressed_layout = QVBoxLayout()
        self.label_compressed = QLabel(self)
        self.label_compressed.setFixedSize(400, 400)
        compressed_layout.addWidget(self.label_compressed)
        self.label_compressed_size = QLabel(self)
        self.label_compressed_size.setStyleSheet("color: white; font-size: 32px;")
        compressed_layout.addWidget(self.label_compressed_size)

        # Add the vertical layouts to the horizontal layout
        image_layout.addLayout(original_layout)
        image_layout.addLayout(compressed_layout)
        image_layout.setAlignment(Qt.AlignCenter)
        image_layout.setSpacing(10)

        # Add the horizontal layout to the main layout
        layout.addLayout(image_layout)

        # Create a horizontal box layout
        Radiobox = QHBoxLayout()

        self.instructions_label = QLabel("Please select your preference", self)
        self.instructions_label.setWordWrap(True)
        self.instructions_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.instructions_label.setStyleSheet("color: white; font-size: 16px;")
        layout.addWidget(self.instructions_label)

        self.button_Low = QRadioButton("Low Quality", self)
        self.button_Low.setStyleSheet("color: white; font-size: 16px;")
        Radiobox.addWidget(self.button_Low)

        self.button_Mid = QRadioButton("Medium Quality", self)
        self.button_Mid.setStyleSheet("color: white; font-size: 16px;")
        Radiobox.addWidget(self.button_Mid)

        self.button_High = QRadioButton("High Quality (Default)", self)
        self.button_High.setStyleSheet("color: white; font-size: 16px;")
        self.button_High.setChecked(True)
        Radiobox.addWidget(self.button_High)

        # # Set the alignment to center
        Radiobox.setAlignment(Qt.AlignCenter)

        # Add the horizontal box layout to the existing layout
        layout.addLayout(Radiobox)

        self.status_label = QLabel('', self)
        self.status_label.setStyleSheet("color: white; font-size: 16px;")
        layout.addWidget(self.status_label)

        self.button_open = QPushButton('Open Image', self)
        self.button_open.clicked.connect(self.open_image)
        layout.addWidget(self.button_open)

        self.button_save = QPushButton('Save Image', self)
        self.button_save.clicked.connect(self.save_image)
        layout.addWidget(self.button_save)

        # Add a progress bar
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

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
            QProgressBar {
            min-width: 100px;
            margin: 10px 0;
            color: #fff;
            font: bold;
            }
            QProgressBar::chunk {
            background-color: #0ff;
            }
            original_layout {
            border: 2px solid white;
            }
            compressed_layout {
            border: 2px solid white;
            } 
        """)

        layout.setAlignment(Qt.AlignCenter)
        self.setGeometry(100, 100, 900, 700)  # Adjust the window size here
        self.show()

    def check_radio(self):
        if self.loq_radio.isChecked():
            return 'low'
        elif self.med_radio.isChecked():
            return 'medium'
        elif self.hiq_radio.isChecked():
            return 'high'
        else:
            return -1

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

    def play_music(self):
        # Load a music file
        url = QUrl.fromLocalFile('Complete.mp3')
        self.player.setMedia(QMediaContent(url))

        # Start playing
        self.player.play()

    def set_quality(self):
        if self.button_Low.isChecked():
            self.user_depth = 6 
            self.MAX_DEPTH = 9
            self.DETAIL_THRESHOLD = 10
            self.SIZE_MULTIPLIER = 1
        elif self.button_Mid.isChecked():
            self.user_depth = 7
            self.MAX_DEPTH = 9
            self.DETAIL_THRESHOLD = 7
            self.SIZE_MULTIPLIER = 1
        else:
            self.user_depth = 9
            self.MAX_DEPTH = 9
            self.DETAIL_THRESHOLD = 5
            self.SIZE_MULTIPLIER = 1
        
        return self.user_depth, self.MAX_DEPTH, self.DETAIL_THRESHOLD, self.SIZE_MULTIPLIER

    # Helper function to convert size in bytes to appropriate unit
    def convert_size(self, size_bytes):
        if size_bytes < 1048576:
            return f"{size_bytes / 1024:.2f} KB"
        else:
            return f"{size_bytes / 1048576:.2f} MB"
        
    def open_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Images (*.png *.jpeg *.jpg)', options=options)
        if self.image_path:
            self.button_open.setEnabled(False)
            self.button_save.setEnabled(False)
            self.status_label.setText('Generating image...')
            self.progress_bar.setValue(20)
            QApplication.processEvents()
            print('Image path:', self.image_path)
            self.user_depth, self.MAX_DEPTH, self.DETAIL_THRESHOLD, self.SIZE_MULTIPLIER = self.set_quality()
            self.compressed_image = main(self.image_path, self.user_depth, self.MAX_DEPTH, self.DETAIL_THRESHOLD, self.SIZE_MULTIPLIER)

            self.progress_bar.setValue(80)
            time.sleep(1)
            
            # Create a media player object
            self.player = QMediaPlayer()
            # Start playing music
            self.play_music()

            self.status_label.setText('Image generation complete.')
            self.button_open.setEnabled(True)
            self.button_save.setEnabled(True)

            # Update the progress bar
            self.progress_bar.setValue(100)

            # Save the image to a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            self.compressed_image.save(temp_file.name)

            # Display the original and compressed images
            pixmap_original = QPixmap(self.image_path).scaled(400, 400, Qt.KeepAspectRatio)
            pixmap_compressed = QPixmap(temp_file.name).scaled(400, 400, Qt.KeepAspectRatio)
            self.label_original.setPixmap(pixmap_original)
            self.label_compressed.setPixmap(pixmap_compressed)

            # Display the sizes of the images
            original_size = os.path.getsize(self.image_path) / 1024  # size in KB
            compressed_size = os.path.getsize(temp_file.name) / 1024  # size in KB
            original_size_str = self.convert_size(original_size)
            compressed_size_str = self.convert_size(compressed_size)

            self.label_original_size.setText(f'Original size: {original_size_str}')
            self.label_compressed_size.setText(f'Compressed size: {compressed_size_str}')


    def save_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.save_path, _ = QFileDialog.getSaveFileName(self, 'Save Image As', '', 'Images (*.png *.jpeg *.jpg)', options=options)
        if self.save_path and self.compressed_image:
            print('Save path:', self.save_path)
            self.compressed_image.save(self.save_path)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setApplicationName("QuadTree Image Compressor")
    ex = App()
    sys.exit(app.exec_())
