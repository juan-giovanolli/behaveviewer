import os
import csv
from config.setup import db
from gherkin_parser.parser_helper import ParserHelper
from gherkin_parser.code_parser import CodeParser
from service.entity_service import EntityService


class NoUiRun:
    def __init__(self):
        self.db_manager = EntityService()

    def parsing_directory(self, feature_directory_path=None):
        assert feature_directory_path is not None
        print feature_directory_path
        if os.path.isdir(feature_directory_path):
            feature_directory_path = unicode(feature_directory_path)
            path_to_step = os.path.join(feature_directory_path, "steps")
            db.begin()
            print "parsing directory ...."
            # CodeParser().parseDir(path_to_step)
            # ParserHelper(feature_directory_path)
            db.commit()
        else:
            print "File doesn't exist"

    def generate_csv_files(self):
        with open('steps.csv', 'wb') as csvfile:
            row_writer = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            row_writer.writerow(['Feature', 'Scenario', 'Step', 'Code Step', 'Tags'])
            for feature in self.db_manager.find_features(""):
                for step in self.db_manager.find_steps_per_feature(feature.id):
                    code_step = self.db_manager.find_code_step(step.name)
                    if not code_step:
                        code_step = ''
                    for tag in step.scenario.tags:
                        new_row = [feature.name, step.scenario.name, step.name, code_step, tag.name]
                        print new_row
                        row_writer.writerow(new_row)


def main_no_ui(feature_directory_path=None):
    assert feature_directory_path, "No feature path given"
    NoUiRun().parsing_directory(feature_directory_path)
    NoUiRun().generate_csv_files()
