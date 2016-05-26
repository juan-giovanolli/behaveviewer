'''
Created on 26 de may. de 2016

@author: Juan
'''
from model.code_step import CodeStep
import re

class CodeParser(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        #self.fileName = fileName
    
    def parseFile(self,fileName):
        line = 'q'
        with open(fileName) as fiLe:
            while line:
                line = fiLe.readline()
                if line.strip().startswith('@step'):
                    print CodeStep.create(name=re.search('\'(.*)\'', line.strip()).group(1), fileName=fileName)
                    print line
    
    def parseDir(self, path):
        