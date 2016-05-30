'''
Created on 24 de may. de 2016

@author: Juan
'''
from peewee import SqliteDatabase, CharField, Model


db = SqliteDatabase('gherkin.db')

class CodeStep(Model):
    '''
    classdocs
    '''
    name = CharField()
    description = CharField(null=True)
    file_name = CharField(null=True)
    
    class Meta:
        database = db
