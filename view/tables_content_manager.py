import sys
from PyQt4 import QtGui, QtCore

class TableDataRepresentation(QtGui.QTableWidget):
    
    __INITIAL_TABLE_SIZE = 1

    def __init__(self, data, table_config_data, db_service_manager, table_id):
        QtGui.QTableWidget.__init__(self,self.__INITIAL_TABLE_SIZE,self.__INITIAL_TABLE_SIZE)
        self.__config_table(table_config_data)
        self.__db_service_manager =  db_service_manager
        self.__table_id = table_id
        
        self.updateData(data)

    def __config_table(self, table_config_data):
        self.setColumnCount(len(table_config_data["table_column_titles"].split(',')))
        self.setHorizontalHeaderLabels(table_config_data["table_column_titles"].split(','))

    def updateData(self, data):
        if (self.__check_data_table(data)):
            print "llenando tabla {}".format(self.__table_id)
        else:
            print "Datos Vacios {}".format(self.__table_id)

    def __check_data_table(self, data):
        return_value = True
        if not data:
            return_value= False
        elif data is None:
            return_value= False
        else:
             pass
        return return_value

    def fill_table(self):
        pass

def main():
    table_config_data = {"table_title":"steps","table_column_titles":"name, descripcion, scenario, code_step"}
    app = QtGui.QApplication(sys.argv)
    data = None
    ex = TableDataRepresentation(data, table_config_data)
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()