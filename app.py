from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import QSize, Qt
from PIL import Image
import subprocess
import sys
import os

class ImagePreviewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Resize Images')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        self.button_layout = QHBoxLayout()
        
        self.select_button = QPushButton('Select Image Folder')
        self.select_button.clicked.connect(self.select_folder)
        self.button_layout.addWidget(self.select_button)

        self.output_button = QPushButton('Select Save Folder')
        self.output_button.clicked.connect(self.output_folder)
        self.button_layout.addWidget(self.output_button)

        self.layout.addLayout(self.button_layout)

        self.input_dir_label = QLabel('No Image Folder!')
        self.layout.addWidget(self.input_dir_label)

        self.output_dir_label = QLabel('No Output Folder!')
        self.layout.addWidget(self.output_dir_label)

        self.label = QLabel('Enter new width (in pixels):')
        self.layout.addWidget(self.label)
        
        self.line_edit = QLineEdit()
        self.layout.addWidget(self.line_edit)
        
        self.save_button = QPushButton('Resize Images')
        self.save_button.clicked.connect(self.save_images)
        self.layout.addWidget(self.save_button)
        
        self.reset_button = QPushButton('Reset')
        self.reset_button.clicked.connect(self.reset)
        self.layout.addWidget(self.reset_button)

        self.setLayout(self.layout)

        self.input_dir = None
        self.output_dir = None

    def select_folder(self):
        dir = QFileDialog.getExistingDirectory(None, 'Select a folder:')
        self.list_widget.clear()
        if dir:
            self.input_dir = dir
            self.input_dir_label.setText(f'Input directory: {dir}')
            for file_name in os.listdir(dir):
                if file_name.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    pixmap = QPixmap(os.path.join(dir, file_name))
                    pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)

                    item = QListWidgetItem()
                    item.setIcon(QIcon(pixmap))
                    item.setText(file_name)
                    self.list_widget.setIconSize(QSize(200, 200))
                    self.list_widget.addItem(item)

    def output_folder(self):
        dir = QFileDialog.getExistingDirectory(None, "Select a folder:")
        if dir:
            self.output_dir = dir
            self.output_dir_label.setText(f'Output directory: {dir}')

    def save_images(self):
        if self.input_dir is None or self.output_dir is None:
            self.show_error_message('Please select image and output folders.')
            return

        try:
            new_width = int(self.line_edit.text())
            if self.input_dir and self.output_dir:
                for i in range(self.list_widget.count()):
                    item = self.list_widget.item(i)
                    img = Image.open(os.path.join(self.input_dir, item.text()))
                    img = self.resize_image(img, new_width)
                    img.save(os.path.join(self.output_dir, f'Scaled-{item.text()}'))
                self.show_success_message()
            else:
                self.show_error_message('Image or output folder is not set.')
        except Exception as e:
            self.show_error_message(str(e))
            
        if sys.platform == 'win32':
            os.startfile(self.output_dir)
        elif sys.platform == 'darwin':
            subprocess.run(['open', self.output_dir])
        else:
            subprocess.run(['xdg-open', self.output_dir])

    def resize_image(self, img, new_width):
        width, height = img.size
        ratio = height/width
        new_height = int(ratio * new_width)
        resized_image = img.resize((new_width, new_height))
        return resized_image
    
    def reset(self):
        self.list_widget.clear()
        self.input_dir = None
        self.output_dir = None
        self.input_dir_label.setText('No Image Folder!')
        self.output_dir_label.setText('No Output Folder!')
        self.line_edit.clear()
    
    def show_error_message(self, message):
        QMessageBox().critical(self, "Error", message)

    def show_success_message(self):
        QMessageBox().information(self, "Success", 'Images were resized successfully.')

def main():
    app = QApplication(sys.argv)
    window = ImagePreviewer()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()