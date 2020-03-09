# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 15:26:34 2019

@author: justRandom
"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import os
import random
import PyQt5.QtGui as qt
from PyQt5 import QtCore
import time
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
from serial import SerialException
import serial
import spellmanXLG

pg.mkQApp()

## Define main window class from template
path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, 'qt/untitled/mainwindow.ui')
WindowTemplate, TemplateBaseClass = pg.Qt.loadUiType(uiFile)

#Dic holding all xlg information 





class MainWindow(TemplateBaseClass):  
    
        
    def __init__(self):
        self.guiXlg = spellmanXLG.xlg()
               
        self.setVoltage = 0
        self.setCurrent = 0
        
        #Set up main ui winows (goes first!)
        TemplateBaseClass.__init__(self)
        self.setWindowTitle('pyqtgraph example: Qt Designer')    
        
        # Create the main window
        self.ui = WindowTemplate()
        self.ui.setupUi(self)
        self.ui.connect.clicked.connect(self.setPort)
        self.ui.enable.clicked.connect(self.enable)
        self.ui.disable.clicked.connect(self.disable)
        
        self.ui.sVoltage.valueChanged.connect(self.vChanged)
        self.ui.sCurrent.valueChanged.connect(self.cChanged)
        
        self.show()
        
        #Qtimer to update gui 
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.getXLR)
        timer.start(1000)

        
    def setPort(self):
        self.guiXlg.connectPort(self.ui.sPort.value())
        
    def enable(self):
        self.guiXlg.setXLG(self.setVoltage, self.setCurrent, True)
        
    def disable(self):
        self.guiXlg.setXLG(0, 0, False)
        
    def vChanged(self):
        self.setVoltage = self.ui.sVoltage.value()
        
    def cChanged(self):
        self.setCurrent = self.ui.sCurrent.value()
        
    def getXLR(self):
        status = self.guiXlg.getXLG()
        print(status)
        v = status["voltage"]
        c = status["current"]
        self.ui.dVoltage.display(v)
       
        self.ui.dCurrent.display(c)
        
        #Errors
        if status["arcError"] is True:
            self.ui.dArc.setStyleSheet("background-color: rgb(235,1,20)")
        else:
            self.ui.dArc.setStyleSheet("background-color: rgb(106,235,43)")
        if status["InterlockError"] is True:
            self.ui.dInterlock.setStyleSheet("background-color: rgb(235,1,20)")
        else:
            self.ui.dInterlock.setStyleSheet("background-color: rgb(106,235,43)")
        if status["regulationError"] is True:
            self.ui.regulationError.setStyleSheet("background-color: rgb(235,1,20)")
        else:
            self.ui.regulationError.setStyleSheet("background-color: rgb(106,235,43)")
        if status["tempError"] is True:
            self.ui.tempError.setStyleSheet("background-color: rgb(235,1,20)")
        else:
            self.ui.tempError.setStyleSheet("background-color: rgb(106,235,43)")
        if status["coolingError"] is True:
            self.ui.coolingError.setStyleSheet("background-color: rgb(235,1,20)")
        else:
            self.ui.coolingError.setStyleSheet("background-color: 106,235,43)")           
        if status["overCurrent"] is True:
            self.ui.overCurrent.setStyleSheet("background-color: rgb(235,1,2)0")
        else:
            self.ui.overCurrent.setStyleSheet("background-color: rgb(106,235,43)")          
        if status["overVoltage"] is True:
            self.ui.overVoltage.setStyleSheet("background-color: rgb(235,1,20)")
        else:
            self.ui.overVoltage.setStyleSheet("background-color: rgb(106,235,43)")       
        if status["remote"] is False:
            self.ui.remote.setStyleSheet("background-color: rgb(235,1,20)")
        else:
            self.ui.remote.setStyleSheet("background-color: rgb(106,235,43)")

        
        #self.ui.voltageDisplay.display(v)
        
        
    def closeEvent(self, event):
        print("Program Closes Here")
        
        exit()
        

win = MainWindow()

if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()