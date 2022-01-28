import sys
from PyQt5.QtWidgets import QApplication
from single_face_search.app_01 import Window


app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec_())