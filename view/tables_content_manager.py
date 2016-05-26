import sys
from PyQt4 import QtGui, QtCore

class TableDataRepresentation(QtGui.QTableWidget):

    def __init__(self,data,table_config_data):
        QtGui.QTableWidget.__init__(self,1,1)
        self.__config_table(table_config_data)
        self.updateData(data)

    def __config_table(self, table_config_data):
        self.setColumnCount(len(table_config_data["table_column_titles"].split(',')))
        self.setHorizontalHeaderLabels(table_config_data["table_column_titles"].split(','))

    def updateData(self, data):
        if (self.__check_data_table(data)):
            print "llenado tabla"
        else:
            print "Datos Vacios"

    def __check_data_table(self, data):
        return_value = True
        if not data:
            return_value= False
        elif data is None:
            return_value= False
        else:
             pass

        return return_value


def main():
    table_config_data = {"table_title":"steps","table_column_titles":"name, descripcion, scenario, code_step"}
    app = QtGui.QApplication(sys.argv)
    data = None
    ex = TableDataRepresentation(data, table_config_data)
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()