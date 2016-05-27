'''
Created on 24 de may. de 2016

@author: Juan
'''
from config.setup import Setup
from service.entity_service import EntityService

if __name__ == '__main__':
    Setup({'reset_db':True, 'dummy_db':True})
    query = EntityService().find_most_used_steps(10)
    print query
    for result in query:
        ##for step in result.steps:
            print result.count