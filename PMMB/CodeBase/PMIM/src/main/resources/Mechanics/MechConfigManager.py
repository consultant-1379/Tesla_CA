'''
Created on Nov 3, 2017

@author: ebrifol
'''

import inspect
import sys
# from Actions import *
# from Difference import *

from Parsers import XML_PMIM_Parser

class MechConfigManager(object):
    
    def __init__(self, params):
        parser = XML_PMIM_Parser(params)
        self.model = parser.parse()
    
    def executeMechanism(self, moduleName, mechanismName, params):
        for name, obj in inspect.getmembers(sys.modules[moduleName]):
            if name == mechanismName and inspect.isclass(obj):
                mech = obj()
                mech.execute(params)
                   
    def setModel(self, model):
        self.model = model
    
    def getMechanicComponent(self, mechanicName):
        if mechanicName in self.model.listComponentNames():
            return self.model.getComponent(mechanicName)
        return None
    
    