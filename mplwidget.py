# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 20:24:34 2015

@author: pawelec
"""
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
#from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        
class MplWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        
        self.canvas = MplCanvas()
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.vbl.addWidget(self.toolbar)
        self.setLayout(self.vbl)
        
        
