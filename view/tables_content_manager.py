import sys
from PyQt4 import QtGui, QtCore

class TableDataRepresentation(QtGui.QTableWidget):

    def __init__(self,data,table_config_data):
        QtGui.QTableWidget.__init__(self,table_config_data["table_title"])
        updateData(data)


    def __config_table(self, table_config_data):
        self.setColumnCount(table_config_data["table_column_count"])
        self.setHorizontalHeaderLabels(table_config_data["table_column_titles"])


    def updateData(self, data):


