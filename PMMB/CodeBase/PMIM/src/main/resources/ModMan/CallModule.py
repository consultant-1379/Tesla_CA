'''
Created on 20 Feb 2018

@author: xarjsin
'''
import inspect
import sys
import ModMan

class CallModule(object):
    '''
    Class which will call the PMIM modules in the background
    '''

    def __init__(self, params):
        '''
        Initialises something
        '''
        self.params = params
                
        
    def callModule(self):
        validArg = False
        for name, obj in inspect.getmembers(sys.modules[ModMan.__name__],inspect.isclass):
            if (name != self.__class__.__name__):
                call = obj()
                if self.params['InputType'] in call.getInputs():
                    validArg = True
                    return call.runBackground(self.params)
                    
        if not validArg:
            print "Incorrect input specified - " + self.params['InputType']
            
            