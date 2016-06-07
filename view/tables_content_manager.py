import sys
from PyQt4 import QtGui, QtCore
from tag_viewer import TagViewerTable


class MyTableWidgetItem(QtGui.QTableWidgetItem):
    def __lt__(self, other):
        if (isinstance(other, QtGui.QTableWidgetItem)):
            my_value, my_ok = self.data(QtCore.Qt.EditRole).toInt()
            other_value, other_ok = other.data(QtCore.Qt.EditRole).toInt()

            if (my_ok and other_ok):
                return my_value < other_value

        return super(MyTableWidgetItem, self).__lt__(other)


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
    __WHITE_SPACE_TEXT = " "
    __TAG_DESCRIPTOR = "@"

    def __init__(self, data, table_config_data, db_service_manager, table_id):
        QtGui.QTableWidget.__init__(self, self.__INITIAL_TABLE_ROW_SIZE, self.__INITIAL_TABLE_SIZE)
        self.__config_table(table_config_data)
        self.__db_service_manager = db_service_manager
        self.__table_id = table_id
        self.__tags_dictionary = {}
        self.__add_connection_to_table()
        self.__tag_viewer = TagViewerTable()

    def __add_connection_to_table(self):
        self.cellClicked.connect(self.__get_current_cell_position)

    def __config_table(self, table_config_data):
        self.setColumnCount(len(table_config_data["table_column_titles"].split(',')))
        self.setHorizontalHeaderLabels(table_config_data["table_column_titles"].split(','))
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)

    def updateData(self, query):
        if (self.__check_data_table(query)):
            self.__select_table_to_populate(query)

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
            index += 1

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
            self.setItem(index, 0, self.__createTableItem(name, QtCore.Qt.ItemIsEditable))
            self.setItem(index, 1, self.__createTableItem(description, QtCore.Qt.ItemIsEditable))
            self.setItem(index, 2, self.__createTableItem(scenario, QtCore.Qt.ItemIsEditable))
            self.setItem(index, 3, self.__createTableItem(codeStep, QtCore.Qt.ItemIsEditable))
            self.setItem(index, 4, self.__createTableItem(tags_fields, QtCore.Qt.ItemIsEditable))
            index += 1

    def __extract_tag_from_querry(self, query):
        tags_fields = self.__EMPTY_STRING
        for tag in query.scenario.tags:
            self.__insert_tag_in_dic(tag.name, str(tag.id))
            tags_fields += self.__TAG_DESCRIPTOR + tag.name
        return tags_fields

    def __populate_table_statistics(self, query):
        self.setSortingEnabled(False)
        index = self.rowCount()
        name = self.__EMPTY_STRING
        step_count = self.__EMPTY_STRING
        for rows in query:
            name = self.__check_string_is_not_None(rows.name)
            step_count = self.__check_string_is_not_None(str(rows.count))
            self.insertRow(index)
            self.setItem(index, 0, self.__createTableItem(name, QtCore.Qt.ItemIsEditable))
            self.setItem(index, 1, self.__createTableItem(step_count, QtCore.Qt.ItemIsEditable))
            index += 1
        self.setSortingEnabled(True)

    def sorting_table(self, qt_order):
        self.sortItems(0, qt_order)

    def __createTableItem(self, table_item_name, item_flag):
        return_item = MyTableWidgetItem(table_item_name)
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

    def __create_action_menu(self, action_name, action_method):
        return_action = QtGui.QAction(action_name, self)
        return_action.triggered.connect(action_method)
        return return_action

    def __order_ascending_table_view(self):
        self.sortItems(self.__column_index_selected, QtCore.Qt.AscendingOrder)

    def __insert_tag_in_dic(self, tag_name, tag_id):
        result = self.__tags_dictionary.get(tag_name)
        if result is None:
            self.__tags_dictionary[tag_name] = tag_name + ":" + tag_id

    def __get_tag_dictionary_as_list_from_selection(self, row_selection):
        row_selection_list = row_selection.split('@')
        return_list = []
        for row_tag in row_selection_list:
            if row_tag:
                return_list.append(self.__tags_dictionary[row_tag].rstrip().lstrip())
        return return_list

    def __get_complete_tag_from_dic_as_list(self):
        return self.__tags_dictionary.values()

    def __is_tag_row(self, data):
        return (self.__TAG_DESCRIPTOR in data)

    def __search_by_tag_in_current_row(self):
        data = self.__get_text_from_selected_cell()
        if self.__is_tag_row(data):
            self.__tag_viewer.set_data_to_combo_list(self.__get_tag_dictionary_as_list_from_selection(data))
            self.__tag_viewer.set_data_service(self.__db_service_manager)
            self.__tag_viewer.show()

    def __get_text_from_selected_cell(self):
        model = self.model()
        index = model.index(self.__row_index_selected, self.__column_index_selected)
        return str(model.data(index).toString())

    def __search_by_tags_in_dictionary(self):
        self.__tag_viewer.set_data_to_combo_list(self.__get_complete_tag_from_dic_as_list())
        self.__tag_viewer.set_data_service(self.__db_service_manager)
        self.__tag_viewer.show()
        print "__search_by_tags_in_dictionary"

    def __order_descending_table_view(self):
        self.sortItems(self.__column_index_selected, QtCore.Qt.DescendingOrder)

    def contextMenuEvent(self, event):
        self.__column_index_selected = self.indexAt(event.pos()).column()
        self.__row_index_selected = self.indexAt(event.pos()).row()
        menu = QtGui.QMenu(self)
        menu.addAction(self.__create_action_menu("AscendingOrder", self.__order_ascending_table_view))
        menu.addAction(self.__create_action_menu("DescingOrder", self.__order_descending_table_view))
        menu.addAction(self.__create_action_menu("Search By Tags in current Row", self.__search_by_tag_in_current_row))
        menu.addAction(self.__create_action_menu("Search By Tags", self.__search_by_tags_in_dictionary))
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
