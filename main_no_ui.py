import os
from config.setup import db
from gherkin_parser.parser_helper import ParserHelper
from gherkin_parser.code_parser import CodeParser


class NoUiRun:
    def __init__(self):
        pass

    def parsing_directory(self, feature_directory_path=None):
        assert feature_directory_path is not None
        if os.path.isfile():
            feature_directory_path = unicode(feature_directory_path)
            path_to_step = os.path.join(feature_directory_path, "steps")
            db.begin()
            CodeParser().parseDir(path_to_step)
            ParserHelper(feature_directory_path)
            db.commit()
            print "parsing directory ...."


def main_no_ui(feature_directory_path=None):
    assert feature_directory_path, "No feature path given"
    NoUiRun().parsing_directory(feature_directory_path)
