'''
Created on 26 de may. de 2016

@author: Juan
'''

from config.setup import Setup
from parser2.code_parser import CodeParser
from service.entity_service import EntityService
if __name__ == '__main__':
    Setup({'reset_db':True, 'dummy_db': False})
    str1 = 'la "{animal}" estaba "{sola}"'
    str2 = 'la "vaca" estaba "sola"'
    
    import re
    str1 = re.sub('(\"{[^}]*}\")','', str1)
    str2 = re.sub('(\"[^\"]*\")','', str2)
    print str1 == str2
    CodeParser().parseDir('C:\\Users\\Juan\\dev\\workspace\\qa_framework\\project\\features\\steps')
    print EntityService().find_code_step( 'I reboot machine "{machine_label}" and wait')