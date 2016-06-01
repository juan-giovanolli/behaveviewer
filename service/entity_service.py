'''
Created on 24 de may. de 2016

@author: Juan
'''
from model.scenario import Scenario
from model.feature import Feature
from model.code_step import CodeStep
from model.step import Step
from peewee import fn
from model.tag import Tag
ScenarioTagsTable = Scenario.tags.get_through_model()

class EntityService(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

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
        return Feature.select().where(Feature.name ** ('%' + expression + '%'))

    def find_scenarios(self, expression):
        return Scenario.select().where(Scenario.name ** ('%' + expression + '%'))

    def find_steps(self, expression, tag_id=None):
        query = Step.select(Step, ScenarioTagsTable)\
            .join(Scenario)\
            .join(ScenarioTagsTable)\
            .where(Step.name ** ('%' + str(expression) + '%'), ScenarioTagsTable.tag_id == tag_id)
        print query
        return query

    def find_code_step(self, step):
        import re
        clean_step_name = re.sub('(\"[^\"]*\")', '', step)
        try:
            return CodeStep.get(CodeStep.clean_name == clean_step_name)
        except:
            return None
