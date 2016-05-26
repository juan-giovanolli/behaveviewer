'''
Created on 26 de may. de 2016

@author: Juan
'''
from peewee import SqliteDatabase
from model.scenario import Scenario
from model.tag import Tag
from model.code_step import CodeStep
from model.feature import Feature
from model.step import Step



class Setup(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        self.reset_db()
    
    def reset_db(self):
        db = SqliteDatabase('gherkin.db')
        db.connect()
        ScenarioTagsTable = Scenario.tags.get_through_model()
        db.drop_tables([Tag, CodeStep, Feature, Scenario, Step, ScenarioTagsTable], safe=True)
        db.create_tables([Tag, CodeStep, Feature, Scenario, Step, ScenarioTagsTable], safe=True)