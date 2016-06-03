'''
Created on 26 de may. de 2016

@author: Juan
'''
from config.setup import Setup, db
from gherkin_parser.parser_helper import ParserHelper

from gherkin_parser.code_parser import CodeParser

from service.entity_service import EntityService

if __name__ == '__main__':

    Setup({'reset_db':True, 'dummy_db': False})
    db.begin()
    CodeParser().parseDir('C:\\Users\\Juan\\dev\\workspace\\qa_framework\\project\\features\\steps')
    ParserHelper('C:\\Users\\Juan\\dev\\workspace\\qa_framework\\project\\features')
    db.commit()
    query = EntityService().find_scenarios('')
    #for step in query:
    #    print step.id, step.name

