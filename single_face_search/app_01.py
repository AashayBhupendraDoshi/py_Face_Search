# Filename: app_01.py


"""Main Window-Style application."""


#from face_search_single import run_single_search
import sys, functools

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QLineEdit, QFileDialog
from directory_file_widger import dir_file_picker

class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('QMainWindow')
        self._create_central_widget()
        #self.setCentralWidget(QLabel("I'm the Central Widget"))
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Search")
        self.menu.addAction('&Images/Videos', self.close)
        self.menu.addAction('&Documents/Audio', self.close)
        self.menu.addAction('&Multi-Modal', self.close)

    def _createToolBar(self):
        tools = QToolBar()
        self.addToolBar(tools)
        tools.addAction('Single Search', self.close)
        tools.addAction('Multi-Search', self.close)
        tools.addAction('Aquaintance Search', self.close)

    def _createStatusBar(self):
        self.status = QStatusBar()
        self.status.showMessage("I'm the Status Bar")
        self.setStatusBar(self.status)

#    def _display_image(self, addr='/home/abd/Pictures/gui.png'):
#        #addr = '/home/abd/Desktop/v20_Backup/DCIM/Camera/20190920_003018.jpg'
        #image = cv2.imread(addr)
        #image = cv2.resize(image, (225,225), interpolation = cv2.INTER_AREA)
        #cv2.imshow('image', image)
#        image = QtGui.QImage(image.data, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
#        self.image_display.setPixmap(QtGui.QPixmap.fromImage(image))

    def run_single_search(self,folder_name, file_name):
        return 0
 
    
    def _create_central_widget(self):
        self.CentralWid = QWidget()
        layout_0 = QVBoxLayout()
        # Initialize and Build Directory-picker widget
        self.dir_prompt = dir_file_picker(file_type=0)
        layout_0.addWidget(self.dir_prompt.basic_widget)
        # Inilialize and Build File Picker
        self.file_prompt = dir_file_picker(file_type=1)
        layout_0.addWidget(self.file_prompt.basic_widget)
        # Add Process Terminal
        self.process_terminal = QLabel('READY !')
        self.process_terminal.setStyleSheet("background-color: white")
        self.process_terminal.setWordWrap(True)
        layout_0.addWidget(self.process_terminal)
        # Add Run Button
        self.run_button = QPushButton('RUN')
        # Run Single Search 
        self.run_button.clicked.connect(functools.partial(self.run_single_search, self.dir_prompt.folder_name, self.file_prompt.file_name))
        layout_0.addWidget(self.run_button)
        #self.image_display = QLabel()
        #layout.addWidget(self.image_display)
        #self.image_display.resize(200,200)
        #self._display_image()
        self.CentralWid.setLayout(layout_0)
        self.setCentralWidget(self.CentralWid)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

