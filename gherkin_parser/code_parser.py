'''
Created on 26 de may. de 2016

@author: Juan
'''
import re
from os import walk
from os.path import join
from model.code_step import CodeStep

class CodeParser(object):
    
    
    def parseFile(self, fileName=None):
        line = 'q'
        __STEP_TAG = '@step'
        __NAME_PATTERN = '(\'|\")(.*)(\'|\")'
        __CLEAN_NAME_PATTERN = '(\"{[^}]*}\")'
        with open(fileName) as parsedfile:
            for line in parsedfile:
                line = line.strip()
                if line.lower().startswith(__STEP_TAG):
                    name = re.search(__NAME_PATTERN, line).group(2)
                    clean_name = re.sub(__CLEAN_NAME_PATTERN, '', name)
                    CodeStep.create(name=name, clean_name=clean_name, file_name=fileName)

    def parseDir(self, path=None):
        assert path is not None
        for root, dirs, files in walk(path):
            for filetoparse in files:
                self.parseFile(join(root, filetoparse))
