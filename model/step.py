'''
Created on 24 de may. de 2016

@author: Juan
'''
from peewee import SqliteDatabase, CharField, Model, ForeignKeyField
from model.scenario import Scenario
from model.code_step import CodeStep


db = SqliteDatabase('gherkin.db')

class Step(Model):
    '''
    classdocs
    '''
    name = CharField()
    description = CharField(null=True)
    scenario = ForeignKeyField(Scenario, related_name='steps')
    codeStep = ForeignKeyField(CodeStep, related_name='steps')
    
    
    class Meta:
        database = db
