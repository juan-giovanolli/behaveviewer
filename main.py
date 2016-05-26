'''
Created on 24 de may. de 2016

@author: Juan
'''
from model.Tag import Tag
from peewee import SqliteDatabase
from model.Scenario import Scenario
from model.Feature import Feature
from model.Step import Step
from model.CodeStep import CodeStep
from service.EntityService import EntityService
db = SqliteDatabase('gherkin.db')

if __name__ == '__main__':
    db.connect()
    db.create_tables([Tag, CodeStep, Feature, Scenario, Step], safe=True)
    ##newTag = Tag.create(name='Juan', description='Giovanolli')
    ##query = Tag.select().where(Tag.name == 'Juan')
    ##for tag in query:
    ##    print tag.name, tag.id
    newFeature = Feature.create(name='Feature1')    
    newTag = Tag.create(name='FVT')
    newScenario = Scenario.create(name='Scenario1', feature=newFeature)
    newCodeStep1 = CodeStep.create(name='CodeStep1')
    newStep1 = Step.create(name='Step1', scenario=newScenario, codeStep=newCodeStep1)
    newStep2 = Step.create(name='Step2', scenario=newScenario, codeStep=newCodeStep1)
    newStep3 = Step.create(name='Step3', scenario=newScenario, codeStep=newCodeStep1)

    newCodeStep2 = CodeStep.create(name='CodeStep2')
    newStep4 = Step.create(name='Step4', scenario=newScenario, codeStep=newCodeStep2)
    newStep5 = Step.create(name='Step5', scenario=newScenario, codeStep=newCodeStep2)


    newCodeStep3 = CodeStep.create(name='CodeStep3')
    newStep6 = Step.create(name='Step6', scenario=newScenario, codeStep=newCodeStep3)
    
    query = EntityService().find_most_used_steps(4)

    for result in query:
        print result.count
