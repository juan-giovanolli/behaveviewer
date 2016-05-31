'''
Created on 26 de may. de 2016

@author: Juan
'''

from peewee import SqliteDatabase
db = SqliteDatabase(':memory:')
from model.scenario import Scenario
from model.tag import Tag
from model.code_step import CodeStep
from model.feature import Feature
from model.step import Step



class Setup(object):
    '''
    classdocs
    '''
    
    def __init__(self, params):
        if isinstance(params, dict):
            if params['reset_db'] != False:
                print 'Running setup'
                self.reset_db()
            if params['dummy_db'] != False:
                print 'Creating dummy database'
                self.populate_db()
        
    def reset_db(self):
        
        db.connect()
        ScenarioTagsTable = Scenario.tags.get_through_model()
        db.drop_tables([Tag, CodeStep, Feature, Scenario, Step, ScenarioTagsTable], safe=True)
        db.create_tables([Tag, CodeStep, Feature, Scenario, Step, ScenarioTagsTable], safe=True)
    
    def populate_db(self):
        tag1 = Tag.create(name='tag1', description='')
        tag2 = Tag.create(name='tag2', description='')
        
        codeStep1 = CodeStep.create(name='CodeStep1')
        codeStep2 = CodeStep.create(name='CodeStep2')
        codeStep3 = CodeStep.create(name='CodeStep3')
        codeStep4 = CodeStep.create(name='CodeStep4')
        codeStep5 = CodeStep.create(name='CodeStep5')
        codeStep6 = CodeStep.create(name='CodeStep6')
        codeStep7 = CodeStep.create(name='CodeStep7')
        codeStep8 = CodeStep.create(name='CodeStep8')
        
        feature1 = Feature.create(name='Feature1')
        feature2 = Feature.create(name='Feature2')
        
        scenario1 = Scenario.create(name='Scenario1', feature=feature1, is_background=True)
        scenario1.tags.add(tag1)
        scenario1.save()
        
        step11 = Step.create(name='Step1', scenario=scenario1, codeStep=codeStep1)
        step12 = Step.create(name='Step2', scenario=scenario1, codeStep=codeStep2)
        
        scenario2 = Scenario.create(name='Scenario2', feature=feature1, is_background=True)
        scenario2.tags.add(tag2)   
        scenario2.save()     

        
        step21 = Step.create(name='Step3', scenario=scenario2, codeStep=codeStep3)
        step22 = Step.create(name='Step4', scenario=scenario2, codeStep=codeStep4)

        scenario3 = Scenario.create(name='Scenario3', feature=feature2, is_background=True)
        scenario3.tags.add(tag1)
        scenario3.save()
        
        step31 = Step.create(name='Step5', scenario=scenario3, codeStep=codeStep5)
        step32 = Step.create(name='Step6', scenario=scenario3, codeStep=codeStep6)
        
        scenario4 = Scenario.create(name='Scenario4', feature=feature2, is_background=True)
        scenario4.tags.add(tag2)   
        scenario4.save()    
        
        step41 = Step.create(name='Step7', scenario=scenario4, codeStep=codeStep7)
        step42 = Step.create(name='Step8', scenario=scenario4, codeStep=codeStep8)        
