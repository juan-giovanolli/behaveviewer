'''
Created on 24 de may. de 2016

@author: Juan
'''
from model import Scenario, Feature
from model.CodeStep import CodeStep
from model.Step import Step
from peewee import fn

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
    