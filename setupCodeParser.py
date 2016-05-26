'''
Created on 26 de may. de 2016

@author: Juan
'''
from parser_service.code_parser import CodeParser 
from config.setup import Setup

if __name__ == '__main__':
    Setup({'reset_db':True, 'dummy_db': False})
    CodeParser().parseFile('C:\\Users\\Juan\\dev\\workspace\\qa_framework\\project\\features\\steps\\common\\auto_agent.py')