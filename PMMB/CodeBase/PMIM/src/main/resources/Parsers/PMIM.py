'''
Created on Oct 12, 2017

@author: ebrifol
'''

from Utilities.XML import XML_Parser
from Model import EntityDef, EntityRef
import Utilities as Utils


class XML_PMIM_Parser(XML_Parser):
    '''
    This parser should be used to parse PMIM model files
    '''
    
    Tags_To_Parse = {'EntityDef' : 'parse_entity'}


    def __init__(self, params):
        super(self.__class__, self).__init__(params, self)
        self.params = params
        
    def parse_entity(self, xmlElement, model):    
        model.setName(xmlElement.get('name'))
        
        for child in xmlElement:
            if child.tag == 'Components':
                section = child.get('section')
                components = Utils.odict()
                for innerchild in child:
                    if innerchild.tag == 'EntityDef':
                        component = EntityDef(innerchild.get('name'))
                        component = self.parse_entity(innerchild, component)
                        components[component.getName()] = component
                    else:
                        component = EntityRef(innerchild.get('name'))
                        component.setSource(innerchild.get('sourceName'), innerchild.get('sourceType'))
                        component.setEntity(innerchild.get('entityName') , innerchild.get('entityType'))
                        components[component.getName()] = component
                        
                model.addComponent(section, components)
            else:
                model.addProperty(child.tag, child.text)
        
        return model

        
        
        
        
        