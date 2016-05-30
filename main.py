'''
Created on 24 de may. de 2016

@author: Juan
'''
import sys
from PyQt4 import QtGui, QtCore
from config.setup import Setup
from service.entity_service import EntityService
from view.main_window import MainBehaveWindow



def test():
    db.connect()
    ScenarioTagsTable = Scenario.tags.get_through_model()
    db.create_tables([Tag, code_step, Feature, Scenario, Step, ScenarioTagsTable], safe=True)
    
    newFeature = Feature.create(name='Feature1')   
    newFeature = Feature.create(name='blaCONsultasdvsdv')
    newFeature = Feature.create(name='Feature2')
    newFeature = Feature.create(name='Feature3')
    newFeature = Feature.create(name='consultablabla') 
    
    query = EntityService().find_features('')

    for result in query:
        print result.count


def main():
    Setup({'reset_db':True, 'dummy_db':True})
    query = EntityService().find_scenarios('')

    app = QtGui.QApplication(sys.argv)
    ex = MainBehaveWindow(EntityService())
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()