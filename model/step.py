'''
Created on 24 de may. de 2016

@author: Juan
'''
from peewee import CharField, Model, ForeignKeyField
from model.scenario import Scenario
from model.code_step import CodeStep
from config.setup import db


class Step(Model):
    name = CharField()
    description = CharField(null=True)
    step_type = CharField()
    scenario = ForeignKeyField(Scenario, related_name='steps')
    code_step = ForeignKeyField(CodeStep, related_name='steps', null=True)

    class Meta:
        database = db
        db_table = 'step'