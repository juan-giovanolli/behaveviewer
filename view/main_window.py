import sys
import time
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread, SIGNAL
from tables_content_manager import TableDataRepresentation
from service_worker_thread import ServiceThread

class MainBehaveWindow(QtGui.QTabWidget):

    __WINDOWS_POS_X = 300
    __WINDOWS_POS_Y = 300
    __WINDOWS_WEIGHT = 800
    __WINDOWS_HEIGHT = 400
    __TAB_FEATURE_INDEX = 1
    __TAB_STEP_INDEX = 2
    __TAB_STATISTICS_INDEX = 3
    #TODO: change this to make this code multi-platform
    __CURRENT_PATH_LINUX = "."
    __EMPTY_TEXT = ""
    __APP_NAME = 'Behave Links'
    __MAIN_LABEL_TEXT = "Features Directory: "
    __TABLE_CONFIG = {"steps_table":{"table_column_titles":"name, descripcion, scenario, code_step"},
                      "feature_table":{"table_column_titles":"name, descripcion"},
                      "statistics_table":{"table_column_titles":"name, descripcion, scenario, code_step"}
                      }

    def __init__(self):
        super(MainBehaveWindow, self).__init__()
        self.__is_feature_directory_loaded=False
        self.initUI()
        self.__create_function_map_for_worker()
        self.__service_worker = ServiceThread(self._function_dictionary)
        #conectando funcion a la finalizacion del thread
        self.connect(self.__service_worker, SIGNAL("finished()"), self._process_terminated)


    def initUI(self):
        self.__create_tabs()
        self.__register_all_tabs()
        self.__lock_unlock_tabs(self.__is_feature_directory_loaded)
        self.setGeometry(self.__WINDOWS_POS_X, self.__WINDOWS_POS_Y, self.__WINDOWS_WEIGHT, self.__WINDOWS_HEIGHT)
        self.setWindowTitle(self.__APP_NAME)
        self.show()


    def __create_botton(self, label, callback,config_dict):
        botton = QtGui.QPushButton( label, self)
        botton.clicked.connect( callback)
        botton.resize( botton.sizeHint())
        botton.move( int(config_dict["X_POS"]), int(config_dict["Y_POS"]))
        return botton

    def __load_feature_directory(self):
        print "loading features directory"
        #TODO: Este codigo esta en verificacion
        self.__show_dialog_find_files()

    def __lock_unlock_tabs(self, lock_status):
        self.setTabEnabled(self.__TAB_FEATURE_INDEX, lock_status )
        self.setTabEnabled(self.__TAB_STEP_INDEX, lock_status )
        self.setTabEnabled(self.__TAB_STATISTICS_INDEX, lock_status)


    def __register_all_tabs(self):
        self.__register_tab(self.__main_tab,"MainTab")
        self.__register_tab(self.__feature_tab,"Features")
        self.__register_tab(self.__steps_tab,"Steps")
        self.__register_tab(self.__statistics_tab,"Statistics")


    def __create_main_tab(self):
        self.__main_tab = QtGui.QWidget()
        self.main_tab_layout = QtGui.QVBoxLayout()
        horizontal_layout = QtGui.QHBoxLayout()
        horizontal_layout.addWidget(self.__create_label(self.__MAIN_LABEL_TEXT))
        horizontal_layout.addStretch(1)
        boton_config= {"X_POS":"300","Y_POS":"70"}
        horizontal_layout.addWidget(self.__create_botton("Load Feature Directory: ", self.__load_feature_directory,boton_config))
        horizontal_layout.addStretch(1)
        self.main_tab_layout.addLayout(horizontal_layout)
        boton_config["X_POS"]="300"
        boton_config["Y_POS"]="50"
        self.__process_label_verbose=self.__create_label(self.__EMPTY_TEXT)
        self.main_tab_layout.addWidget(self.__process_label_verbose)
        self.main_tab_layout.addStretch(1)
        self.main_tab_layout.addWidget(self.__create_botton("Quit",QtCore.QCoreApplication.instance().quit,boton_config))
        self.__main_tab.setLayout(self.main_tab_layout)

    def __create_label(self, label_text):
        label = QtGui.QLabel(label_text,self)
        label.setAlignment(QtCore.Qt.AlignCenter)
        return label


    def __create_features_tab(self):
        self.__feature_tab = QtGui.QWidget()
        features_tab_layout = QtGui.QVBoxLayout()
        features_tab_layout.addWidget(TableDataRepresentation(None, self.__TABLE_CONFIG["feature_table"]))
        self.__feature_tab.setLayout(features_tab_layout)

    def __create_steps_tab(self):
        self.__steps_tab = QtGui.QWidget()
        step_tab_layout = QtGui.QVBoxLayout()
        step_tab_layout.addWidget(TableDataRepresentation(None, self.__TABLE_CONFIG["steps_table"]))
        self.__steps_tab.setLayout(step_tab_layout)


    def __create_statistics_tab(self):
        self.__statistics_tab = QtGui.QWidget()
        statistics_tab_layout = QtGui.QVBoxLayout()
        statistics_tab_layout.addWidget(TableDataRepresentation(None, self.__TABLE_CONFIG["statistics_table"]))
        self.__statistics_tab.setLayout(statistics_tab_layout)

    def __register_tab(self, tab, tab_label):
        self.addTab(tab, tab_label)


    def __show_dialog_find_files(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        #TODO: change this to make this code multi-platform
        feature_directory_path = None
        feature_directory_path = QtGui.QFileDialog.getExistingDirectory(self, 'SelectDirectory',\
                                                                self.__CURRENT_PATH_LINUX,\
                                                                options)
        self.__service_worker.start()


    def parsing_directory(self,feature_directory_path = None):
        #TODO: Crear variable que setea estado de la aplicacion
        if feature_directory_path is not None:
            self.setTextInVerboseLabel("Seletcted Path : {0}".format(feature_directory_path))
            time.sleep(1)
            print "Path Seleccionado: {0}".format(feature_directory_path)
            self.setTextInVerboseLabel("parsing directory ....")
            time.sleep(1)
            print "parsing directory ...."


    def creating_db_tables(self):
        self.setTextInVerboseLabel("create DataBase tables .....")
        time.sleep(1)
        print "create DataBase tables ....."


    def fill_view_tables_with_sql(self):
        print "Filling View tables from SQL Sentences........."
        self.setTextInVerboseLabel("Filling View tables from SQL Sentences.........")
        time.sleep(1)
        self.__fill_steps_table()
        self.__fill_feature_table()
        self.__fill_statistics_table()


    def __fill_steps_table(self):
        self.setTextInVerboseLabel("fill_steps_table")
        time.sleep(1)
        print "fill_steps_table"


    def __fill_feature_table(self):
        self.setTextInVerboseLabel("__fill_feature_table")
        time.sleep(1)
        print "__fill_feature_table"


    def __fill_statistics_table(self):
        self.setTextInVerboseLabel("__fill_statistics_table")
        time.sleep(1)
        print "__fill_statistics_table"


    def __create_tabs(self):
        self.__create_main_tab()
        self.__create_features_tab()
        self.__create_steps_tab()
        self.__create_statistics_tab()


    def __create_function_map_for_worker(self):
        self._function_dictionary = {"PARSING_DIRECTORY: ":self.parsing_directory,\
                                     "CREATING_DB_TABLES:":self.creating_db_tables,\
                                     "FILL_VIEW_TABLE: ":self.fill_view_tables_with_sql\
                                     }

    def _process_terminated(self):
        self.setTextInVerboseLabel("Process Terminated")
        self.__lock_unlock_tabs( True)


    def setTextInVerboseLabel(self, label_text):
        self.__process_label_verbose.clear()
        self.__process_label_verbose.setText(label_text)

def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainBehaveWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

