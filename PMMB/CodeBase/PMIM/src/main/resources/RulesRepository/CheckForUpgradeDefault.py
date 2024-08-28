'''
Created on 12 Mar 2018

@author: xarjsin
'''
from Model import EntityDef,EntityRef
import Utilities as Utils

class CheckForUpgrade_Rule(object):
    '''
    Rule indicating child tags should be iterated for upgrade check
    '''


    def __init__(self, params):
        '''
        Initialises something, define later
        '''
        self.ActionList = params['ActionList']
        self.Tag = params['Model']
    
    
    def prep(self):
        '''
        DO NOT IGNORE TAG - ADDITION OF ACTION COMPONENTS INDICATES NEXT LEVEL ITERATION
        '''
        greenComponent = self.ActionList.getComponent('GREEN')
        if greenComponent is None:
            greenComponent = Utils.odict()
            
        redComponent = self.ActionList.getComponent('RED')
        if greenComponent is None:
            greenComponent = Utils.odict()
            
        yellowComponent = self.ActionList.getComponent('YELLOW')
        if greenComponent is None:
            greenComponent = Utils.odict()
            
        blueComponent = self.ActionList.getComponent('BLUE')
        if greenComponent is None:
            greenComponent = Utils.odict()
            
        self.ActionList.addComponent('GREEN', greenComponent)
        self.ActionList.addComponent('RED', redComponent)
        self.ActionList.addComponent('YELLOW', yellowComponent)
        self.ActionList.addComponent('BLUE', blueComponent)
        return self.ActionList
    
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