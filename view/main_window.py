import sys
import os
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL
from tables_content_manager import TableDataRepresentation
from service_worker_thread import ServiceThread
from gherkin_parser.parser_helper import ParserHelper
from gherkin_parser.code_parser import CodeParser


class MainBehaveWindow(QtGui.QTabWidget):

    __WINDOWS_POS_X = 300
    __WINDOWS_POS_Y = 300
    __WINDOWS_WEIGHT = 800
    __WINDOWS_HEIGHT = 400
    __TAB_FEATURE_INDEX = 1
    __TAB_STEP_INDEX = 2
    __TAB_STATISTICS_INDEX = 3
    # TODO: change this to make this code multi-platform
    __CURRENT_PATH_LINUX = "."
    __EMPTY_TEXT = ""
    __APP_NAME = 'Behave Links'
    __MAIN_LABEL_TEXT = "Features Directory: "

    __FEATURE_TABLE_ID = "feature_table"
    __STEPS_TABLE_ID = "steps_table"
    __STATISTICS_TABLE_ID = "statistics_table"
    __DEFAULT_CONFIG_FILE = "config_behavior_viewer.conf"

    __TABLE_CONFIG = {"steps_table": {"table_column_titles": "name, descripcion, scenario, code_step, Tags"},
                      "feature_table": {"table_column_titles": "name, descripcion"},
                      "statistics_table": {"table_column_titles": "Most Used Step name, Count"}
                      }

    def __init__(self, db_service_manager):
        super(MainBehaveWindow, self).__init__()
        self.__is_feature_directory_loaded = False
        self.__feature_directory_path = None
        self.__code_parser = CodeParser()
        self.__db_service_manager = db_service_manager
        self.__step_table = TableDataRepresentation(None, self.__TABLE_CONFIG[self.__STEPS_TABLE_ID], self.__db_service_manager, self.__STEPS_TABLE_ID)
        self.__feature_table = TableDataRepresentation(None, self.__TABLE_CONFIG[self.__FEATURE_TABLE_ID], self.__db_service_manager, self.__FEATURE_TABLE_ID)
        self.__statistics_table = TableDataRepresentation(None, self.__TABLE_CONFIG[self.__STATISTICS_TABLE_ID], self.__db_service_manager, self.__STATISTICS_TABLE_ID)
        self.initUI()
        self.__create_function_map_for_worker()
        self.__service_worker = ServiceThread(self._function_dictionary)
        # conectando funcion a la finalizacion del thread
        self.connect(self.__service_worker, SIGNAL("finished()"), self._process_terminated)

    def initUI(self):
        self.__create_tabs()
        self.__register_all_tabs()
        self.__lock_unlock_tabs(self.__is_feature_directory_loaded)
        self.setGeometry(self.__WINDOWS_POS_X, self.__WINDOWS_POS_Y, self.__WINDOWS_WEIGHT, self.__WINDOWS_HEIGHT)
        self.setWindowTitle(self.__APP_NAME)
        self.show()

    def __create_botton(self, label, callback, config_dict):
        botton = QtGui.QPushButton(label, self)
        botton.clicked.connect(callback)
        botton.resize(botton.sizeHint())
        botton.move(int(config_dict["X_POS"]), int(config_dict["Y_POS"]))
        return botton

    def __load_feature_directory(self):
        print "loading features directory"
        # TODO: Este codigo esta en verificacion
        self.__show_dialog_find_files()

    def __lock_unlock_tabs(self, lock_status):
        self.setTabEnabled(self.__TAB_FEATURE_INDEX, lock_status)
        self.setTabEnabled(self.__TAB_STEP_INDEX, lock_status)
        self.setTabEnabled(self.__TAB_STATISTICS_INDEX, lock_status)

    def __register_all_tabs(self):
        self.__register_tab(self.__main_tab, "MainTab")
        self.__register_tab(self.__feature_tab, "Features")
        self.__register_tab(self.__steps_tab, "Steps")
        self.__register_tab(self.__statistics_tab, "Statistics")

    def __create_main_tab(self):
        self.__main_tab = QtGui.QWidget()
        self.main_tab_layout = QtGui.QVBoxLayout()
        horizontal_layout = QtGui.QHBoxLayout()
        horizontal_layout.addWidget(self.__create_label(self.__MAIN_LABEL_TEXT))
        horizontal_layout.addStretch(1)
        boton_config = {"X_POS": "300", "Y_POS": "70"}
        horizontal_layout.addWidget(self.__create_botton("Load Feature Directory: ", self.__load_feature_directory, boton_config))
        horizontal_layout.addStretch(1)
        self.main_tab_layout.addLayout(horizontal_layout)
        boton_config["X_POS"] = "300"
        boton_config["Y_POS"] = "50"
        self.__process_label_verbose = self.__create_label(self.__EMPTY_TEXT)
        self.main_tab_layout.addWidget(self.__process_label_verbose)
        self.main_tab_layout.addStretch(1)
        boton_config["X_POS"] = "300"
        boton_config["Y_POS"] = "40"
        self.main_tab_layout.addWidget(self.__create_botton("Load Only Tables: ", self.__load_only_tables_view, boton_config))
        self.main_tab_layout.addStretch(1)
        self.main_tab_layout.addWidget(self.__create_botton("Quit", QtCore.QCoreApplication.instance().quit, boton_config))
        self.__main_tab.setLayout(self.main_tab_layout)

    def __create_label(self, label_text):
        label = QtGui.QLabel(label_text, self)
        label.setAlignment(QtCore.Qt.AlignCenter)
        return label

    def __create_features_tab(self):
        self.__feature_tab = QtGui.QWidget()
        features_tab_layout = QtGui.QVBoxLayout()
        features_tab_layout.addWidget(self.__feature_table)
        self.__feature_tab.setLayout(features_tab_layout)

    def __create_steps_tab(self):
        self.__steps_tab = QtGui.QWidget()
        step_tab_layout = QtGui.QVBoxLayout()
        step_tab_layout.addWidget(self.__step_table)
        self.__steps_tab.setLayout(step_tab_layout)

    def __create_statistics_tab(self):
        self.__statistics_tab = QtGui.QWidget()
        statistics_tab_layout = QtGui.QVBoxLayout()
        statistics_tab_layout.addWidget(self.__statistics_table)
        self.__statistics_tab.setLayout(statistics_tab_layout)

    def __register_tab(self, tab, tab_label):
        self.addTab(tab, tab_label)

    def __show_dialog_find_files(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        # TODO: change this to make this code multi-platform
        self.__feature_directory_path = None
        self.__feature_directory_path = QtGui.QFileDialog.getExistingDirectory(self, 'SelectDirectory',
                                                                               self.__CURRENT_PATH_LINUX,
                                                                               options)
        # self.__service_worker.start()
        self.__run_sequencial()

    def parsing_directory(self, feature_directory_path=None):
        # TODO: Crear variable que setea estado de la aplicacion
        if self.__feature_directory_path is not None:
            self.setTextInVerboseLabel("Seletcted Path : {0}".format(feature_directory_path))
            self.setTextInVerboseLabel("parsing directory ....")
            self.__save_current_directory_to_file()
            self.__process_directory_name()
            path_to_step = os.path.join(self.__feature_directory_path, "steps")
            self.__code_parser.parseDir(path_to_step)
            ParserHelper(path_to_step)
            self.__save_current_directory_to_file()

    def creating_db_tables(self):
        self.setTextInVerboseLabel("create DataBase tables .....")


    def fill_view_tables_with_sql(self):

        self.setTextInVerboseLabel("Filling View tables from SQL Sentences.........")
        self.__fill_steps_table()
        self.__fill_feature_table()
        self.__fill_statistics_table()

    def __fill_steps_table(self):
        self.setTextInVerboseLabel("fill_steps_table")
        data = self.__step_table.extract_data_fom_sql_table()
        self.__step_table.updateData(data)


    def __fill_feature_table(self):
        self.setTextInVerboseLabel("__fill_feature_table")
        data = self.__feature_table.extract_data_fom_sql_table()
        self.__feature_table.updateData(data)


    def __fill_statistics_table(self):
        self.setTextInVerboseLabel("__fill_statistics_table")
        data = self.__statistics_table.extract_data_fom_sql_table()
        self.__statistics_table.updateData(data)


    def __create_tabs(self):
        self.__create_main_tab()
        self.__create_features_tab()
        self.__create_steps_tab()
        self.__create_statistics_tab()

    def __create_function_map_for_worker(self):
        self._function_dictionary = {"PARSING_DIRECTORY: ": self.parsing_directory,
                                     "CREATING_DB_TABLES:": self.creating_db_tables,
                                     "FILL_VIEW_TABLE: ": self.fill_view_tables_with_sql
                                     }

    def _process_terminated(self):
        self.setTextInVerboseLabel("Process Terminated")
        self.__lock_unlock_tabs(True)

    def setTextInVerboseLabel(self, label_text):
        self.__process_label_verbose.clear()
        self.__process_label_verbose.setText(label_text)

    def __run_sequencial(self):
        self.parsing_directory()
        self.fill_view_tables_with_sql()
        self._process_terminated()

    def __save_current_directory_to_file(self):
        with open(self.__DEFAULT_CONFIG_FILE, "w") as output_file:
            output_file.write(self.__feature_directory_path)

    def __load_feature_directory_from_file(self):
        with open(self.__DEFAULT_CONFIG_FILE, 'r') as input_file:
            self.__feature_directory_path = input_file.readlines()

    def __load_only_tables_view(self):
        if self.__feature_directory_path is None:
            self.__load_feature_directory_from_file()

        self.fill_view_tables_with_sql()
        self._process_terminated()

    def __reset_labels(self):
        self.setTextInVerboseLabel("")

    def __process_directory_name(self):
        self.__feature_directory_path = unicode(self.__feature_directory_path)


def main():
    app = QtGui.QApplication(sys.argv)
    MainBehaveWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
