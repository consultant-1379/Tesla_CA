'''
Created on 20 Feb 2018

@author: xarjsin
'''

import inspect
import Mechanics

class Call_Engine(object):
    '''
    Calls the methods to run rules on the input model
    '''
    Input = {'TPRules'}

    def __init__(self):
        '''
        Initialises something
        '''
        pass
    
    
    def getInputs(self):
        return self.Input
    
    def runBackground(self,params):
        engineName = params['InputType'] + '_Engine'
        for name, obj in inspect.getmembers(Mechanics,inspect.isclass):
            if(name == engineName):
                print "Calling " + params['InputType'] + " Engine"
                rules = obj(params)
                result = rules.runRules()
                return result