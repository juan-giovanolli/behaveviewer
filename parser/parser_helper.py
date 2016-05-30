from model.feature import Feature
from model.scenario import Scenario
from model.tag import Tag
from model.step import Step
from model.code_step import CodeStep
from parser import Parser
import parser_constants




class ParserHelper:
    """
    This class makes use of the parser in order to create each model
    retrieving information from the file parsed
    """

    def __init__(self, filename):
        self.CODESTEP = CodeStep.create(name="CODE STEP PRUEBA")
        self._tags = []
        print "Parsing file: "  + filename
        self._parsed_data = Parser().parse_file(filename)
        self._feature = ''


    def _load_feature_with_background(self):
        feature_and_background = self._parsed_data[1]
        feature = feature_and_background[0]
        feature_name = ' '.join(feature[1])
        self._feature = feature_name #Used to create scenarios
        try:
            db_name = Feature.get(Feature.name == feature_name).name
        except:
            print 'Adding feature in the database'
            db_name = ''
        if feature_name != db_name:
            feature = Feature.create(name=feature_name)
        if len(feature_and_background) > 1:
            background = feature_and_background[1]
            scenario = self._create_scenario('background', True, [], feature)
            for step in background[1]:
                self._create_step(' '.join(step[1]), scenario, self.CODESTEP, step[0])
        return feature


    def _create_tags(self, scenario):
        """
        Reads parsed tags and add each in the database if it dowsn't exists
        """
        tags = []
        for elem in scenario:
            if elem[0] == 'tag':
                for tag in elem[1]:
                    try:
                        db_name = Tag.get(Tag.name == tag).name
                    except:
                        db_name = ''
                    if tag != db_name:
                        tags.append(Tag.create(name=tag, description=''))
        return tags


    def _create_scenario(self, name, is_background, tags, feature):
        scenario = Scenario.create(name=name, is_background=is_background, feature=feature)
        scenario.tags.add(tags)
        scenario.save()
        return scenario


    def _create_step(self, name, scenario, code_step, step_type):
        pass


    def load_scenarios(self):
        """
        Loads all scenarios in the database
        """
        feature = self._load_feature_with_background()
        list_of_scenarios = self._parsed_data[0]
        for scen in list_of_scenarios:
            scenario_name = ' '.join(scen[0][1])
            tags = self._create_tags(scen)
            scenario = self._create_scenario(name=scenario_name, is_background=False, tags=tags, feature=feature)


if __name__ == '__main__':
    parser = ParserHelper("behave.example")
    parser.load_scenarios()
