'''
Created on 24 de may. de 2016

@author: Juan
'''
from model.Tag import Tag
from peewee import SqliteDatabase
db = SqliteDatabase('gherkin.db')

if __name__ == '__main__':
    db.connect()
    db.create_tables([Tag], safe=True)
    newTag = Tag.create(name='Juan', description='Giovanolli')
    query = Tag.select().where(Tag.name == 'Juan')
    for tag in query:
        print tag.name, tag.id
