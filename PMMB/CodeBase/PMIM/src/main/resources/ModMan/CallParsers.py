'''
Created on 20 Feb 2018

@author: xarjsin
'''
import inspect
import sys
import Parsers


class Call_Parsers(object):
    '''
    Calls the parsers for input files
    '''
    Input = {'ECIM','XML_PMIM','TP','Unv', 'Classic_MIM', 'JSON_PMIM'}


    def __init__(self):
        '''
        Constructor
        '''
        self.parserResult = {}
    
    
    def getInputs(self):
        return self.Input
    
    
    def getDescription(self):
        return self.description
    
    
    def runBackground(self,params):
        parserName = params['InputType'] + '_Parser'
        for name, obj in inspect.getmembers(Parsers,inspect.isclass):
            if(name == parserName):
                print "Parsing " + params['InputType']
                parser = obj(params)
                description = parser.__doc__
                result = parser.parse()
                self.parserResult['Docs'] = description
                self.parserResult['Result'] = result
                return self.parserResult
            
