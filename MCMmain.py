# -*- coding: utf-8 -*-
"""
Initiated on Tue Oct 13 22:43:38 2015
Amended for MultiCPU processing 10.05.2016

@author: pawelec
"""
__appname__="MCM Estymator"

import sys
import MCMpropagation
from PyQt4 import QtGui
from PyQt4 import QtCore
from MCMWindow import Ui_MainWindow
from MainDialog import Ui_Variable_Form
from HelpDialog import Ui_Dialog_Help
import matplotlib.pyplot as plt
from csv import reader, writer
from time import clock, sleep


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        

class Main(QtGui.QMainWindow): #the main window class 
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.z_count = 0 #index zmiennych
        self.threadPool =[] #lista otwartych watkow
        self.completed = [] #lista 
        self.ui.draw_btn.setDisabled(True)
        self.ui.oblicz_btn.setDisabled(True)
        self.mutex = QtCore.QMutex() 
        self.calculation_flag=0

        
        
#sterowanie zdarzeniami nad elementami sterowania okna               
        self.connect(self.ui.line_M, QtCore.SIGNAL("editingFinished()"), self.verifyM)
        self.connect(self.ui.line_P, QtCore.SIGNAL("editingFinished()"), self.verifyP)
        self.connect(self.ui.lineWyrazenie, QtCore.SIGNAL("editingFinished()"), self.sw_onEXEC)
        self.connect(self.ui.lineWyrazenie, QtCore.SIGNAL("returnPressed()"), self.formatExp)
        self.connect(self.ui.line_M, QtCore.SIGNAL("selectionChanged()"), self.formatM)
        self.connect(self.ui.line_P, QtCore.SIGNAL("selectionChanged()"), self.verifyP)
        self.connect(self.ui.lineWyrazenie, QtCore.SIGNAL("selectionChanged()"), self.formatExp)
        self.connect(self.ui.oblicz_btn, QtCore.SIGNAL("clicked()"), self.calculateData)
        self.connect(self.ui.dodaj_btn, QtCore.SIGNAL("clicked()"), self.dialogopen)
        self.connect(self.ui.draw_btn, QtCore.SIGNAL("clicked()"), self.draw)
        self.connect(self.ui.spinBox, QtCore.SIGNAL("valueChanged(int)"), self.recalculateR)
        self.connect(self.ui.reset_btn, QtCore.SIGNAL("clicked()"), self.resetW)
        self.connect(self.ui.checkBox_generator, QtCore.SIGNAL("stateChanged(int)"), self.genCheck)
        
#obsluga sygnalow emitowanych przez elementy menu 
        self.connect(self.ui.actionExit, QtCore.SIGNAL("triggered()"), self.exitApp)
        self.connect(self.ui.actionOpenM, QtCore.SIGNAL("triggered()"), self.openFileM)
        self.connect(self.ui.actionOpen_Variable_File, QtCore.SIGNAL("triggered()"), self.openFileV)
        self.connect(self.ui.actionExtract, QtCore.SIGNAL("triggered()"), self.extractResult)
        self.connect(self.ui.actionAbout, QtCore.SIGNAL("triggered()"), self.dispAbout)
        self.connect(self.ui.actionHelp, QtCore.SIGNAL("triggered()"), self.dispHelp)
        self.connect(self.ui.actionCleanlooks_Style, QtCore.SIGNAL("triggered()"), self.cleanStyle)
        self.connect(self.ui.actionWindowsVista_Style, QtCore.SIGNAL("triggered()"), self.winVistStyle)
        self.connect(self.ui.actionCDE_Style, QtCore.SIGNAL("triggered()"), self.cdeStyle)
        self.connect(self.ui.actionGTK_Style, QtCore.SIGNAL("triggered()"), self.gtkStyle)
        self.connect(self.ui.actionMotif_Style, QtCore.SIGNAL("triggered()"), self.motifStyle)
        self.connect(self.ui.actionPlastique_Style, QtCore.SIGNAL("triggered()"), self.plastiqueStyle)
        self.connect(self.ui.actionWindows_Style, QtCore.SIGNAL("triggered()"), self.winStyle)
        self.connect(self.ui.actionMacintosh, QtCore.SIGNAL("triggered()"), self.macStyle)
        self.connect(self.ui.actionShow_Histogram, QtCore.SIGNAL("triggered()"), self.showHist)
        
        self.connect(self.ui.dockWidget_1, QtCore.SIGNAL("visibilityChanged(bool)"), self.resizeW)
        
#metody zmieniajace styl wyswietlania   
    
    def showHist(self): #metoda przywracajaca wyswietlanie histogramu dostepna z menu
        self.ui.dockWidget_1.show()        
        
    def resizeW(self, changed): #metoda miala umozliwiac automatyczne modyfikowanie wielkosci okna glownego
        
        if changed == True and self.ui.dockWidget_1.isHidden:
            pass            
            

#metody sterujace zmiana stylu wyswietlania, dostepne z menu View        
    def cleanStyle(self):
        if 'Cleanlooks' in QtGui.QStyleFactory.keys():
            QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(u'Cleanlooks'))
        else:
            pass
        
    def winVistStyle(self):
        if 'WindowsVista' in QtGui.QStyleFactory.keys():
            QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(u'WindowsVista'))
        else:
            pass
        
    def cdeStyle(self):
        if 'CDE' in QtGui.QStyleFactory.keys():
            QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(u'CDE'))
        else:
            pass      
        
    def gtkStyle(self):
        if 'GTK+' in QtGui.QStyleFactory.keys():
            QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(u'GTK+'))
        else:
            pass 
        
    def motifStyle(self):
        if 'CDE' in QtGui.QStyleFactory.keys():
            QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(u'Motif'))
        else:
            pass   
        
    def plastiqueStyle(self):
        if 'Plastique' in QtGui.QStyleFactory.keys():
            QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(u'Plastique'))
        else:
            pass        
    def winStyle(self):
        if 'Windows' in QtGui.QStyleFactory.keys():
            QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(u'Windows'))
        else:
            pass 
        
    def macStyle(self):
        if 'Macintosh' in QtGui.QStyleFactory.keys():
            QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(u'Macintosh'))
        else:
            pass 
        
    def openFileM(self): #metoda otwierajaca plik textowy z zapisanym modelem
        dir = "."
        fileObj = None
        
        try:
            fileObj = QtGui.QFileDialog.getOpenFileName(self, __appname__ + "Open File", dir, filter="Text file(*.txt)")
            if len(fileObj)>0:            
                fileM = open(fileObj, "r")
                text = fileM.read()
                fileM.close()

                self.ui.lineWyrazenie.setText(text)
            else:
                pass
        except ValueError as e:
            QtGui.QMessageBox.warning(self, __appname__, str(e)) 
            
    def openFileV(self): #metoda odczytujaca z pliku csv zapisane dane o zmiennych
        self.lista_p=[]    
        dir = "."
        fileObj = None
        self.clearData()
        self.clearZm()
        self.clearY()
        
        try:
            fileObj = QtGui.QFileDialog.getOpenFileName(self, __appname__ + "Open File", dir, filter="Text file(*.csv)")
            if len(fileObj)>0:  
                try:
                    self.mutex.lock()#blokujemy obiekt, ktory moglby byc edytowany rownoczesnie przez inny watek
                    self.statusfontB()
                    self.ui.statusbar.showMessage("Variables are loading, please wait a moment...")
                finally:
                    self.mutex.unlock()
 
                QtCore.QCoreApplication.processEvents()
                self.ui.checkBox_generator.setDisabled(True)
                from collections import namedtuple #bedziemy uzywac krotek nazwanych do identyfikacji naglowkow kolumn
                with open(fileObj, mode ="r") as f: #otwieramy plik
                    f_csv = reader(f) #czytamy plik
                    headings = next(f_csv) #odczytujemy naglowki
                    Row = namedtuple('Row', headings) #definiujemy kolumny 
                    for r in f_csv: #oczytujemy wiersze
                        row = Row(*r) #parametryzujemy zawartosc
                        zmienne.append(row.VarName) #the list which contains info about data taken from the file
                        zmienne.append(row.PropType)
                        
                        #proces wczytywania zmiennych odbywa sie zgodnie ze sposobem zaimplementowanym przy obsludze okna dialogowego
                        #dla kazdej zmiennej okreslonej co do typu propagacji, ktora ja reprezentuje wczytujemy odpowiednia liczbe parametrow
  
                        if MCMpropagation.dict[int(row.PropType)]['parm']==3:
                            self.lista_p.append(float(row.Parm1))
                            self.lista_p.append(float(row.Parm2))
                            self.lista_p.append(float(row.Parm3))

                            self.fillTextB(self.z_count, row.VarName, MCMpropagation.dict[int(row.PropType)]['name'], MCMpropagation.dict[int(row.PropType)]['parm'] , row.Parm1, row.Parm2, row.Parm3 )
                        elif MCMpropagation.dict[int(row.PropType)]['parm']==4:
                            self.lista_p.append(float(row.Parm1))
                            self.lista_p.append(float(row.Parm2))
                            self.lista_p.append(float(row.Parm3))  
                            self.lista_p.append(float(row.Parm4))

                            self.fillTextB(self.z_count, row.VarName, MCMpropagation.dict[int(row.PropType)]['name'], MCMpropagation.dict[int(row.PropType)]['parm'], row.Parm1, row.Parm2, row.Parm3, row.Parm4 )
                        elif MCMpropagation.dict[int(row.PropType)]['parm']==1:
                            self.lista_p.append(float(row.Parm1))

                            self.fillTextB(self.z_count, row.VarName, MCMpropagation.dict[int(row.PropType)]['name'], MCMpropagation.dict[int(row.PropType)]['parm'] , row.Parm1 )                        
                        else:    
                            self.lista_p.append(float(row.Parm1))
                            self.lista_p.append(float(row.Parm2))

                            #wypelniamy okno dedykowane do przegladania informacji o zmiennych
                            self.fillTextB(self.z_count, row.VarName, MCMpropagation.dict[int(row.PropType)]['name'], MCMpropagation.dict[int(row.PropType)]['parm'], row.Parm1, row.Parm2)
                        zmienne.append(self.lista_p[0:3])
                        sleep(0.1)#wymuszone opoznienie zwieksza stabilnosc pracy programu
                                           
                        del self.lista_p[:]
                                                
                        self.z_count += 1

            
                
                try:
                    self.mutex.lock()#blokujemy obiekt, ktory moglby byc edytowany rownoczesnie przez inny watek
                    self.statusfontI()
                    self.ui.statusbar.showMessage("Ready for further activities...")
                finally:
                    self.mutex.unlock()

            else:
                pass
            
        except ValueError as e:
            QtGui.QMessageBox.warning(self, __appname__, str(e))
            
    def extractResult(self):#metoda exportujaca wynik w postaci wyliczonych wartosci dyskretnych szukanej PDF
        rows=[]
        if len(prop_Y)>0: #Jezeli mamy dane do exportowania, to budujemy ich strukture, zeby zapisac w pliku csv   
            header = ['Item_no', 'Value'] #definicja naglowka pliku, bedziemy numerowac kolejne wiersze
            for item in range(len(prop_Y)):
                row=[]
                row.append(item+1)
                row.append(prop_Y[item])
                rows.append(row)

            dir = "."
            fileObj = None
            try: 
                fileObj = QtGui.QFileDialog.getSaveFileName(self, __appname__ + "Open File", dir, filter="Text file(*.csv)")
            
                with open(fileObj, mode = "w") as f:
                    f_csv = writer(f)
                    f_csv.writerow(header)
                    f_csv.writerows(rows)
            except ValueError as e:
                QtGui.QMessageBox.warning(self, __appname__, str(e))       
        else:
            QtGui.QMessageBox.warning(self, __appname__, "There are no data to extract") 
            
    def fontB(self):
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		return font
    
    def formatM(self):
        self.ui.line_M.setFont(self.fontB())
		
    def formatP(self):
        self.ui.line_P.setFont(self.fontB())
		
    def formatExp(self):
        self.ui.lineWyrazenie.setFont(self.fontB())
    
    def verifyM(self): #metoda weryfikujaca zawartosc w polu M
        if len(self.ui.line_M.text())<4:
            QtGui.QMessageBox.warning(self, __appname__, "The smallest possible value for M is 1000")            
            self.ui.line_M.setText("1000")
            self.ui.line_M.setFocus()
        else:
            try:
                globals()["gl_M"] = int(self.ui.line_M.text())
                self.formatM()
                             
            except ValueError as e:#obsluga bledu na wypadek, gdyby podana wartosc nie dala sie skonwertowac do int
                QtGui.QMessageBox.warning(self, __appname__, u"You have put wrong value, the smallest possible value for M is 1000")
                QtGui.QMessageBox.warning(self, __appname__, str(e))
                self.ui.line_M.setText("1000")
                self.ui.line_M.setFocus()
                self.ui.line_M.selectAll()
            if len(self.ui.lineWyrazenie.text())>=1 and len(zmienne_n)>=1 and gl_P >= 1 and globals()["gl_M"] >= 1000 :
                self.ui.oblicz_btn.setDisabled(False)
            
    def verifyP(self): #metoda weryfikujaca zawartosc w polu P
        if len(self.ui.line_P.text())<2 or len(self.ui.line_P.text())>2:
			QtGui.QMessageBox.information(self, __appname__, "Default value for Coverage Probability P = 95")
			self.ui.line_P.setText("95")
			self.ui.line_P.setFocus()   
            
        else:
            try:
                globals()["gl_P"] = int(self.ui.line_P.text())
                self.formatP()
                if self.calculation_flag==1:
					
					self.PropY.calc_prd(int(self.ui.line_P.text())) 
					self.ui.Wynik_przedzil.setText(str(round(self.PropY.prd, self.ui.spinBox.value())) + "  " + str(round(self.PropY.prw, self.ui.spinBox.value())))    
                                
            except ValueError as e:#obsluga bledu na wypadek. gdyby podana wartosc nie dala sie skonwertowac do int
                QtGui.QMessageBox.warning(self, __appname__, "You have put wrong value, default value for Coverage Probability P = 95")            
                QtGui.QMessageBox.warning(self, __appname__, str(e))         
                self.ui.line_P.setText("95")
                self.ui.line_P.setFocus()
                self.ui.line_P.selectAll()
                
        self.ui.dodaj_btn.setFocus()
        if len(self.ui.lineWyrazenie.text())>=1 and len(zmienne)>=3 and globals()["gl_P"] >= 1 and globals()["gl_M"] >= 1000 :
            self.ui.oblicz_btn.setDisabled(False)
        
    def sw_onEXEC(self):
        if len(self.ui.lineWyrazenie.text())>=1 and len(zmienne)>=3 and globals()["gl_P"] >= 1 and globals()["gl_M"] >= 1000 :
            self.ui.oblicz_btn.setDisabled(False)
            self.formatExp()

    def verifyExp(self):
        if len(self.ui.lineWyrazenie.text())>=1 and len(zmienne)>=3:
            zmienne_n=self.genZmn()
            self.name_var=zmienne_n[:]
            if MCMpropagation.expVer(self.ui.lineWyrazenie.text(),self.name_var)==0:
                globals()["exp_ver_Flag"]=1
                self.sw_onEXEC()
            elif MCMpropagation.expVer(self.ui.lineWyrazenie.text(),self.name_var)==1:
                QtGui.QMessageBox.warning(self, __appname__, "You haven't defined the model properly, please verify if all the variables defined are the same as the one used in the expression")
                globals()["exp_ver_Flag"]=0
                self.formatExp()    
            elif MCMpropagation.expVer(self.ui.lineWyrazenie.text(),self.name_var)==2:
                QtGui.QMessageBox.warning(self, __appname__, "You haven't defined the model properly, an odd number of parentheses has been used, please verify")
                globals()["exp_ver_Flag"]=0
                self.formatExp()
            else:
                QtGui.QMessageBox.warning(self, __appname__, "You haven't defined the model properly, please verify if all the variables defined are the same as the one used in the expression... Unidentified character \"%s\" " % (MCMpropagation.expVer(self.ui.lineWyrazenie.text(),self.name_var)))  
                self.ui.lineWyrazenie.setFocus()
                globals()["exp_ver_Flag"]=0
                self.formatExp()
            #print 'zmienne_n', zmienne_n
            #print 'self.name_var', self.name_var
            
                     
        else:
            print 'Data undefined'
            self.formatExp()
            
    def genZmn(self):
        if len(self.ui.lineWyrazenie.text())>=1 and len(zmienne)>=3:
            try:
                del zmienne_n[:]
            except ValueError, e:
                QtGui.QMessageBox.warning(self, "Zmienne_n", str(e))
            for x in range(0, len(zmienne), 3):
                zmienne_n.append(zmienne[x])
            return zmienne_n
        else:
            print 'no data to process'
            
    def genCheck(self,val):#metoda ustawiajaca typ generatora
        if self.ui.checkBox_generator.isChecked():
            globals()["generator"]= 1
        else:
            globals()["generator"]= 0
    
    def calculateData(self): #metoda inicjuje obliczenia glowne programu, wylicza podstawowe dane
        if len(self.ui.lineWyrazenie.text())<1:
            QtGui.QMessageBox.warning(self, __appname__, "You haven't defined the model, please enter  ")  
            self.ui.lineWyrazenie.setFocus()
        elif globals()["gl_P"] < 1 or globals()["gl_M"] < 1000:
            QtGui.QMessageBox.warning(self, __appname__, "You haven't defined valid values for M or P, please enter  ")  
            self.ui.line_P.setText("95")
            self.ui.line_P.setFocus()
        else:
            self.clearY()
            if exp_ver_Flag!=1: 
                self.verifyExp()
            if exp_ver_Flag==1:     
                self.generateZm()
                self.generateY()
                self.calculation_flag=1
            else:
                QtGui.QMessageBox.warning(self, __appname__, "You haven't defined valid model, please verify  ") 
                self.ui.oblicz_btn.setDisabled(True)                
                self.ui.lineWyrazenie.setFocus()
                
        
    def dialogopen(self):#metoda obslugujaca wywolanie okna dialogu z glownego okna
        dialog = Form()
        #chcemy aby zmiany dokonane na oknie dialogowym widoczne byly na oknie glownym  
        #wywolanie okna dialogowego
        if dialog.exec_():

            self.fillTextB(self.z_count, dialog.ui.line_Variable.text(), dialog.ui.combo_Typ.currentText(), dialog.n_param, dialog.ui.line_Par1.text(), dialog.ui.linePar2.text(), dialog.ui.linePar3.text(), dialog.ui.linePar4.text()) 

            self.z_count += 1
            self.ui.dodaj_btn.setFocus()
        else:
            QtGui.QMessageBox.warning(self, __appname__, "The dialog window is going to be closed.")  
            
    def dispHelp(self):#metoda wyswietlajaca okno pomocy
        helpF = Help_d()
        helpF.exec_()
            
    def fillTextB(self, licz, zm_N, zm_T, parm, pr1, pr2=0, pr3=0, pr4=0 ): #metoda wypelniajaca textBrowser informacjami o zmiennych
        if  parm == 3:           
            self.ui.textEdit.append("Variable %s: <font color=green><b> %s</b></font>, PDF type: <font color=green> %s</font>, Parm1= <b>%s</b>, Parm2= <b>%s</b>, Parm3= <b>%s</b>" % (str(licz+1), str(zm_N), str(zm_T), str(float(pr1)), str(float(pr2)), str(float(pr3)))  )          
        elif parm == 4:
            self.ui.textEdit.append("Variable %s: <font color=green><b> %s</b></font>, PDF type: <font color=green> %s</font>, Parm1= <b>%s</b>, Parm2= <b>%s</b>, Parm3= <b>%s</b>, Parm4= <b>%s</b>" % (str(licz+1), str(zm_N), str(zm_T), str(float(pr1)), str(float(pr2)), str(float(pr3)), str(float(pr4)) )) 
        elif parm == 2:
            self.ui.textEdit.append("Variable %s: <font color=green><b> %s</b></font>, PDF type: <font color=green> %s</font>, Parm1= <b>%s</b>, Parm2= <b>%s</b>" % (str(licz+1), str(zm_N), str(zm_T), str(float(pr1)), str(float(pr2)))  ) 
        else:
            self.ui.textEdit.append("Variable %s: <font color=green><b> %s</b></font>, PDF type: <font color=green> %s</font>, Parm1= <b>%s</b>" % (str(licz+1), str(zm_N), str(zm_T), str(float(pr1)))  ) 
            
    def generateZm(self):#metoda do generowania danych wejsciowych
        self.ui.oblicz_btn.setDisabled(True)
        self.clearData()
        try:
            self.mutex.lock()#blokujemy obiekt, ktory moglby byc edytowany rownoczesnie przez inny watek
            self.statusfontB()
            self.ui.statusbar.showMessage("Data computation has been started, please wait...")
        finally:
            self.mutex.unlock()
            self.c_time = clock()
            print "type of generator:" , generator
            print 'M=', gl_M
            for zm in range(0,len(zmienne),3):
                     
                if len(zmienne[zm+2])==1:    
                    zmienne_o.append(MCMpropagation.assignVar(gl_M,zmienne[zm],zmienne[zm+1],generator,zmienne[zm+2][0]))    
                
                elif len(zmienne[zm+2])==2:    
                    zmienne_o.append(MCMpropagation.assignVar(gl_M,zmienne[zm],zmienne[zm+1],generator,zmienne[zm+2][0],zmienne[zm+2][1]))      
                    
                elif len(zmienne[zm+2])==3:    
                    zmienne_o.append(MCMpropagation.assignVar(gl_M,zmienne[zm],zmienne[zm+1],generator,zmienne[zm+2][0],zmienne[zm+2][1],zmienne[zm+2][2])) 
                
                else:    
                    zmienne_o.append(MCMpropagation.assignVar(gl_M,zmienne[zm],zmienne[zm+1],generator,zmienne[zm+2][0],zmienne[zm+2][1],zmienne[zm+2][2],zmienne[zm+2][3])) 

            print 'generated %s trials' % len(zmienne_o[-1].list_res)
            print 'Computation time for trials',  clock()-self.c_time
            sleep(0.5)
               
                
    def stopThreads(self): #metoda czyszczaca listy watkow
        try:
            del self.threadPool[:]
        except ValueError, e:
                QtGui.QMessageBox.warning(self, "TreadPool", str(e))
        try:
            del self.completed[:]
        except ValueError, e:
                QtGui.QMessageBox.critical(self, "Error", str(e))
        
                
    def thread3ErrorProc(self, err): #metoda obslugujaca sygnal zakonczenia dzialania 3 watku
        try:
            self.mutex.lock()
            self.ui.statusbar.showMessage("Error # %s  occurred the process has been stopped..." % err)
        finally:
            self.mutex.unlock()
            if err == 1:
                QtGui.QMessageBox.warning(self, __appname__, "Error #1: The model has been wrongly defined, calculation impossible... Please verify if any variable name is not a part of any other... ")
            else:
                QtGui.QMessageBox.warning(self, __appname__, "Error #2: The model has been wrongly defined, calculation impossible... Please verify, the model is not in line with the number of defined variables. ")
            self.ui.reset_btn.setDisabled(False)
            self.ui.oblicz_btn.setDisabled(True)
            self.ui.draw_btn.setDisabled(True)
            
    def threadISAlive(self): #metoda sprawdza aktywnosc watkow
        count = 0
        for tread in self.threadPool:
                while tread.isRunning():
                    sleep(1)
                    self.ui.progressBar.setValue(count)
                    count += 1
                sleep(2)
                
    def threadISworking(self):#metoda uruchamiana w celu wymuszenia oczekiwania na wyliczenie wartosci losowych dla zmiennych
        self.OK = True     

        if len(self.completed)>0:
            try:
                self.mutex.lock()  
                self.statusfontB()
                self.ui.statusbar.showMessage("MCM trials are loading, please wait a moment...")  
            finally:
                self.mutex.unlock()            
                QtCore.QCoreApplication.processEvents()
                
                while not self.OK:
                    self.OK = True
                    for obiekt in zmienne_o:
                        if len(obiekt.list_res) >=gl_M:
                            self.OK = True & self.OK
                        else:
                            self.OK = False 
                            
                    sleep(6)
        else:
            pass
            
        
    def generateY(self):#metoda startujaca dodatkowy watek do generowania danych 
        self.c_time = clock()        
        if gl_M >= 1000:
            self.ui.dodaj_btn.setDisabled(True)
            self.ui.draw_btn.setDisabled(True)
            self.ui.lineWyrazenie.setDisabled(True)
            self.ui.checkBox_generator.setDisabled(True)
          
            if all(self.completed) or (len(zmienne_o[-1].list_res)>= gl_M and len(zmienne_o[0].list_res)>= gl_M):
                self.ui.reset_btn.setDisabled(True)
                self.ui.line_M.setDisabled(True)
                self.ui.line_P.setDisabled(True)
                self.clearY()
                self.genZmn()
                self.ui.progressBar.setValue(0)

                QtCore.QCoreApplication.processEvents()
                self.threadPool.append(Worker2Thread(gl_M, self.z_count))
                self.connect(self.threadPool[-1], QtCore.SIGNAL("thread2Count(int)"), self.progressB)
                self.threadPool[-1].start()
                
                try:
                    self.mutex.lock() 
                    self.statusfontB()
                    self.ui.statusbar.showMessage("Data computation has been started, please wait...")  
                finally:
                    self.mutex.unlock()

                globals()["gl_wyrazenie"] = self.ui.lineWyrazenie.text()

                self.threadPool.append(Worker3Thread()) #inicjalizujemy Thread3
                self.connect(self.threadPool[-1], QtCore.SIGNAL("thread3Done(bool)"), self.thread3Done) #obsluga sygnalu thread3Done       
                self.connect(self.threadPool[-1], QtCore.SIGNAL("thread3ErrorProc(int)"), self.thread3ErrorProc) #obsluga bledow sygnalu z thread3  
                self.threadPool[-1].start()
                # "Computing data for variable workerThread 3"                
                sleep(0.5)

            else:
                QtGui.QMessageBox.warning(self, "Calculation", "Not all data are ready, please wait a moment and try again ")
                self.ui.oblicz_btn.setDisabled(False)
                self.ui.reset_btn.setDisabled(False)
        else:
            QtGui.QMessageBox.information(self, __appname__, "This program version has been designed to calculate with number of the MCM trials >= 1000. ")
    
    def statusfontB(self):
        font=QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.ui.statusbar.setFont(font)
        
    def statusfontI(self):
        font=QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.ui.statusbar.setFont(font)
        
    def progressB(self, counter): #metoda zmieniajaca wartosc paska postepu 
        if len(prop_Y) < gl_M:
            try:
                self.mutex.lock() 
                self.ui.progressBar.setValue(counter)
            finally:
                self.mutex.unlock() 
        else:
            pass
            
    def thread3Done(self,sucess): #metoda uruchamian po uzyskaniu sygnalu zakonczenia wyliczen Y
        #podajemy wyniki   
        if sucess:        
            self.PropY = MCMpropagation.Ypdf(gl_M, gl_P)#inicjacja instancji obiektu Ypdf
            self.PropY.calculate(prop_Y)
            self.recalculateR()

            try:
                self.mutex.lock() 
                self.ui.progressBar.setValue(100)
                self.statusfontI()
                self.ui.statusbar.showMessage("Ready for further calculation...")
            finally:
                self.mutex.unlock()        
                QtGui.QMessageBox.information(self, "Calculation", "Calculation completed ")
                self.ui.oblicz_btn.setDisabled(False)
                self.ui.dodaj_btn.setDisabled(True)
                self.ui.draw_btn.setDisabled(False)
                self.ui.reset_btn.setDisabled(False)
                self.ui.line_M.setDisabled(False)
                self.ui.line_P.setDisabled(False)
                self.ui.lineWyrazenie.setDisabled(True)
        else:
            self.ui.lineWyrazenie.setDisabled(False)
            self.ui.reset_btn.setDisabled(False)

        
    def recalculateR(self): #przeliczenie wartosci dla wynikow po zaokragleniu w zaleznosci od ustawienia wymaganych miejsc dziesietnych
     
        if len(self.PropY.list_res)>=gl_M:
            self.ui.Wynik_odchylenie.setText(str(round(self.PropY.uy, self.ui.spinBox.value())))
            self.ui.Wynik_srednia.setText(str(round(self.PropY.y, self.ui.spinBox.value())))
            self.ui.Wynik_przedzil.setText(str(round(self.PropY.prd, self.ui.spinBox.value())) + "  " + str(round(self.PropY.prw, self.ui.spinBox.value())))
        else:
            pass
        
    def draw(self): #metoda uruchamiajaca rysowanie histogramu nowej PDF
        if len(self.PropY.list_res) > 999:    
            self.plot(self.PropY.list_res)
        else:
            QtGui.QMessageBox.warning(self, __appname__, "There is no data to draw") 
            
    def plot(self, prop):
        plt.clf()
        num_bins = 200
# the histogram of the data
        n, bins, patches = plt.hist(prop, num_bins, normed=1, facecolor='green')

        plt.xlabel('Smarts')
        plt.ylabel('Probability density')
        plt.title(r'Histogram of IQ')
               
        self.ui.mpl.canvas.draw()

    def clearZm(self): #the methode clear out the list of variables
        self.z_count = 0
        self.ui.progressBar.setValue(0)
        self.ui.textEdit.clear()
        if len(zmienne)>0:     #czyscimy poszczegolne listy  
            try:
                del zmienne[:]
            except ValueError, e:
                QtGui.QMessageBox.warning(self, "Zmienne", str(e))  
                
    def clearZo(self):
        try:                
            del zmienne_o[:]
        except ValueError, e:
            QtGui.QMessageBox.warning(self, "Zmienne_o", str(e))
        
    def clearData(self): #metoda czysci listy uzywane jako zmienne globalne
        if len(zmienne)>0:     #czyscimy poszczegolne listy  

            self.clearZo()
            try:    
                del zmienne_n[:]
            except ValueError, e:
                QtGui.QMessageBox.warning(self, "Zmienne_n", str(e))
            try:    
                del self.completed[:]
            except ValueError, e:
                QtGui.QMessageBox.warning(self, "Zmienne_n", str(e))
                
    def clearY(self): #metoda czysci liste wartosci Y
        plt.clf() #w teorii metoda powinna czyscic obszar obiektu figure() ale tego nie robi
        self.stopThreads()
        self.PropY = None
        self.calculation_flag=0
        if len(prop_Y)>0:
            try:    
                del prop_Y[:]  
            except ValueError, e:
                QtGui.QMessageBox.warning(self, "prop_y", str(e))
            self.ui.Wynik_odchylenie.setText("0.0")
            self.ui.Wynik_przedzil.setText("0.0")
            self.ui.Wynik_srednia.setText("0.0")
        else:
            pass
                
            
    def resetW(self):#metoda resetuje wszystkie zmienne i wartosci wyswietlane na ekranie glownym
        globals()["gl_P"] = 95
        globals()["gl_M"] = 1000
        globals()["gl_wyrazenie"] =''
        globals()["exp_ver_Flag"]=0
        self.clearData()   
        self.clearZm()
        self.clearY()
        
        self.ui.line_M.setText("")
        self.ui.line_M.setDisabled(False)
        self.ui.line_P.setText("")
        self.ui.line_P.setDisabled(False)
        self.ui.lineWyrazenie.setText("")
        self.ui.lineWyrazenie.setDisabled(False)
        self.ui.checkBox_generator.setDisabled(False)
        self.ui.Wynik_odchylenie.setText("0.0")
        self.ui.Wynik_przedzil.setText("0.0")
        self.ui.Wynik_srednia.setText("0.0")
        self.ui.oblicz_btn.setDisabled(True)
        self.ui.draw_btn.setDisabled(True)
        self.ui.dodaj_btn.setDisabled(False)
        self.ui.dodaj_btn.setFocus()
        try:
            self.mutex.lock() 
            self.ui.progressBar.setValue(0)
            self.statusfontI()
            self.ui.statusbar.showMessage("Ready for further calculation...")
        finally:
            self.mutex.unlock() 
            
    def closeEvent(self, event): #metoda obslugujaca zamkniecie okna glownego
        reply = QtGui.QMessageBox.question(self, __appname__,
            "Are you sure to exit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.stopThreads()            
            event.accept()
            sys.exit()
        else:
            event.ignore()
            
    def exitApp(self): #metoda obslugujaca zakonczenie dzialania aplikacji
        reply = QtGui.QMessageBox.question(self, __appname__,
            "Are you sure to exit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.stopThreads()            
            sys.exit()
        else:        
            pass
        
    def dispAbout(self): #metoda wyswietlajaca okno About
        QtGui.QMessageBox.about(self, __appname__ + "About",
                                """MCMEstymator 1.03
Copyright 2015 Pawel Gurnecki

This program has been designed as the thesis on the end of my study.
It may be used and modified with no restrictions.                              
                                """)
                                
class Help_d(QtGui.QDialog): #definicja klasy okna dialogowego wykorzystywanego do wyswietlania pomocy
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Dialog_Help()
        self.ui.setupUi(self)
        self.ui.textBrowser.append("<font color=green><b>Help </b></font>")
        try:
            fileH = open('help.html', 'r')
            text = fileH.read()
            fileH.close()
        except ValueError as e:
            QtGui.QMessageBox.warning(self, __appname__, str(e))
        self.ui.textBrowser.append(text)                       
        
       
class Form(QtGui.QDialog): #definicja klasy okna dialogowego, formy do wprowadzania danych
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Variable_Form()
        self.ui.setupUi(self)
        for p in range(len(MCMpropagation.dict.keys())):
            self.ui.combo_Typ.addItem(MCMpropagation.dict.values()[p]['name']) 
        self.ui.combo_Typ.addItem(" ")
        self.ui.combo_Typ.setCurrentIndex(11)
        self.ui.line_Variable.setFocus()
        self.ui.OK_btn.setDefault(False)
        self.n_param = 1
        self.connect(self.ui.OK_btn, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("accept()")) 
        self.connect(self.ui.Cancel_btn, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("reject()")) 
        
        self.connect(self.ui.line_Variable, QtCore.SIGNAL("editingFinished()"), self.verifyZ) 
        self.connect(self.ui.line_Variable, QtCore.SIGNAL("returnPressed()"), self.verifyZ)
        self.connect(self.ui.combo_Typ, QtCore.SIGNAL("currentIndexChanged(int)"), self.passValue)
  
        
#weryfikujemy zawartosc pola z nowa zmienna       
    def verifyZ(self):
        powtorka = 0
        zmienna = self.ui.line_Variable.text()        
        if len(zmienna)<1:
            QtGui.QMessageBox.warning(self, "Variable", "Enter variable name. ") 
            self.ui.combo_Typ.setDisabled(True)
            self.ui.line_Variable.setText("xxx")            
            self.ui.line_Variable.setFocus()
            self.ui.line_Variable.selectAll()

        elif len(zmienna) > 0:
            for p in range(0,len(zmienne),3):
                zmienna_p = zmienne[p]                
                if str(zmienna) == str(zmienna_p):
                        powtorka = 1
                        QtGui.QMessageBox.warning(self, "Dialog", "Variable name is in use, please enter another one.") 
                        self.ui.line_Variable.clear()                        
                        self.ui.line_Variable.setFocus()
                        break
            if powtorka != 1:       
                self.ui.combo_Typ.setDisabled(False)
                self.ui.combo_Typ.setFocus()
            
           
    def cursorMove(self):
        self.ui.combo_Typ.setFocus()

#weryfikujemy czy zmienna nie zostala uzyta juz wczesniej, a jezeli wszystko jest OK, w oparciu o zdefiniowany typ propagacji inicjujemy obiekt odpowiadajacy nowej zmiennej       
    def passValue(self):
        self.ui.combo_Typ.setDisabled(True)
        powtorka = 0
        zmienna = self.ui.line_Variable.text()

        if len(zmienna) > 0:#weryfikujemy czy nie mamy juz takiej zmiennej an liscie
            for zmienna_p in zmienne:
                if str(zmienna) == str(zmienna_p):
                        powtorka = 1
                        QtGui.QMessageBox.warning(self, "Dialog", "Variable name is in use, please enter another one.") 
                        self.ui.line_Variable.clear()                        
                        self.ui.line_Variable.setFocus()
                        break
            if powtorka != 1:    
                zmienne.append(str(zmienna))
                zmienne.append(str(MCMpropagation.dict.keys()[self.ui.combo_Typ.currentIndex()]))
                self.ui.line_Variable.setDisabled(True)

        #modyfikujemy elementy okna dialogowego w zaleznosci od definiowanego typu f. propagacji
        self.ui.label_Opis.setText(MCMpropagation.descPDF[int(zmienne[-1])])
        self.n_param = MCMpropagation.dict[int(zmienne[-1])]['parm']
        self.ui.label_2.setText("Parameter 1 ")
        self.ui.linePar2.setDisabled(True)
        if self.n_param==2:  
            self.ui.label_3.setText("Parameter 2")
            self.ui.linePar2.setDisabled(False)
        if self.n_param==3:   
            self.ui.label_3.setText("Parameter 2")
            self.ui.label_4.setText("Parameter 3")
            self.ui.linePar2.setDisabled(False)
            self.ui.linePar3.setDisabled(False)
        if self.n_param==4:    
            self.ui.label_3.setText("Parameter 2")
            self.ui.label_4.setText("Parameter 3")
            self.ui.label_4.setText("Parameter 4")
            self.ui.linePar2.setDisabled(False)
            self.ui.linePar3.setDisabled(False)
            self.ui.linePar4.setDisabled(False)
        self.ui.line_Par1.setFocus()

#nadpisujemy standarowa metode aby weryfikowac poprawnosc definicji danych przed pobraniem  danych z dialogu      
    def accept(self): 
        lista_p=[]        
        class IsEmptyZ(Exception): pass
        class IsEmptyC(Exception): pass
        class IsEmpty1(Exception): pass
        class IsEmpty2(Exception): pass
        class IsEmpty3(Exception): pass
        class IsEmpty4(Exception): pass        
        
        try:
            if   len(self.ui.line_Variable.text()) == 0:
                raise IsEmptyZ, ("The Variable Name field can not be empty, add value")
            elif len(self.ui.combo_Typ.currentText()) == 0:
                raise IsEmptyC, ("Select the PDF type")
            elif len(self.ui.line_Par1.text()) == 0 or is_number(self.ui.line_Par1.text()) == False:
                raise IsEmpty1, ("Enter a value for parameter 1 field, it must be numeric")
            elif self.n_param==2 and (len(self.ui.linePar2.text()) == 0 or is_number(self.ui.linePar2.text()) == False):
                raise IsEmpty2, ("Enter a value for parameter 2 field, it must be numeric")
            elif self.n_param==3 and (len(self.ui.linePar3.text()) == 0 or is_number(self.ui.linePar3.text()) == False):
                raise IsEmpty3, ("Enter a value for parameter 3 field, it must be numeric")
            elif self.n_param==4 and (len(self.ui.linePar4.text()) == 0 or is_number(self.ui.linePar4.text()) == False):
                raise IsEmpty4, ("Enter a value for parameter 4 field, it must be numeric")
            else:
                try:
                    if self.n_param==3:
                        lista_p.append(float(self.ui.line_Par1.text()))
                        lista_p.append(float(self.ui.linePar2.text()))
                        lista_p.append(float(self.ui.linePar3.text()))

                    elif self.n_param==4:
                        lista_p.append(float(self.ui.line_Par1.text()))
                        lista_p.append(float(self.ui.linePar2.text()))
                        lista_p.append(float(self.ui.linePar3.text()))
                        lista_p.append(float(self.ui.linePar4.text()))

                    elif self.n_param==1:
                        lista_p.append(float(self.ui.line_Par1.text()))

                    else:
                        lista_p.append(float(self.ui.line_Par1.text()))
                        lista_p.append(float(self.ui.linePar2.text()))

                    zmienne.append(lista_p[0:3])    
                
                except ValueError as e:
                    QtGui.QMessageBox.warning(self, "Dialog", str(e))
                QtGui.QDialog.accept(self)
                
                
        except IsEmptyZ, e:
            QtGui.QMessageBox.warning(self, "Dialog", str(e))
            self.ui.line_Variable.selectAll()
            self.ui.line_Variable.setFocus()
            return
                
        except IsEmptyC, e:
            QtGui.QMessageBox.warning(self, "Dialog", str(e))
            self.ui.combo_Typ.setFocus()
            return
                
        except IsEmpty1, e:
            QtGui.QMessageBox.warning(self, "Dialog", str(e))
            self.ui.line_Par1.selectAll()
            self.ui.line_Par1.setFocus()
            return
                
        except IsEmpty2, e:
            QtGui.QMessageBox.warning(self, "Dialog", str(e))
            self.ui.linePar2.selectAll()
            self.ui.linePar2.setFocus()
            return
                
        except IsEmpty3, e:
            QtGui.QMessageBox.warning(self, "Dialog", str(e))
            self.ui.linePar3.selectAll()
            self.ui.linePar3.setFocus()
            return
                
        except IsEmpty4, e:
            QtGui.QMessageBox.warning(self, "Dialog", str(e))
            self.ui.linePar4.selectAll()
            self.ui.linePar4.setFocus()
            return
   
                    
    def reject(self):#metoda uruchamiana w momencie wycofania sie z okna dialogowego
        if len(zmienne)>=3:        
            #zmienne_o.remove(zmienne_o[-1]) #usuwamy z listy wczesniej utworzony obiekt
            for z in range(3):            
                zmienne.remove(zmienne[-z])
        #zmienne.remove(zmienne[-2])
        QtGui.QDialog.reject(self)

       
class Worker2Thread(QtCore.QThread): #clasa definiujaca dodatkowy watek obslugujacy pasek postepu
    
    def __init__(self, Num, LenZ, parent=None):
        super(Worker2Thread, self).__init__(parent)
        self.comp = 4
        self.Num = Num
        self.LenZ = LenZ
        
    def __del__(self):#metoda powinna konczyc watek po wykorzystaniu
        self.wait()

    def run(self):#w ramach metody run dla watku drugiega obslugujemy pasek postepu (niestety w oparciu o parametry czasowe)
               
        if self.LenZ > 4:  
            wsp = (self.LenZ-3)*0.01
        else:
            wsp = 0.001

        while self.comp<101: 
            
            if self.Num > 1000000 and self.Num <= 2000000:          
                sleep(8*wsp)
            elif self.Num > 2000000 and self.Num <= 3000000:          
                sleep(16*wsp)
            elif self.Num > 3000000 and self.Num <= 4000000:          
                sleep(32*wsp)
            elif self.Num == 1000000:
                sleep(4*wsp)
            elif self.Num > 4000000 and self.Num <= 5000000:
                sleep(60*wsp)
            elif self.Num == 500000:          
                sleep(2*wsp)   
            else:
                sleep(0.01) 
                
            self.emit(QtCore.SIGNAL("thread2Count(int)"), self.comp)
            
            self.comp+=1    

        return
           
              
class Worker3Thread(QtCore.QThread): #clasa definiujaca dodatkowego threada - wykorzystany do przeprowadzenia obliczen dla Y
   
    def __init__(self, parent=None):
        super(Worker3Thread, self).__init__(parent)
        self.mutex = QtCore.QMutex()  
        self.complete=False

    def __del__(self):#metoda powinna konczyc watek po wykorzystaniu
        self.wait()
        
    def run(self):  
        self.c_time = clock()
        
        if len(zmienne_o)==len(zmienne_n):#badam czy lista nazw ma taka sama dlugosc jak lista zdefiniowanych propagacji
            try:
                print "The expression computation has been started"
                #print 'wyrazenie', gl_wyrazenie
                self.Prop = MCMpropagation.Ypdf(gl_M, gl_P, gl_wyrazenie,zmienne_n,zmienne_o )#inicjacja instancji obiektu Ypdf
                self.Prop.procExpression()
                globals()["prop_Y"]=self.Prop.list_res
                self.complete = True
                print "The expression has been processed successfully"
                print 'Computation time for final result',  clock()-self.c_time

                
                self.emit(QtCore.SIGNAL("thread3Done(bool)"), self.complete)
            except ValueError as e:
                self.emit(QtCore.SIGNAL("thread3ErrorProc(int)"), 1)        
                print "Error: ", e
                try:
                    self.mutex.lock()
                    self.ui.statusbar.showMessage("Error # %s  occurred the process has been stopped..." % e)
                finally:
                    self.mutex.unlock()
                    QtGui.QMessageBox.warning(self, __appname__, "Error 1: The model has been wrongly defined, calculation impossible... Please verify if any variable name is not a part of any other... ")
  
        else:
            self.emit(QtCore.SIGNAL("thread3ErrorProc(int)"), 2)
            QtGui.QMessageBox.warning(self, __appname__, "Error 2: The model has been wrongly defined, calculation impossible... Please verify, the model is not in line with the number of defined variables. ")
            self.ui.reset_btn.setDisabled(False)
            self.ui.oblicz_btn.setDisabled(True)
            self.ui.draw_btn.setDisabled(True)
        

if __name__== '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()

    gl_P = 95
    gl_M = 1000
    zmienne = []
    zmienne_o = [] #lista obiektow propagacji wejsciowych
    zmienne_n = [] #lista nazw zmiennych
    prop_Y = []
    gl_wyrazenie =''
    generator = 0
    exp_ver_Flag = 0
    sys.exit(app.exec_())
