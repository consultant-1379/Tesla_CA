'''
Created on Oct 12, 2017

@author: ebrifol
'''

from Utilities import Utils
from Model import EntityDef

class XML_Parser(object):
    '''
    This is the parent of all XML based parsers
    '''

    def __init__(self, params, parserImpl):
        self.params = params
        self.parserImpl = parserImpl
    
    def parse(self):
        if 'filepath' not in self.params:
            raise Exception('No valid file path provided')
        
        model = EntityDef('temporary')
        
        XML = Utils.fileToXMLObject(self.params['filepath'])
        XML = XML.getroot()
        model = self.parseElements(XML, model)
        
        return model
        
    def parseElements(self, xmlElement, model):
        if xmlElement.tag in self.parserImpl.Tags_To_Parse:
            model = getattr(self.parserImpl, self.parserImpl.Tags_To_Parse[xmlElement.tag])(xmlElement, model)
            for child in xmlElement:
                if child.tag in self.parserImpl.Tags_To_Parse:
                    model = getattr(self.parserImpl, self.parserImpl.Tags_To_Parse[child.tag])(child, model)
                    self.parseElements(child, model)
        else:
            for child in xmlElement:
                if child.tag in self.parserImpl.Tags_To_Parse:
                    model = getattr(self.parserImpl, self.parserImpl.Tags_To_Parse[child.tag])(child, model)
                    self.parseElements(child, model)
        
        return model
        
        
        
        
        
        