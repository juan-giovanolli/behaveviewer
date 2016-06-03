from os import walk
from os.path import isfile, join
from model.feature import Feature
from model.scenario import Scenario
from model.tag import Tag
from model.step import Step
from gherkin_parser import Parser
from service.entity_service import EntityService
import parser_constants


class ParserHelper:
    """
    This class makes use of the parser in order to create each model
    retrieving information from the file parsed
    """

    def __init__(self, filename=None):
        assert filename is not None, "filename not a string"
        if not isfile(filename):
            for root, dirs, files in walk(filename):
                self._parse_file(root, files)
        else:
            print "Parsing file: " + filename
            self._entity_service = EntityService()
            self._current_file = filename
            self._tags = []
            self._parsed_data = Parser().parse_file(filename)
            self._feature = ''
            self._tags_cache = {}
            self._fill_cache_with_existing_tags()

    def _parse_file(self, root=None, files=None):
        assert root is not None
        assert files is not None
        for file in files:
            print join(root, file)
            if file.endswith(parser_constants.FEATURE_EXTENSION):
                parser = ParserHelper(join(root, file))
                parser.load_scenarios()

    def _fill_cache_with_existing_tags(self):
        tag = Tag()
        tags = tag.select()
        for tg in tags:
            self._tags_cache[tg.name] = tg

    def _load_feature_with_background(self):
        feature_and_background = self._parsed_data[1]
        feature = feature_and_background[0]
        feature_name = ' '.join(feature[1])
        self._feature = feature_name  # Used to create scenarios
        db_feature = None
        try:
            Feature.get(Feature.name == feature_name)  # This statement will throw an exception if feature is not in the db
            db_feature = Feature(name=feature_name + " - (Duplicated)")
            db_feature.save()
        except Feature.DoesNotExist:
            print "Adding new feature to database..."
            db_feature = Feature.create(name=feature_name)
        if len(feature_and_background) > 1:  # Has background
            background = feature_and_background[1]
            scenario = self._create_scenario(parser_constants.BACKGROUND, True, [], db_feature)
            for step in background[1]:
                self._create_step(' '.join(step[1]), scenario, step[0])
        return db_feature

    def _create_tags(self, scenario=None):
        """
        Reads parsed tags and add each in the database if it dowsn't exists
        """
        assert scenario is not None
        tags = []
        for elem in scenario:
            if elem[0] == 'tag':
                for tag in elem[1]:
                    tags.append(self._crete_new_tag(tag))
        return tags

    def _crete_new_tag(self, tag=None):
        assert tag is not None
        if tag not in self._tags_cache:
            new_tag = Tag.create(name=tag, description='')
            self._tags_cache[tag] = new_tag
        else:
            new_tag = self._tags_cache[tag]
        return new_tag

    def _create_scenario(self, name=None, is_background=None, tags=None, feature=None):
        assert name is not None
        assert is_background is not None
        assert tags is not None
        assert feature is not None
        scenario = Scenario.create(name=name, is_background=is_background, feature=feature)
        scenario.tags.add(tags)
        scenario.save()
        return scenario

    def _create_step(self, name=None, scenario=None, step_type=None):
        assert name is not None
        assert scenario is not None
        assert step_type is not None
        codeStep = self._entity_service.find_code_step(name)
        Step.create(name=name, scenario=scenario, code_step=codeStep, step_type=step_type)

    def load_scenarios(self):
        """
        Loads all scenarios in the database
        """
        feature = self._load_feature_with_background()
        list_of_scenarios = self._parsed_data[0]
        for scen in list_of_scenarios:
            scenario_name = ' '.join(scen[0][1]) if scen[0][0] == parser_constants.SCENARIO_MARK else ' '.join(scen[1][1])
            tags = self._create_tags(scen)
            scenario = self._create_scenario(name=scenario_name, is_background=False, tags=tags, feature=feature)
            steps = scen[2:]
            for step in steps:
                step_type = step[0]
                step_name = ' '.join(step[1])
                self._create_step(step_name, scenario, step_type)
