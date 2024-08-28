'''
Created on Feb 15, 2018

@author: ebrifol
'''

import json
from Model import EntityDef, EntityRef

class JSON_PMIM_Parser(object):

    def __init__(self, params):
        self.params = params
    
    def parse(self):
        if 'filepath' not in self.params:
            raise Exception('No valid file path provided')
        
        data = json.load(open(self.params['filepath']))
        
        
        model = EntityDef(data['name'])
        model = self.parseJSONDicts(data, model)
        
        return model
                
        
    def parseJSONDicts(self, data, model):
        for key, value in data['properties'].iteritems():
            model.addProperty(key, value)
        
        for key, value in data['components'].iteritems():
            collection = {}
            for innerkey, innervalue in data['components'][key].iteritems():
                if innerkey.startswith('EntityRef_'):
                    child = EntityRef(data['components'][key][innerkey]['name'])
                    child.setSourceName(data['components'][key][innerkey]['sourceName'])
                    child.setSourceType(data['components'][key][innerkey]['sourceType'])
                    child.setEntityName(data['components'][key][innerkey]['entityName'])
                    child.setEntityType(data['components'][key][innerkey]['entityType'])
                else:
                    child = EntityDef(data['components'][key][innerkey]['name'])
                    child = self.parseJSONDicts(innervalue, child)
                collection[innerkey] = child
            model.addComponent(key, collection)
        
        return model