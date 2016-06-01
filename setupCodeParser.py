'''
Created on 26 de may. de 2016

@author: Juan
'''
from config.setup import Setup,db
from parser2.parser_helper import ParserHelper

from parser2.code_parser import CodeParser
from service.entity_service import EntityService
from os import walk
from os.path import isfile, join, basename
if __name__ == '__main__':
    Setup({'reset_db':True, 'dummy_db': False})
    db.begin()
    CodeParser().parseDir('C:\\Users\\Juan\\dev\\workspace\\qa_framework\\project\\features\\steps')

    ParserHelper('C:\\Users\\Juan\\dev\\workspace\\qa_framework\\project\\features')
    db.commit()
    query = EntityService().find_steps('',1)
   # for step in query:
      #  print step.name
