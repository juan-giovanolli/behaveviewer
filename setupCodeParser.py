'''
Created on 26 de may. de 2016

@author: Juan
'''
from parser2.parser_helper import ParserHelper
from config.setup import Setup
from parser2.code_parser import CodeParser
from service.entity_service import EntityService
from os import walk
from os.path import isfile, join, basename
if __name__ == '__main__':
    Setup({'reset_db':True, 'dummy_db': False})
    str1 = 'la "{animal}" estaba "{sola}"'
    str2 = 'la "vaca" estaba "sola"'
    
    import re
    str1 = re.sub('(\"{[^}]*}\")','', str1)
    str2 = re.sub('(\"[^\"]*\")','', str2)
    print str1 == str2
    CodeParser().parseDir('C:\\Users\\Juan\\dev\\workspace\\qa_framework\\project\\features\\steps')

    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in walk('C:\\Users\\Juan\\dev\\workspace\\qa_framework\\project\\features'):
        path = root.split('/')
        ##print root
        for file in files:
            print join(root, file)
            ##self.parseFile(join(root, file))
            if file.endswith('.feature') and file not in('ipe_epo_remotecmd.feature'):
                parser = ParserHelper(join(root, file))
                parser.load_scenarios()
    query = EntityService().find_most_used_steps(10)
    for step in query:
        print step.count