'''
Created on 24 de may. de 2016

@author: Juan
'''
from model.tag import Tag
from peewee import SqliteDatabase
from model import scenario.Scenario
from model import feature.Feature
from model.Step import Step
from model import code_step.CodeStep
from service.EntityService import EntityService
db = SqliteDatabase('gherkin.db')

if __name__ == '__main__':
    db.connect()
    ScenarioTagsTable = Scenario.tags.get_through_model()
    db.create_tables([Tag, code_step, Feature, Scenario, Step, ScenarioTagsTable], safe=True)
    ##newTag = Tag.create(name='Juan', description='Giovanolli')
    ##query = Tag.select().where(Tag.name == 'Juan')
    ##for tag in query:
    ##    print tag.name, tag.id
    newFeature = Feature.create(name='Feature1')   
    newFeature = Feature.create(name='blaCONsultasdvsdv')
    newFeature = Feature.create(name='Feature2')
    newFeature = Feature.create(name='Feature3')
    newFeature = Feature.create(name='consultablabla') 
    #newTag = Tag.create(name='FVT')
    #newScenario = Scenario.create(name='Scenario1', feature=newFeature,is_background=True)
    #newScenario.tags.add(newTag)
    #newCodeStep1 = code_step.create(name='CodeStep1')
    #newStep1 = Step.create(name='Step1', scenario=newScenario, codeStep=newCodeStep1)
    #newStep2 = Step.create(name='Step2', scenario=newScenario, codeStep=newCodeStep1)
    #newStep3 = Step.create(name='Step3', scenario=newScenario, codeStep=newCodeStep1)

    #newCodeStep2 = code_step.create(name='CodeStep2')
    #newStep4 = Step.create(name='Step4', scenario=newScenario, codeStep=newCodeStep2)
    #newStep5 = Step.create(name='Step5', scenario=newScenario, codeStep=newCodeStep2)


    #newCodeStep3 = code_step.create(name='CodeStep3')
    #newStep6 = Step.create(name='Step6', scenario=newScenario, codeStep=newCodeStep3)
    
    query = EntityService().find_features('')

    for result in query:
        print result.name
