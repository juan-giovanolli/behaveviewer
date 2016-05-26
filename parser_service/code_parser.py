'''
Created on 26 de may. de 2016

@author: Juan
'''

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
                #print line
                if line.strip().startswith('@step'):
                    print line
