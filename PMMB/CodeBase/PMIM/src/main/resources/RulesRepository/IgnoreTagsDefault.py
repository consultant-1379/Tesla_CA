'''
Created on 9 Mar 2018

@author: xarjsin
'''
from Model import EntityDef,EntityRef
import Utilities as Utils

class IgnoreTags_Rule(object):
    '''
    Rule that defines behaviour if a tag is to be ignored
    '''


    def __init__(self, params):
        '''
        Initialises something, define later
        '''
        self.ActionList = params['ActionList']
        self.TagFound = params['RuleObject']
        self.TagsToIgnore = ['structRef', 'enumRef', 'Relationships']
    
    
    def prep(self):
        '''
        Ignoring the tags for which this rule is called
        '''
        Result = {}
        if self.TagFound in self.TagsToIgnore:
            print self.TagFound + " has been ignored in this implementation"
            Result['Ignore'] = True
            Result['ActionList'] = self.ActionList
        else:
            greenComponent = self.ActionList.getComponent('GREEN')
            if greenComponent is None:
                greenComponent = Utils.odict()
            
            redComponent = self.ActionList.getComponent('RED')
            if redComponent is None:
                redComponent = Utils.odict()
            
            yellowComponent = self.ActionList.getComponent('YELLOW')
            if yellowComponent is None:
                yellowComponent = Utils.odict()
            
            blueComponent = self.ActionList.getComponent('BLUE')
            if blueComponent is None:
                blueComponent = Utils.odict()
            
            self.ActionList.addComponent('GREEN', greenComponent)
            self.ActionList.addComponent('RED', redComponent)
            self.ActionList.addComponent('YELLOW', yellowComponent)
            self.ActionList.addComponent('BLUE', blueComponent)
            Result['Ignore'] = False
            Result['ActionList'] = self.ActionList
        
        return Result
    
    def execute(self):
        '''
        '''
        pass
    
    
    def validate(self):
        '''
        '''
        pass
    
    
    def test(self):
        '''
        '''
        pass
    
    