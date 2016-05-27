from model.Feature import Feature
from model.Tag import Tag
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
        if self.parsed_data[0][0][0].lower() == 'feature:': # TODO make this unnecessary
            parsed_name = ' '.join(self.parsed_data[0][0][1])
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
            list_of_tags =  self.parsed_data[index][1][1]
            if self.parsed_data[index][1][0].lower() == 'tag': # TODO make this unnecessary
                for parsed_name in list_of_tags:
                    try:
                        db_name = Tag.get(Tag.name == parsed_name).name
                    except:
                        db_name = ''
                    if parsed_name != db_name:
                        Tag.create(name=parsed_name, description='')


    def get_scenario(self, n_of_scenario):
        pass


    def load_scenarios(self):
        """
        Loads all scenarios in the database
        """
        tags = []
        feature = Feature()
        print self.parsed_data
        for n_of_scenario in xrange(len(self.parsed_data)):
            for component in xrange(len(self.parsed_data[n_of_scenario])):
                if self.parsed_data[n_of_scenario][0][0].lower() == 'feature:':
                    parsed_name = ' '.join(self.parsed_data[0][0][1])
                    try:
                        db_name = Feature.get(Feature.name == parsed_name).name
                    except:
                        db_name = ''
                    if parsed_name != db_name:
                        Feature.create(name=parsed_name)
                if self.parsed_data[n_of_scenario][0][0].lower() == 'tag:':
                    list_of_tags = self.parsed_data[n_of_scenario][0][1]
                    for parsed_name in list_of_tags:
                        try:
                            db_name = Tag.get(Tag.name == parsed_name).name
                        except:
                            db_name = ''
                        if parsed_name != db_name:
                            tags.append(Tag.create(name=parsed_name, description=''))
                if self.parsed_data[n_of_scenario][0][0].lower() == 'scenario:':
                    parsed_name = ' '.join(self.parsed_data[n_of_scenario][0][1])
                    try:
                        db_name = Scenario.get(Scenario.name == parsed_name).name
                    except:
                        db_name = ''
                    if parsed_name != db_name:
                        Scenario.create(name=parsed_name, description='', Feature.get(Feature.name == parsed_name))




    name = CharField()
    description = CharField()
    feature = ForeignKeyField(Feature, related_name='scenarios')
    tags = ManyToManyField(Tag, related_name='scenarios')