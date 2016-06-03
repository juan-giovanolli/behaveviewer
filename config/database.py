'''
Created on 2 de jun. de 2016

@author: Juan
'''

from peewee import SqliteDatabase

db = SqliteDatabase('gherkin.db')
db.set_autocommit(False)