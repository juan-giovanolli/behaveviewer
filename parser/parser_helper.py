from model.Feature import Feature
from parser import Parser


class ParserHelper:
    """
    This class makes use of the parser in order to create each model
    retrieving information from the file parsed
    """

    def __init__(self, filename):
        self.parsed_data = Parser().parse_file(filename)


    def get_feature(self, n_of_scenario):
        """
        If the feature already exists, it returns the feature from de database,
        otherwise, it creates a new in the database and returns it.
        """
        if len(self.parsed_data) > n_of_scenario:
            parsed_name = ' '.join(self.parsed_data[n_of_scenario][0][1])
            try:
                db_name = Feature.get(Feature.name == parsed_name).name
            except:
                db_name = ''
            if parsed_name != db_name:
                return Feature.create(name=parsed_name)
            else:
                return Feature.get(Feature.name == parsed_name)
        else:
            return False


    def load_features(self):
        """
        Loads all features in the database
        """
        for index in xrange(len(self.parsed_data)):
            parsed_name = ' '.join(self.parsed_data[index][0][1])
            try:
                db_name = Feature.get(Feature.name == parsed_name).name
            except:
                db_name = ''
            if parsed_name != db_name:
                Feature.create(name=parsed_name)
                

    def get_tag_list(self, n_of_scenario):
        return scenarios[n_of_scenario][1][1]

    def load_tags(self):
        """
        Loads all tags in the database
        """
        for index in xrange(len(self.parsed_data)):
            parsed_name = ' '.join(self.parsed_data[index][0][1])
            try:
                db_name = Feature.get(Feature.name == parsed_name).name
            except:
                db_name = ''
            if parsed_name != db_name:
                Feature.create(name=parsed_name)


    def get_scenario(self, n_of_scenario):
        pass 