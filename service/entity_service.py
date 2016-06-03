'''
Created on 24 de may. de 2016

@author: Juan
'''

from peewee import fn
import re
from model.scenario import Scenario
from model.feature import Feature
from model.code_step import CodeStep
from model.step import Step
from model.tag import Tag


class EntityService(object):

    _ANY_STRING = '%'
    
    def find_steps_per_feature(self, feature_id):
        return Step.select().join(Scenario).join(Feature).where(Feature.id == feature_id)

    def find_features_per_step(self, step_id):
        return Feature.select().join(Scenario).join(Step).where(Step.id == step_id)

    def find_most_used_steps(self, limit):
        return Step.select(Step, fn.Count(Step.id).alias('count'))\
            .join(CodeStep)\
            .group_by(CodeStep)\
            .limit(limit)\
            .order_by(fn.Count(Step.id).desc())

    def find_features(self, expression):
        return Feature.select().where(Feature.name ** (self._ANY_STRING + expression + self._ANY_STRING))

    def find_scenarios(self, expression, is_background=False):
        return Scenario.select().where(Scenario.name ** (self._ANY_STRING + expression + self._ANY_STRING), Scenario.is_background == is_background)

    def find_steps(self, expression, tag_id=None):
        ScenarioTagsTable = Scenario.tags.get_through_model()
        query = Step.select(Step)\
            .join(Scenario)
        if tag_id is not None:
            query = query.join(ScenarioTagsTable).join(Tag).where(Step.name ** (self._ANY_STRING + str(expression) + self._ANY_STRING), Tag.id == tag_id)
        else:
            query = query.where(Step.name ** (self._ANY_STRING + str(expression) + self._ANY_STRING))
        return query

    def find_code_step(self, step):
        __MATCH_PATTERN = '(\"[^\"]*\")'
        clean_step_name = re.sub(__MATCH_PATTERN, '', step)
        try:
            return CodeStep.get(CodeStep.clean_name == clean_step_name)
        except CodeStep.DoesNotExist:
            return None
