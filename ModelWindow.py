from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import random
import json
import pathlib
from TextEditor import *
from CollapsibleBox import *

class ModelWindow(QMainWindow):
    
    name = "Bulk Data Creator"
    width = 300
    height = 600
    filesPathList = []
    factor = 11
    
    def __init__(self, parent=None):
        super(ModelWindow, self).__init__(parent)
        
        self.setWindowTitle(self.name)
        self.resize(self.width, self.height)
        self.initUI()
        
        
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
        newFileAct = QAction(QIcon("new_file.png"),"New file",self)
        newFileAct.setShortcut("ctrl+N")
        newFileAct.triggered.connect(self.new_file_pressed)
        
        self.toolbar = self.addToolBar("New file")
        self.toolbar.addAction(newFileAct)
        
        openModelAct = QAction(QIcon("load.jpeg"),"Open model",self)
        openModelAct.setShortcut("ctrl+O")
        openModelAct.triggered.connect(self.openModel_pressed)
        
        self.toolbar = self.addToolBar("Open model")
        self.toolbar.addAction(openModelAct)
        
    def new_file_pressed(self):
        w = TextEditor(self)
        w.show()
    
    ###file dialog
    def openModel_pressed(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 
         '{}'.format(pathlib.Path().absolute()),"Data files (*.json *.csv)")[0]
        
        if (fname not in self.filesPathList):
            self.filesPathList.append(fname)
        
        self.drawModels()
    
    ###load .json file and show it
    def openModel(self,path):
        with open(path,"r") as f:
            
            jsonModel = json.load(f)
            
            fileTitle = path.split("/")[-1].split(".")[0]
            
            box = CollapsibleBox(fileTitle)
            self.vlay.addWidget(box)
            
            ###grid layout to show color box followed by json elt
            grid = QGridLayout()
            row = 0
            
            ### for each json elt
            for k in jsonModel.keys():
                
                ###skip if key is elt color (program property)
                if  k.endswith("-color") :
                    continue
                
                ###label containning json elt, format {k:v}
                label = QLabel("{ "+"{0} : {1}".format(k,jsonModel[k])+" }")
                
                try:
                    ###extract json elt color
                    color = QColor(*jsonModel[k+"-color"])
                    
                except Exception as e:
                    
                    ### if doesn't exist, gen random color
                    print(e)
                    color = QColor(*[random.randint(0, 255) for _ in range(3)])
                    
                ###color box is an empty label
                c = QLabel("")
                c.setStyleSheet(
                "background-color: {}".format(color.name()))
                
                grid.addWidget(c,row,0)
                ### label is factor:1 color box size
                grid.addWidget(label,row,1,1,self.factor)
                
                row = row +1

            box.setContentLayout(grid)
        self.vlay.addStretch()
    
    def drawModels(self):
        for path in self.filesPathList:
            self.openModel(path)
