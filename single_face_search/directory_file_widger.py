# Filename: app_01.py


"""Main Window-Style application."""


import sys, functools
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QLineEdit, QFileDialog

class dir_file_picker(QWidget):
# Build a directory or file-picker widget
    def __init__(self, file_type):
        super().__init__()
        self.file_type = file_type
        # If file_type=1, frompt is for selecting file
        # If file_type=0, frompt is for selecting folder/directory
        self.folder_name = ''
        self.file_name = ''
        self._create_widget()


    def _create_display(self):
        self.display = QLineEdit()

    def _set_display_text(self, text):
        # Set display's text.
        self.display.setText(text)
        self.display.setFocus()

    def _get_display_text(self):
        # Get display's text.
        return self.display.text()

    def _clear_display(self):
        # Clear the display.
        self.setDisplayText('')


    def _folder_picker(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folderName = QFileDialog.getExistingDirectory(self, "Select Directory", "/home/abd/Desktop") 
        # When the window is not inherited from QtWidgets.QDialog, self can be replaced with None
        self.folder_name = folderName
        self._set_display_text(folderName)

    def _file_picker(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Select File", "/home/abd/Desktop","All Files (*);;Python Files (*.py)", options=options)
        self.file_name = fileName
        self._set_display_text(fileName)

    def _create_widget(self):
        
        self.basic_widget = QWidget()
        self._create_display()
        # Setup Directory prompt layout
        self.widget_layout= QHBoxLayout()

        if self.file_type == 1:
            select_label = QLabel('Select File    ')
            #print(select_label.sizeHint())
            #select_label.resize(61,15)
            self.widget_layout.addWidget(select_label)
            self.widget_layout.addWidget(self.display)
            # Set-up file-picker
            self.file_picker = QPushButton('...')
            self.file_picker.clicked.connect(self._file_picker)
        else:
            select_label = QLabel('Select Folder')
            #print(select_label.sizeHint())
            #select_label.resize(61,15)
            self.widget_layout.addWidget(select_label)
            self.widget_layout.addWidget(self.display)
            # Set-up folder-picker
            self.file_picker = QPushButton('...')
            self.file_picker.clicked.connect(self._folder_picker)

        self.widget_layout.addWidget(self.file_picker)
        self.basic_widget.setLayout(self.widget_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = dir_file_picker(file_type=1)
    a.basic_widget.show()
    sys.exit(app.exec_())
