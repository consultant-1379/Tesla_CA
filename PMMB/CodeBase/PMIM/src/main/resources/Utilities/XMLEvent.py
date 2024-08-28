'''
Created on Feb 14, 2018

@author: ebrifol
'''

from Utilities import Utils

class XMLEventParser(object):

    def __init__(self, params, parserImpl):
        self.params = params
        self.parserImpl = parserImpl
    
    def parse(self):
        if 'filepath' not in self.params:
            raise Exception('No valid file path provided')
        
        context = Utils.fileToXMLEvents(self.params['filepath'])
        
        model = self.parseElements(context)
        
        return model
    
    def parseElements(self, context):
        flag = None
        for event, elem in context:
            method = None
            if elem.tag in self.parserImpl.Tags_To_Parse:
                try:
                    method = getattr(self.parserImpl, elem.tag + '_' + event)
                except:
                    #Suppress the exception is the method doesnt exist. Maybe no handling is required. 
                    flag = None
                
                if method is not None:
                    model, flag = method(elem)
                
            elif flag is not None:
                method = getattr(self.parserImpl, self.parserImpl.GeneralParseMethod + '_' + event)
                model, flag = method(elem, flag)
                
            elem.clear()
        
        return model
    
    
        