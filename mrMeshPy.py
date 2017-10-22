#!/usr/bin/python

'''
The main mrMeshPy qapplication window built with Qt5

Andre' Gouws 2017
'''


import sys
import vtk

# some local modules
from mrMeshPyQtTCPServer import mrMeshPyQtTCPServer
from mp_MainWindow import Ui_MrMeshMainWindow
from mp_MenuCallbacks import Ui_setupMenuBarCallbacks
from mp_setupVTKWindow import mrMeshVTKWindow

# for the gui
from PyQt5 import QtCore, QtGui, QtNetwork, QtWidgets


#for debugging/testing
debug = False
test = False


class mrMeshPyMainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent = None):

        # set up the initial user interface window on Qt
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MrMeshMainWindow()
        self.ui.setupUi(self)


        # set up a tcp server instance (Qt TCP server)
        self.server = mrMeshPyQtTCPServer(self)
        self.ui.TCP_server = self.server ## this puts the service instance into the scope of the user interface (ui) 


        # TODO - hard code TCP port 9999 for now #next available may be better
        if not self.server.listen(QtNetwork.QHostAddress('127.0.0.1'), 9999):
            print('Error starting TCP instance on requested port - quitting.')
            return
        print('Running TCP instance on port %d' % self.server.serverPort())


        # set up the menu bar in the UI window with its callbacks
        Ui_setupMenuBarCallbacks(self.ui)
        

        # lets keep track of how many vtk instances are open in a list that is in the scope of the ui
        self.ui.vtkInstances = [] #empty for now
        self.ui.statusbar.showMessage(' ... Waiting for matlab to send a mesh ...')



        # ---Ready to go unless testing/debugging ---------------------------------

        # some debug options
        if debug:
            # ---------------
            # add a vtk window!
            mrMeshVTKWindow(self.ui, 'debug')
            self.ui.statusbar.showMessage(' ... in debug mode; loaded test VTK window ...')            

            def testMenuPrint(self):
                print('test menu print message')
    
            print(dir(self.ui.actionDraw))
            self.ui.actionDraw.triggered.connect(testMenuPrint)
        
        # some other test options    
        if test:
            from testRender import mp_launchVTKWindow   
            mp_launchVTKWindow(self.ui)

        # -------------------------------------------------------------------------




if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = mrMeshPyMainWindow()
    window.show()
    sys.exit(app.exec_())

