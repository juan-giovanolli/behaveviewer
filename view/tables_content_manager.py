import sys
from PyQt4 import QtGui, QtCore

class TableDataRepresentation(QtGui.QTableWidget):
    __FEATURE_TABLE_ID = "feature_table"
    __STEPS_TABLE_ID = "steps_table"
    __STATISTICS_TABLE_ID = "statistics_table"
    __INITIAL_TABLE_SIZE = 1
    __INITIAL_TABLE_ROW_SIZE = 0
    __EMPTY_STRING = ""
    __MAX_COUNT_VALUE = 5
    __EMPTY_FIELD = "EMPTY_FIELD"

    def __init__(self, data, table_config_data, db_service_manager, table_id):
        QtGui.QTableWidget.__init__(self,self.__INITIAL_TABLE_ROW_SIZE ,self.__INITIAL_TABLE_SIZE)
        self.__config_table(table_config_data)
        self.__db_service_manager =  db_service_manager
        self.__table_id = table_id


    def __config_table(self, table_config_data):
        self.setColumnCount(len(table_config_data["table_column_titles"].split(',')))
        self.setHorizontalHeaderLabels(table_config_data["table_column_titles"].split(','))

    def updateData(self, query):
        if (self.__check_data_table(query)):
            self.__select_table_to_populate(query)
        else:
            print "Datos Vacios ---->>>> {} \n".format(self.__table_id)


    def __select_table_to_populate(self,query):
         if ( self.__table_id==self.__FEATURE_TABLE_ID ):
            self.__populate_table_feature(query)
         elif ( self.__table_id==self.__STEPS_TABLE_ID ):
            self.__populate_table_step(query)
         elif ( self.__table_id==self.__STATISTICS_TABLE_ID ) :
            self.__populate_table_statistics(query)

    def __populate_table_feature(self, query):
        index = self.rowCount()
        description = self.__EMPTY_STRING
        for rows in query:
            description = self.__check_string_is_not_None(rows.description)
            self.insertRow(index)
            self.setItem(index, 0, QtGui.QTableWidgetItem(rows.name))
            self.setItem(index, 1, QtGui.QTableWidgetItem(description))
            index +=1


    def __populate_table_step(self, query):
        index = self.rowCount()
        description = self.__EMPTY_STRING
        name = self.__EMPTY_STRING
        scenario = self.__EMPTY_STRING
        codeStep = self.__EMPTY_STRING
        name = self.__EMPTY_STRING
        for rows in query:
            description = self.__check_string_is_not_None(rows.description)
            name = self.__check_string_is_not_None(rows.name)
            scenario = self.__check_string_is_not_None(rows.scenario.name)
            codeStepName = None if rows.code_step == None else rows.code_step.name
            codeStep = self.__check_string_is_not_None(codeStepName)
            self.insertRow(index)
            self.setItem(index, 0, QtGui.QTableWidgetItem(name))
            self.setItem(index, 1, QtGui.QTableWidgetItem(description))
            self.setItem(index, 2, QtGui.QTableWidgetItem(scenario))
            self.setItem(index, 3, QtGui.QTableWidgetItem(codeStep))
            index +=1


    def __populate_table_statistics(self, query):
        print "populate table stastistics"
        index = self.rowCount()
        name = self.__EMPTY_STRING
        step_count = self.__EMPTY_STRING
        for rows in query:
            name = self.__check_string_is_not_None(rows.name)
            print "row name: {}".format(name)
            step_count = self.__check_string_is_not_None(str(rows.count))
            self.insertRow(index)
            self.setItem(index, 0, QtGui.QTableWidgetItem(name))
            self.setItem(index, 1, QtGui.QTableWidgetItem(step_count))
            index +=1


    def __check_string_is_not_None(self, some_string):
        if some_string is None:
            some_string = self.__EMPTY_FIELD
        return some_string

    def __check_data_table(self, data):
        return_value = True
        if not data:
            return_value= False
        elif data is None:
            return_value= False
        else:
             pass
        return return_value

    def extract_data_fom_sql_table(self):
        if ( self.__table_id==self.__FEATURE_TABLE_ID ) :
            data = self.__db_service_manager.find_features(self.__EMPTY_STRING)
        elif ( self.__table_id==self.__STEPS_TABLE_ID ) :
            data = self.__db_service_manager.find_steps(self.__EMPTY_STRING)
        elif ( self.__table_id==self.__STATISTICS_TABLE_ID ) :
            data = self.__db_service_manager.find_most_used_steps(self.__MAX_COUNT_VALUE)
        return data

def main():
    table_config_data = {"table_title":"steps","table_column_titles":"name, descripcion, scenario, code_step"}
    app = QtGui.QApplication(sys.argv)
    data = None
    ex = TableDataRepresentation(data, table_config_data)
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()