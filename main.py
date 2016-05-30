from model.feature import Feature
from model.scenario import Scenario
from model.tag import Tag
from peewee import SqliteDatabase
from parser.parser_helper import ParserHelper
import sys
from PyQt4 import QtGui, QtCore
from config.setup import Setup
from service.entity_service import EntityService
from view.main_window import MainBehaveWindow

db = SqliteDatabase('gherkin.db')

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
    db.connect()
    db.create_tables([Feature], safe=True)
    db.create_tables([Tag], safe=True)
    db.create_tables([Scenario], safe=True)

    parser = ParserHelper("behave.example")

    parser.load_scenarios()

    feature_query = Feature.select()
    tag_query = Tag.select()
    scenario_query = Scenario.select()

    for ft in feature_query:
        print ft.name, ft.id
    for tag in tag_query:
        print tag.name, tag.id
    for scen in tag_query:
        print scen.name, scen.id
    main()