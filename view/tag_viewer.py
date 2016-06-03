import sys
from PyQt4 import QtGui, QtCore

class TagViewerTable(QtGui.QWidget):
    __TABLE_PROPS = ["Steps Code","Step Def","Scenario","File Name"]
    __INITIAL_TABLE_SIZE = 1
    __INITIAL_TABLE_ROW_SIZE = 0
    __LABEL_TEXT = "Search Steps by Flag"
    __BUTTON_LABEL_TEXT = "Search Steps bys Flags"
    __EMPTY_STRING = ""
    __INITIAL_INDEX_VALUE = 0
    __ERROR_TEXT_STEP_NONE = "Step Text is None, Null or Empty"
    __ERROR_TEXT_INFORMATIVE_TEXT_STEP_NONE= " STEP CODE NULL"
    __ERROR_STEP_ERROR_TITLE = "STEP ERROR"
    __ERROR_STEP_DETAILLED_TEXT = " "


    def __init__(self, parent = None ):
    	super(TagViewerTable,self).__init__(parent)
        self.__result_table = QtGui.QTableWidget( self.__INITIAL_TABLE_ROW_SIZE, self.__INITIAL_TABLE_SIZE)
        self.__create_combo_box()
        self.__config_table()
        self.__create_layout()
        self.__data_service = None
        self.__tag_dictionary = {}


    def __create_dictionary_from_data(self, data):
        self.__tag_dictionary = {}
        for text_data in data:
            text_data = text_data.strip()
            flag_text = text_data.split(":")[0]
            flag_id = text_data.split(":")[1]
            self.__tag_dictionary[flag_text] = flag_id


    def __get_list_from_dictionary(self):
        return self.__tag_dictionary.keys()


    def set_data_to_combo_list(self, data):
        if not self.__list_is_empty(data):
            self.__create_dictionary_from_data(data)
            self.__load_combo_box(self.__get_list_from_dictionary())


    def __list_is_empty(self, data):
        return data is None


    def set_data_service(self, service):
        self.__data_service = service


    def __create_layout(self):
        horizontal_layout = QtGui.QHBoxLayout()
        horizontal_layout = self.__add_widget_to_layout(horizontal_layout, self.__create_label(self.__LABEL_TEXT))
        horizontal_layout = self.__add_widget_to_layout(horizontal_layout, self.__tag_comboBox)
        horizontal_layout = self.__add_widget_to_layout(horizontal_layout, self.__create_botton(self.__BUTTON_LABEL_TEXT,self.__search_steps_callback))
        vertical_layout = QtGui.QVBoxLayout()
        vertical_layout.addLayout(horizontal_layout)
        vertical_layout = self.__add_widget_to_layout(vertical_layout , self.__result_table)
        self.setLayout(vertical_layout)


    def __config_table(self):
        self.__result_table.setColumnCount(len(self.__TABLE_PROPS))
        self.__result_table.setHorizontalHeaderLabels(self.__TABLE_PROPS)


    def __add_widget_to_layout(self, layout, widget):
        layout.addWidget(widget)
        return layout


    def __create_label(self, label_text):
        label = QtGui.QLabel(label_text, self)
        label.setAlignment(QtCore.Qt.AlignCenter)
        return label


    def __create_combo_box(self):
        self.__tag_comboBox = QtGui.QComboBox(self)


    def __create_botton(self, label, callback):
        botton = QtGui.QPushButton(label, self)
        botton.clicked.connect(callback)
        botton.resize(botton.sizeHint())
        return botton


    def __load_combo_box(self, data):
        if not self.__check_data_is_not_null(data):
            for item in data:
                self.__tag_comboBox.addItem(item)


    def __check_data_is_not_null(self, data):
        return  data is None 


    def __search_steps_callback(self):
        selected_tag = str(self.__tag_comboBox.currentText())
        tag_id = self.__tag_dictionary.get(selected_tag)
        data = self.__data_service.find_steps(self.__EMPTY_STRING,int(tag_id))
        if data is not None:
            self.__populate_table_from_new_data(data)
        else:
            self.__show_error_msg(self.__ERROR_TEXT_STEP_NONE,\
                                  self.__ERROR_TEXT_INFORMATIVE_TEXT_STEP_NONE,\
                                  self.__ERROR_STEP_ERROR_TITLE,\
                                  self.__ERROR_STEP_DETAILLED_TEXT)

    def __show_error_msg(self, text, informative_text, windows_title, detailed_Text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setInformativeText(informative_text)
        msg.setWindowTitle(windows_title)
        msg.setDetailedText(detailed_Text)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()

    def __get_tag_id_from_description(self, tag_description):
        return self.__tag_dictionary[tag_description]


    def __createTableItem(self, table_item_name, item_flag):
        return_item = QtGui.QTableWidgetItem( table_item_name )
        return_item.setFlags(item_flag)
        return return_item


    def __check_string_is_not_None(self, some_string):
        if some_string is None:
            some_string = self.__EMPTY_FIELD
        return some_string


    def __populate_table_from_new_data(self, query):
    	self.__result_table.setRowCount(0)
        self.__result_table.clear()
        self.__config_table()
        index = self.__INITIAL_INDEX_VALUE
        name = self.__EMPTY_STRING
        scenario = self.__EMPTY_STRING
        codeStepFile = self.__EMPTY_STRING
        codeStepName = self.__EMPTY_STRING
        for rows in query:
            name = self.__check_string_is_not_None(rows.name)
            scenario = self.__check_string_is_not_None(rows.scenario.name)
            codeStepName = None if rows.code_step is None else rows.code_step.name
            codeStepFile = self.__check_string_is_not_None(rows.code_step.file_name)
            self.__result_table.insertRow(index)
            self.__result_table.setItem(index, 0, self.__createTableItem( name, QtCore.Qt.ItemIsEditable))
            self.__result_table.setItem(index, 1, self.__createTableItem( codeStepName, QtCore.Qt.ItemIsEditable))
            self.__result_table.setItem(index, 2, self.__createTableItem( scenario, QtCore.Qt.ItemIsEditable))
            self.__result_table.setItem(index, 3, self.__createTableItem( codeStepFile, QtCore.Qt.ItemIsEditable))
            index +=1


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName(str(TagViewerTable))
    data = ["@FVT:122","@TCID1232:1222","@TCID1233:212"]
    TagViewer = TagViewerTable()
    TagViewer.set_data_to_combo_list(data)
    TagViewer.show()
    sys.exit(app.exec_())