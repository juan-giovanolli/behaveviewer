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
    __DEFAULT_TABLE_ROW_INDEX_ALLOW_CONTEXT_MENU = 0

    def __init__(self, data, table_config_data, db_service_manager, table_id):
        QtGui.QTableWidget.__init__(self, self.__INITIAL_TABLE_ROW_SIZE, self.__INITIAL_TABLE_SIZE)
        self.__config_table(table_config_data)
        self.__db_service_manager = db_service_manager
        self.__table_id = table_id
        self.__add_connection_to_table()




    def __add_connection_to_table(self):
        self.cellClicked.connect(self.__get_current_cell_position)



    def __config_table(self, table_config_data):
        self.setColumnCount(len(table_config_data["table_column_titles"].split(',')))
        self.setHorizontalHeaderLabels(table_config_data["table_column_titles"].split(','))
        #Contextual Menu
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)

    def updateData(self, query):
        if (self.__check_data_table(query)):
            self.__select_table_to_populate(query)
        else:
            print "Datos Vacios ---->>>> {} \n".format(self.__table_id)




    def __select_table_to_populate(self, query):
        self.setSortingEnabled(False)
        if (self.__table_id == self.__FEATURE_TABLE_ID):
            self.__populate_table_feature(query)
        elif (self.__table_id == self.__STEPS_TABLE_ID):
            self.__populate_table_step(query)
        elif (self.__table_id == self.__STATISTICS_TABLE_ID):
            self.__populate_table_statistics(query)
        self.setSortingEnabled(True)



    def __populate_table_feature(self, query):
        index = self.rowCount()
        description = self.__EMPTY_STRING
        for rows in query:
            description = self.__check_string_is_not_None(rows.description)
            self.insertRow(index)
            self.setItem(index, 0, self.__createTableItem(rows.name, QtCore.Qt.ItemIsEditable))
            self.setItem(index, 1, self.__createTableItem(description, QtCore.Qt.ItemIsEditable))
            index +=1


    def __populate_table_step(self, query):
        index = self.rowCount()
        description = self.__EMPTY_STRING
        name = self.__EMPTY_STRING
        scenario = self.__EMPTY_STRING
        codeStep = self.__EMPTY_STRING
        name = self.__EMPTY_STRING
        tags_fields = self.__EMPTY_STRING
        for rows in query:
            description = self.__check_string_is_not_None(rows.description)
            name = self.__check_string_is_not_None(rows.name)
            scenario = self.__check_string_is_not_None(rows.scenario.name)
            codeStepName = None if rows.code_step is None else rows.code_step.name
            codeStep = self.__check_string_is_not_None(codeStepName)
            tags_fields = self.__check_string_is_not_None(self.__extract_tag_from_querry(rows))
            self.insertRow(index)
            self.setItem(index, 0, self.__createTableItem( name, QtCore.Qt.ItemIsEditable))
            self.setItem(index, 1, self.__createTableItem( description, QtCore.Qt.ItemIsEditable))
            self.setItem(index, 2, self.__createTableItem( scenario, QtCore.Qt.ItemIsEditable))
            self.setItem(index, 3, self.__createTableItem( codeStep, QtCore.Qt.ItemIsEditable))
            self.setItem(index, 4, self.__createTableItem( tags_fields, QtCore.Qt.ItemIsEditable))
            index +=1

    def __extract_tag_from_querry(self,query):
        tags_fields = self.__EMPTY_STRING
        for tag in query.scenario.tags:
                tags_fields += " "+tag.name
        return tags_fields

    def __populate_table_statistics(self, query):
        print "populate table stastistics"
        self.setSortingEnabled(False)
        index = self.rowCount()
        name = self.__EMPTY_STRING
        step_count = self.__EMPTY_STRING
        for rows in query:
            name = self.__check_string_is_not_None(rows.name)
            print "row name: {}".format(name)
            step_count = self.__check_string_is_not_None(str(rows.count))
            self.insertRow(index)
            self.setItem(index, 0, self.__createTableItem(name, QtCore.Qt.ItemIsEditable))
            self.setItem(index, 1, self.__createTableItem( step_count , QtCore.Qt.ItemIsEditable))
            index +=1
        self.setSortingEnabled(True)

#Qt Event overriding
#QtCore.Qt.DescendingOrder
#QtCore.Qt.AscendingOrder
    def sorting_table(self,qt_order ):
        self.sortItems(0,qt_order)

    def __createTableItem(self, table_item_name, item_flag):
        return_item = QtGui.QTableWidgetItem( table_item_name )
        return_item.setFlags(item_flag)
        return return_item


    def __check_string_is_not_None(self, some_string):
        if some_string is None:
            some_string = self.__EMPTY_FIELD
        return some_string


    def __check_data_table(self, data):
        return_value = True
        if not data:
            return_value = False
        elif data is None:
            return_value = False
        else:
            pass
        return return_value


    def extract_data_fom_sql_table(self):
        if (self.__table_id == self.__FEATURE_TABLE_ID):
            data = self.__db_service_manager.find_features(self.__EMPTY_STRING)
        elif (self.__table_id == self.__STEPS_TABLE_ID):
            data = self.__db_service_manager.find_steps(self.__EMPTY_STRING)
        elif (self.__table_id == self.__STATISTICS_TABLE_ID):
            data = self.__db_service_manager.find_most_used_steps(self.__MAX_COUNT_VALUE)
        return data


    def __create_action_menu(self, action_name , action_method ):
        return_action = QtGui.QAction(action_name,self)
        return_action.triggered.connect(action_method)
        return return_action


    def __order_ascending_table_view(self):
        print "ascending order"
        self.sortItems(self.__column_index_selected, QtCore.Qt.AscendingOrder)


    def __order_descending_table_view(self):
        print "descending table order"
        self.sortItems(self.__column_index_selected, QtCoreQt.DescendingOrder)

    def contextMenuEvent(self, event):
        self.__column_index_selected = self.indexAt(event.pos()).column()
        menu = QtGui.QMenu(self)
        menu.addAction(self.__create_action_menu("AscendingOrder", self.__order_ascending_table_view))
        menu.addAction(self.__create_action_menu("DescingOrder", self.__order_descending_table_view))
        menu.exec_(event.globalPos())
        event.accept()
        


    def __get_current_cell_position(self, row, column):
        self.__current_row_selected = row
        self.__current_column_selected = column


    def __lt__(self, other):
        return self.__number < other.__number


def main():
    table_config_data = {"table_title": "steps", "table_column_titles": "name, descripcion, scenario, code_step"}
    app = QtGui.QApplication(sys.argv)
    data = None
    ex = TableDataRepresentation(data, table_config_data)
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
