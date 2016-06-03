import os
from config.setup import db
from gherkin_parser.parser_helper import ParserHelper


def parsing_directory(self, feature_directory_path=None):
    # TODO: Crear variable que setea estado de la aplicacion
    if self.__feature_directory_path is not None:
        self.setTextInVerboseLabel("Seletcted Path : {0}".format(feature_directory_path))
        print "Path Seleccionado: {0}".format(self.__feature_directory_path)
        self.setTextInVerboseLabel("parsing directory ....")
        self.__save_current_directory_to_file()
        self.__process_directory_name()
        path_to_step = os.path.join(self.__feature_directory_path, "steps")
        db.begin()
        self.__code_parser.parseDir(path_to_step)
        ParserHelper(self.__feature_directory_path)
        db.commit()
        print "parsing directory ...."
        self.__save_current_directory_to_file()


def main_no_ui(feature_directory_path=None):
    assert feature_directory_path, "No feature path given"
    parsing_directory(feature_directory_path)
