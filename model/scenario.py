'''
Created on 24 de may. de 2016

@author: Juan
'''
from peewee import CharField, Model, ForeignKeyField,\
    BooleanField
from playhouse.fields import ManyToManyField
from model.feature import Feature
from model.tag import Tag
from config.setup import db


class Scenario(Model):
    name = CharField()
    description = CharField(null=True)
    feature = ForeignKeyField(Feature, related_name='scenarios')
    is_background = BooleanField()
    tags = ManyToManyField(Tag, related_name='scenarios')

    class Meta:
        database = db
        db_table = 'scenario'
