'''
Created on 24 de may. de 2016

@author: Juan
'''
from parser.parser_helper import ParserHelper
from model.Tag import Tag
from model.Feature import Feature
from model.Scenario import Scenario
from peewee import SqliteDatabase
db = SqliteDatabase('gherkin.db')

if __name__ == '__main__':
    db.connect()
    db.create_tables([Feature], safe=True)
    db.create_tables([Tag], safe=True)
    db.create_tables([Scenario], safe=True)

    parser = ParserHelper("behave.example")

    #parser.load_features()
   # parser.load_tags()
    parser.load_scenarios()

    feature_query = Feature.select()
    tag_query = Tag.select()
    scenario_query = Scenario.select()

    for ft in feature_query:
        print ft.name, ft.id
    for tag in tag_query:
        print tag.name, tag.id
    for scen in tag_query:
        print scen.name, scen.id
