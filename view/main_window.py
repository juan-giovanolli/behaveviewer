import sys
from PyQt4 import QtGui, QtCore


class MainBehaveWindow(QtGui.QTabWidget):

    __WINDOWS_POS_X = 300
    __WINDOWS_POS_Y = 300
    __WINDOWS_WEIGHT = 800
    __WINDOWS_HEIGHT = 400
    __TAB_FEATURE_INDEX = 1
    __TAB_STEP_INDEX = 2
    __TAB_STATISTICS_INDEX = 3
    __MAIN_LABEL_TEXT = "Features Directory: "

    def __init__(self):
        super(MainBehaveWindow, self).__init__()
        self.__is_feature_directory_loaded=False
        self.initUI()


    def initUI(self):
        self.__create_tabs()
        self.__register_all_tabs()
        self.__lock_unlock_tabs(self.__is_feature_directory_loaded)
        self.setGeometry(self.__WINDOWS_POS_X, self.__WINDOWS_POS_Y, self.__WINDOWS_WEIGHT, self.__WINDOWS_HEIGHT)
        self.setWindowTitle('Behave Links')
        self.show()


    def __create_botton(self, label, callback,config_dict):
        botton = QtGui.QPushButton( label, self)
        botton.clicked.connect( callback)
        botton.resize( botton.sizeHint())
        botton.move( int(config_dict["X_POS"]), int(config_dict["Y_POS"]))
        return botton

    def __load_feature_directory(self):
        print "loading features directory"
        self.__is_feature_directory_loaded=True
        self.__lock_unlock_tabs( self.__is_feature_directory_loaded)

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
        self.main_tab_layout.addWidget(self.__create_botton("Quit",QtCore.QCoreApplication.instance().quit,boton_config))
        self.__main_tab.setLayout(self.main_tab_layout)

    def __create_label(self, label_text):
        label = QtGui.QLabel(label_text,self)
        #label.setText(label_text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        #label.setReadOnly(True)
        return label


    def __create_features_tab(self):
        self.__feature_tab = QtGui.QWidget()


    def __create_steps_tab(self):
        self.__steps_tab = QtGui.QWidget()


    def __create_statistics_tab(self):
        self.__statistics_tab = QtGui.QWidget()

    def __register_tab(self, tab, tab_label):
        self.addTab(tab, tab_label)


    def __show_dialog_find_files(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, 'OpenFile')
        self.myTextBox.setText(fileName)

    def __create_tabs(self):
        self.__create_main_tab()
        self.__create_features_tab()
        self.__create_steps_tab()
        self.__create_statistics_tab()

def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainBehaveWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

