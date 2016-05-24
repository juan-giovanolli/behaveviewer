'''
Created on 24 de may. de 2016

@author: Juan
'''
from peewee import SqliteDatabase, CharField, Model, ForeignKeyField
from Feature import Feature
from Tag import Tag
from playhouse.fields import ManyToManyField


db = SqliteDatabase('gherkin.db')

class Scenario(Model):
    '''
    classdocs
    '''
    name = CharField()
    description = CharField(null=True)
    feature = ForeignKeyField(Feature, related_name='scenarios')
    ##tags = ManyToManyField(Tag, related_name='scenarios')
    
    class Meta:
        database = db
