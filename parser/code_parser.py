'''
Created on 26 de may. de 2016

@author: Juan
'''
from model.code_step import CodeStep
import re
from os import walk
from os.path import isfile, join, basename

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
                if line.strip().startswith('@step') or line.strip().startswith('@Step'):
                    
                    print re.search('(\'|\")(.*)(\'|\")', line.strip()).group(2)
                    name = re.search('(\'|\")(.*)(\'|\")', line.strip()).group(2)
                    clean_name = re.sub('(\"{[^}]*}\")','', name)
                    print clean_name
                    print CodeStep.create(name=name, clean_name=clean_name, file_name=fileName)
                    
    
    def parseDir(self, path):

        # traverse root directory, and list directories as dirs and files as files
        for root, dirs, files in walk(path):
            path = root.split('/')
            ##print root
            for file in files:
                print join(root, file)
                self.parseFile(join(root, file))
                
    