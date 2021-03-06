# Filename: app_01.py


"""Main Window-Style application."""


#from face_search_single import run_single_search
import sys, functools, cv2

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar, QScrollArea
from PyQt5.QtWidgets import QToolBar, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QTableWidget
from PyQt5.QtCore import Qt, QSize
from gui.directory_file_widger import dir_file_picker


from utils.approximate_search import single_emb_search
from utils.general_utils import *
from utils.face_detection import face_detection


class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        # Initialize face Detector
        self.detector = face_detection()
        self.setWindowTitle('QMainWindow')
        self._create_central_widget()
        #self.setCentralWidget(QLabel("I'm the Central Widget"))
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()
        #Define output variable
        self.output_list = pd.DataFrame()

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




    def _convert_bbox(self, bbox, original_resolution):
        # Scale bbox to original resolution
        # Since bbox are calculated at scaled resolution

        dimension_limit = self.detector.det_size
        max_dim = max(original_resolution)
        ratio = 1
        if max_dim > dimension_limit:
            ratio = max_dim/dimension_limit
            new_dimension = (int(ratio*original_resolution[0]), int(ratio*original_resolution[1]))
            #image = cv2.resize(image, new_dimension, interpolation = cv2.INTER_AREA)

        return ratio*bbox



    def _display_output(self, output_number):
        if self.output_list.empty:
            #self.output_image_display.setText('No Output')
            return 0
            
        # Display query image using QPixmap
        file_name = self.output_list['file_name'].iloc[output_number]
        original_resolution = self.output_list['original_resolution'].iloc[output_number]
        bbox = self.output_list['bbox'].iloc[output_number]
        #bbox = self._convert_bbox(bbox, original_resolution)
        # Convert bbox to int
        bbox = [int(i) for i in bbox]
        query_img = cv2.cvtColor(cv2.imread(file_name), cv2.COLOR_RGB2BGR)

        # Scaling image to within set max dimension
        # Since images can be of different sizes, the maximum dimension needs to be
        # scaled to winthin set limit
        dimension_limit = self.detector.det_size
        max_dim = max(query_img.shape)
        if max_dim > dimension_limit:
            ratio = dimension_limit/float(max_dim)
            new_dimension = (int(ratio*query_img.shape[0]), int(ratio*query_img.shape[1]))
            #print(query_img.shape)
            #new_dimension = [int(ratio*i) for i in query_img.shape]
            query_img = cv2.resize(query_img, new_dimension, interpolation = cv2.INTER_AREA)
            #print(query_img.shape)
        #print(original_resolution, bbox)
        # bbox output = [x1,y1,x2,y2]

        query_img = cv2.rectangle(query_img,(bbox[0],bbox[1]), (bbox[2],bbox[3]), (255,255,0), 4)
        height, width, channel = query_img.shape
        bytesPerLine = 3 * width
        # Convert cv2Image to QImage
        qImg = QtGui.QImage(query_img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        self.output_image_pixmap = QtGui.QPixmap.fromImage(qImg)
        # Resize Image
        #self.input_image_pixmap.scaled(64, 64, QtCore.Qt.KeepAspectRatio)
        # Display Image
        self.output_image_display.setPixmap(self.output_image_pixmap.scaled(480, 480, QtCore.Qt.KeepAspectRatio))        

        return 0


    def run_single_search(self):
        dir_addr = self.dir_prompt.folder_name 
        file_addr = self.file_prompt.file_name
        process_terminal_output = "Ready \n"

        # Perform file and directory checks
        check_file = image_support(file_addr)
        if check_file == -1:
            process_terminal_output += "File Does not Exist or Address Invalid \n"
            self.process_terminal.setText(process_terminal_output)
        elif check_file == 0:
            process_terminal_output += "File format not support. Use one of the following image formats: \n"
            buff_format = ' '
            buff_format = buff_format.join(supported_image_formats)
            process_terminal_output += buff_format
            process_terminal_output += '\n'
            self.process_terminal.setText(process_terminal_output)
        
        else:
            # Display query image with bounding box using QPixmap
            query_img = cv2.cvtColor(cv2.imread(file_addr), cv2.COLOR_RGB2BGR)
            height, width, channel = query_img.shape
            bytesPerLine = 3 * width
            # Convert cv2Image to QImage
            qImg = QtGui.QImage(query_img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
            self.input_image_pixmap = QtGui.QPixmap.fromImage(qImg)
            # Resize Image
            #self.input_image_pixmap.scaled(64, 64, QtCore.Qt.KeepAspectRatio)
            # Display Image
            self.input_image_display.setPixmap(self.input_image_pixmap.scaled(480, 480, QtCore.Qt.KeepAspectRatio))



            # Check for process files
            file_name, last_update = get_process_files(dir_addr, task='face_detection', media='image')
            # Process Input Image for Faces
            
            face_emb, bbox, counter = self.detector.get_face_emb(file_addr)
            if counter == -1:
                process_terminal_output += "No face detected in Image \n Terminating \n"
                self.process_terminal.setText(process_terminal_output)
                return 0

            else:
                if counter == 1:
                    process_terminal_output += "Multiple Images Detected \n Performing Search on First Face \n"
                else:
                    process_terminal_output += "Performing Search on Detected Face \n"
                self.process_terminal.setText(process_terminal_output)

                # Check for process files
                #file_name, last_update = get_process_files(dir_addr, task='face_detection', media='image')
                if file_name == -1:
                    process_terminal_output += "Directory not Processed. Processing Directory \n"
                    process_terminal_output += "This may take some time... \n"
                    self.process_terminal.setText(process_terminal_output)

                    # Process Directory if no process files are found
                    self.detector.process_dir_img(dir_addr)
                    #self.detector.process_dir_videos(dir_addr)

                    process_terminal_output += "Done Processing Directory. Performing Search  now. \n"
                    self.process_terminal.setText(process_terminal_output)
                    #file_name, last_update = get_process_files(dir_addr, 'face_detection', 'image')
                else:
                    process_terminal_output += "Folder already processed. Performing Search\n"
                    self.process_terminal.setText(process_terminal_output)

            #face_emb = self.detector.get_face_emb(file_addr)
            # Display Query Image woth Bounding Box on it
            #cv2.rectangle(query_img,(int(bbox[0]),int(bbox[1])),(int(bbox[2]),int(bbox[3])),(0,0,0),2) # add rectangle to image
            
            self.output_list = single_emb_search(file_name, face_emb, num_results=100)
            process_terminal_output += "Search Complete \n"
            self.process_terminal.setText(process_terminal_output)

            # Set OutputButton text
            for i in range(len(self.output_list)):
                self.output_buttons[i].setText(self.output_list['file_name'].iloc[i])
            # Define Button Layout Based on these elements
            #for i in range(len(output_list)):
            #    btn = QPushButton(output_list['file_name'].iloc[i])
            #    btn.clicked.connect(functools.partial(self._display_output,output_list['file_name'].iloc[i],output_list['bbox'].iloc[i],output_list['original_resolution'].iloc[i]))
            #    self.output_list.addWidget(btn)
            #self.output_list.update()
            #self.output_scroll.update()
            #self.CentralWid.update()

        #return output_list
        
        return 0
 
    
    def _create_central_widget(self):
        self.CentralWid = QWidget()
        # Upper Layer encompassing lower layers
        layout_1 = QHBoxLayout() 
        # Bottom Most Layer, Left Half of Main Window
        layout_0 = QVBoxLayout()
        # VBOX layout to display pictures, Right Half of Main Window
        layout_01 = QVBoxLayout()


        # Defining layout_0, i.e., the left half
        #
        #
        # Inilialize and Build File Picker
        self.file_prompt = dir_file_picker(file_type=1)
        layout_0.addWidget(self.file_prompt.basic_widget)
        # Initialize and Build Directory-picker widget
        self.dir_prompt = dir_file_picker(file_type=0)
        layout_0.addWidget(self.dir_prompt.basic_widget)
        # Add Process Terminal
        # Add Process Terminal to Scrollable area
        self.terminal_scroll = QScrollArea()
        self.terminal_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.terminal_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.terminal_scroll.setWidgetResizable(True)
        # Define Process termina
        self.process_terminal = QLabel('READY ! ')
        self.process_terminal.setStyleSheet("background-color: white")
        self.process_terminal.setWordWrap(True)
        # Add process terminal to scrollable area
        # Add scrollable area to mainwindow
        self.terminal_scroll.setWidget(self.process_terminal)
        layout_0.addWidget(self.terminal_scroll)
        # Add Run Button
        self.run_button = QPushButton('RUN')
        # Run Single Search 
        self.run_button.clicked.connect(functools.partial(self.run_single_search))
        layout_0.addWidget(self.run_button)

        #self.image_display = QLabel()
        #layout.addWidget(self.image_display)
        #self.image_display.resize(200,200)
        #self._display_image()
        
        # Add Search result Scrollable area to Left Half
        #
        self.output_scroll = QScrollArea()
        self.output_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.output_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.output_scroll.setWidgetResizable(True)
        #Define table to hold buttons
        #self.output_table = QTableWidget()
        #self.output_table.setRowCount(100)
        #self.output_table.setVerticalHeaderLabels(["MATCHES"])
        #QVBoxLayout to hold output buttons
        self.output_area = QWidget()
        self.output_list = QVBoxLayout()
        self.output_buttons = {}
        for i in range(100):
            self.output_buttons[i] = QPushButton('--')
            self.output_buttons[i].clicked.connect(functools.partial(self._display_output, i))
            self.output_list.addWidget(self.output_buttons[i])
            pass
        #self.output_list.addWidget(QLabel(''))
        self.output_area.setLayout(self.output_list)
        #self.output_scroll.setLayout(self.output_list)
        self.output_scroll.setWidget(self.output_area)
        # Add Output List to Left Half
        layout_0.addWidget(self.output_scroll)

        # Adding Stretch in the bottom to Stack them vertically from the top
        layout_0.addStretch()
            
        # Defining layout_01,i.e., the right half
        #
        #
        # Black Place-holder to display input image
        self.input_image_display = QLabel('Input')
        layout_01.addWidget(self.input_image_display, alignment=Qt.AlignCenter)
        # Black Place-holder to display output image
        self.output_image_display = QLabel('Output')
        layout_01.addWidget(self.output_image_display, alignment=Qt.AlignCenter)

        layout_1.addLayout(layout_0,1)
        layout_1.addLayout(layout_01,1)
        self.CentralWid.setLayout(layout_1)
        self.setCentralWidget(self.CentralWid)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

