'''
Created on 24 de may. de 2016

@author: Juan
'''
from parser.parser_helper import ParserHelper
from model.Tag import Tag
from model.Feature import Feature
from peewee import SqliteDatabase
db = SqliteDatabase('gherkin.db')

if __name__ == '__main__':
    db.connect()
    db.create_tables([Tag], safe=True)
    db.create_tables([Feature], safe=True)

    parser = ParserHelper("behave.example")
    newTag = Tag.create(name='Juan', description='Giovanolli')
    newFeature = parser.get_feature(0)
    #newFeature.save()
    parser.load_features()
    query = Feature.select()
    print query
    for ft in query:
        print ft.name, ft.id
