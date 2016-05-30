from model.feature import Feature
from model.tag import Tag
from parser import Parser
import parser_constants


class ParserHelper:
    """
    This class makes use of the parser in order to create each model
    retrieving information from the file parsed
    """

    def __init__(self, filename):
        self._tags = []
        print "Parsing file: "  + filename
        self._parsed_data = Parser().parse_file(filename)


    def load_feature_with_background(self):
        feature_and_background = self._parsed_data[1]


    def create_tags(self, scenario):
        """
        Reads parsed tags and add each in the database if it dowsn't exists
        """
        for elem in scenario:
            if elem[0] == 'tag':
                for tag in elem[1]:
                    try:
                        db_name = Tag.get(Tag.name == tag).name
                    except:
                        db_name = ''
                    if tag != db_name:
                        self._tags.append(Tag.create(name=tag, description=''))

    def create_scenarios(self):
        pass


    def load_scenarios(self):
        """
        Loads all scenarios in the database
        """
        list_of_scenarios = self._parsed_data[0]
        feature = Feature()
        for scenario in list_of_scenarios:
            self._create_tags(scenario)

            if self._parsed_data[n_of_scenario][0][0].lower() == 'feature:':
                parsed_name = ' '.join(self._parsed_data[0][0][1])
                try:
                    db_name = Feature.get(Feature.name == parsed_name).name
                except:
                    db_name = ''
                if parsed_name != db_name:
                    Feature.create(name=parsed_name)
            if .lower() == 'tag:':
                list_of_tags = self._parsed_data[n_of_scenario][0][1]
                for parsed_name in list_of_tags:
                    try:
                        db_name = Tag.get(Tag.name == parsed_name).name
                    except:
                        db_name = ''
                    if parsed_name != db_name:
                        tags.append(Tag.create(name=parsed_name, description=''))
            if self._parsed_data[n_of_scenario][0][0].lower() == 'scenario:':
                parsed_name = ' '.join(self._parsed_data[n_of_scenario][0][1])
                try:
                    db_name = Scenario.get(Scenario.name == parsed_name).name
                except:
                    db_name = ''
                #if parsed_name != db_name:
                #    Scenario.create(name=parsed_name, description='', Feature.get(Feature.name == parsed_name))
    #name = CharField()
    #description = CharField()
    #feature = ForeignKeyField(Feature, related_name='scenarios')
    #tags = ManyToManyField(Tag, related_name='scenarios')


if __name__ == '__main__':
    parser = ParserHelper("behave.example")
    parser.load_scenarios()