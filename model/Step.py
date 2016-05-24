'''
Created on 24 de may. de 2016

@author: Juan
'''
from peewee import SqliteDatabase, CharField, Model, ForeignKeyField
from model import Scenario, CodeStep


db = SqliteDatabase('gherkin.db')

class Step(Model):
    '''
    classdocs
    '''
    name = CharField()
    description = CharField()
    scenario = ForeignKeyField(Scenario, related_name='steps')
    codeStep = ForeignKeyField(CodeStep, related_name='steps')
    
    
    class Meta:
        database = db
