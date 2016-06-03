'''
Created on 24 de may. de 2016

@author: Juan
'''
from peewee import CharField, Model
from config.setup import db


class Feature(Model):
    name = CharField()
    description = CharField(null=True)

    class Meta:
        database = db
        db_table = 'feature'
