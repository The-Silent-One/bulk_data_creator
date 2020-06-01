import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import random
import json

class CollapsibleBox(QWidget):
    def __init__(self, title="", parent=None):
        super(CollapsibleBox, self).__init__(parent)

        self.toggle_button = QToolButton(
            text=title, checkable=True, checked=False
        )
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(
            Qt.ToolButtonTextBesideIcon
        )
        self.toggle_button.setArrowType(Qt.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.toggle_animation = QParallelAnimationGroup(self)

        self.content_area = QScrollArea(
            maximumHeight=0, minimumHeight=0
        )
        self.content_area.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed
        )
        self.content_area.setFrameShape(QFrame.NoFrame)

        lay = QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)

        self.toggle_animation.addAnimation(
            QPropertyAnimation(self, b"minimumHeight")
        )
        self.toggle_animation.addAnimation(
            QPropertyAnimation(self, b"maximumHeight")
        )
        self.toggle_animation.addAnimation(
            QPropertyAnimation(self.content_area, b"maximumHeight")
        )

    @pyqtSlot()
    def on_pressed(self):
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(
            Qt.DownArrow if not checked else Qt.RightArrow
        )
        self.toggle_animation.setDirection(
            QAbstractAnimation.Forward
            if not checked
            else QAbstractAnimation.Backward
        )
        self.toggle_animation.start()

    def setContentLayout(self, layout):
        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(layout)
        collapsed_height = (
            self.sizeHint().height() - self.content_area.maximumHeight()
        )
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(500)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(
            self.toggle_animation.animationCount() - 1
        )
        content_animation.setDuration(500)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)
        
class ModelWindow(QMainWindow):
    
    name = "Bulk Data Creator"
    width = 300
    height = 600
    filespathList = ["car.json"]
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle(self.name)
        self.resize(self.width, self.height)
        self.initUI()
        self.drawModels()
        
    def initUI(self):
        ###Models list
        dock = QDockWidget("Models")
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        
        scroll = QScrollArea()
        dock.setWidget(scroll)
        
        content = QWidget()
        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        
        self.vlay = QVBoxLayout(content)
        
        ###Toolbar
        newfimeAct = QAction(QIcon("new_file.png"),"New file",self)
        newfimeAct.setShortcut("ctrl+N")
        newfimeAct.triggered.connect(self.new_file_pressed)
        
        self.toolbar = self.addToolBar("New file")
        self.toolbar.addAction(newfimeAct)
        
    def new_file_pressed(self):
        print("ello")
    
    def openModel(self,path):
        with open(path,"r") as f:
            jsonElt = json.load(f)
            box = CollapsibleBox("Car")
            self.vlay.addWidget(box)
            lay = QVBoxLayout()
            
            for k in jsonElt.keys():
                if  k.endswith("-color") :
                    continue
                label = QLabel("{0} : {1}".format(k,jsonElt[k]))
                
                try:
                    color = QColor(*jsonElt[k+"-color"])
                except Exception as e:
                    print(e)
                    color = QColor(*[random.randint(0, 255) for _ in range(3)])
                    
                label.setStyleSheet(
                "background-color: {}; color : black;".format(color.name())
                )
                label.setAlignment(Qt.AlignCenter)
                lay.addWidget(label)

            box.setContentLayout(lay)
        self.vlay.addStretch()
    
    def drawModels(self):
        for path in self.filespathList:
            self.openModel(path)
        
    #def clicked(self, qmodelindex):
        #item = self.listwidget.currentItem()
        #print(item.text())
    
            
def create_app():
    app = QApplication(sys.argv)
    
    screen = ModelWindow()
    screen.show()
    
    sys.exit(app.exec_())
    

create_app()
