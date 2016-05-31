'''
Created on 24 de may. de 2016

@author: Juan
'''
import sys
from PyQt4 import QtGui, QtCore
from config.setup import Setup
from service.entity_service import EntityService
from view.main_window import MainBehaveWindow

def main():
    Setup({'reset_db':True, 'dummy_db':False})

    app = QtGui.QApplication(sys.argv)
    ex = MainBehaveWindow(EntityService())
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()