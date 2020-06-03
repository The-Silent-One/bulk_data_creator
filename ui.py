import sys
from PyQt5.QtGui import *
from ModelWindow import *

def create_app():
    app = QApplication(sys.argv)
    
    screen = ModelWindow()
    screen.show()
    
    sys.exit(app.exec_())
    

create_app()
