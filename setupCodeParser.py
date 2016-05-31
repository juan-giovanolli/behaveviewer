'''
Created on 26 de may. de 2016

@author: Juan
'''
from parser.parser_helper import ParserHelper
from config.setup import Setup
from parser.code_parser import CodeParser
from service.entity_service import EntityService
from os import walk
from os.path import isfile, join, basename
if __name__ == '__main__':
    Setup({'reset_db':True, 'dummy_db': False})

    CodeParser().parseDir('/home/federico/Desktop/Harriague/230_auto/qa_framework/project/features/steps')

    ParserHelper('/home/federico/Desktop/Harriague/230_auto/qa_framework/project/features')
    
    query = EntityService().find_most_used_steps(10)
    for step in query:
        print step.count