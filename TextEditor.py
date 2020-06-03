from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class TextEditor(QMainWindow):
    
    name = "Editor"
    width = 500
    height = 700
    
    def __init__(self,parent=None):
        super(TextEditor, self).__init__(parent)
        
        self.setWindowTitle(self.name)
        self.resize(self.width, self.height)
        
        self.editor()
    
    def editor(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
