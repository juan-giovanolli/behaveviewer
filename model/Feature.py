'''
Created on 24 de may. de 2016

@author: Juan
'''
from peewee import SqliteDatabase, CharField, Model


db = SqliteDatabase('gherkin.db')

class Feature(Model):
    '''
    classdocs
    '''
    name = CharField()
    description = CharField()
    
    class Meta:
        database = db
