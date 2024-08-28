'''
Created on 13 Oct 2017

@author: xshubor
'''

from Utilities.XML import XML_Parser
from Model import EntityDef

class Unv_Parser(XML_Parser):
    '''
    This parser should be used to parse Tech pack universe inputs
    '''
    
    Tags_To_Parse = {'BO' : 'parse_bo'}    
    
    def __init__(self, params):
        super(self.__class__, self).__init__(params, self)
        self.params = params
    
    def parse_bo(self, xmlElement, model):
        bo = model.getComponent('BO')
        if bo is None:
            bo = {}
         
        tpName = 'BO'
        bo_entity = EntityDef(tpName)
         
        searchTags = ['Universes']
        for child in xmlElement:
            if child.tag in searchTags:
                bo_entity = self.parse_universes(child, bo_entity)
                 
        bo[tpName] = bo_entity
        model.addComponent('BO', bo)
         
        return model
    
    def parse_universes(self, xmlElement, model):
        unvModel = model.getComponent('Universes')
        if unvModel is None:
            unvModel = {}
         
        unvName = 'Universes'
        unv_entity = EntityDef(unvName)
         
        searchTags = ['Universe']
        for child in xmlElement:
            if child.tag in searchTags:
                unv_entity = self.parse_universe(child, unv_entity)
                 
        unvModel[unvName] = unv_entity
        model.addComponent('Universes', unvModel)
         
        return model
    
    def parse_universe(self, xmlElement, model):
        universe = model.getComponent('Universe')
        if universe is None:
            universe = {}
        
        unvName = xmlElement.get('name')
        unv_entity = EntityDef(unvName)
        unv_entity.addProperty('name', xmlElement.get('name'))
        
        searchTags = ['UniverseExtensions' ,'UniverseTables', 'UniverseClasses', 'UniverseJoins']
        for child in xmlElement:
            if child.tag in searchTags:
                if child.tag == 'UniverseExtensions':
                    unv_entity = self.parse_unvextension(child, unv_entity)
                elif child.tag == 'UniverseTables':
                    unv_entity = self.parse_unvtables(child, unv_entity)
                elif child.tag == 'UniverseClasses':
                    unv_entity = self.parse_unvclasses(child, unv_entity)
                elif child.tag == 'UniverseJoins':
                    unv_entity = self.parse_unvjoins(child, unv_entity)
                    
        universe[unvName] = unv_entity
        model.addComponent('Universe', universe)
        
        return model
    
    
    def parse_unvextension(self, xmlElement, model):
        
        return model
    
    def parse_unvtables(self, xmlElement, model):
        unvtables = model.getComponent('UniverseTables')
        if unvtables is None:
            unvtables = {}
        
        unvName = 'universeTables'
        unvtables_entity = EntityDef(unvName)
        
        searchTags = ['UniverseTable']
        for child in xmlElement:
            if child.tag in searchTags:
                if child.tag == 'UniverseTable':
                    unvtables_entity = self.parse_unvtable(child, unvtables_entity)
                    
        unvtables[unvName] = unvtables_entity
        model.addComponent('UniverseTables', unvtables)
        
        return model
    
    def parse_unvtable(self, xmlElement, model):
        unvtable = model.getComponent('UniverseTable')
        if unvtable is None:
            unvtable = {}
        
        dName = xmlElement.get('name')
        unvtable_entity = EntityDef(dName)
        unvtable_entity.addProperty('name', xmlElement.get('name'))
        unvtable_entity.addProperty('extension', xmlElement.get('extension'))
        
        searchTags = ['ORDERNRO' ,'OWNER', 'ALIAS']
        for child in xmlElement:
            if child.tag in searchTags:
                strValue = xmlElement.find(child.tag).text
                if strValue is not None:
                    unvtable_entity.addProperty(child.tag, strValue.strip())
                    
        unvtable[dName] = unvtable_entity
        model.addComponent('UniverseTable', unvtable)
        
        return model
   
    def parse_unvclasses(self, xmlElement, model):
        unvclasses = model.getComponent('UniverseClasses')
        if unvclasses is None:
            unvclasses = {}
        
        unvName = 'universeClasses'
        unvclasses_entity = EntityDef(unvName)
        
        searchTags = ['UniverseClass']
        for child in xmlElement:
            if child.tag in searchTags:
                if child.tag == 'UniverseClass':
                    unvclasses_entity = self.parse_unvclass(child, unvclasses_entity)
                    
        unvclasses[unvName] = unvclasses_entity
        model.addComponent('UniverseClasses', unvclasses)
        
        return model
    
    def parse_unvclass(self, xmlElement, model):
        unvclass = model.getComponent('UniverseClass')
        if unvclass is None:
            unvclass = {}
        
        dName = xmlElement.get('name')
        unvclass_entity = EntityDef(dName)
        unvclass_entity.addProperty('name', xmlElement.get('name'))
        unvclass_entity.addProperty('extension', xmlElement.get('extension'))
        
        searchTags = ['ORDERNRO' ,'DESCRIPTION', 'PARENT', 'UniverseObjects', 'UniverseConditions']
        for child in xmlElement:
            if child.tag in searchTags:
                if child.tag == 'UniverseObjects':
                    unvclass_entity = self.parse_unvobjects(child, unvclass_entity)
                elif child.tag == 'UniverseConditions':
                    unvclass_entity = self.parse_unvconditions(child, unvclass_entity)
                else:
                    strValue = xmlElement.find(child.tag).text
                    if strValue is not None:
                        unvclass_entity.addProperty(child.tag, strValue.strip())
                    
        unvclass[dName] = unvclass_entity
        model.addComponent('UniverseClass', unvclass)
        
        return model
       
    def parse_unvobjects(self, xmlElement, model):
        unvobjects = model.getComponent('UniverseObjects')
        if unvobjects is None:
            unvobjects = {}
        
        unvName = 'universeObjects'
        unvobjects_entity = EntityDef(unvName)
        
        searchTags = ['UniverseObject']
        for child in xmlElement:
            if child.tag in searchTags:
                if child.tag == 'UniverseObject':
                    unvobjects_entity = self.parse_unvobject(child, unvobjects_entity)
                    
        unvobjects[unvName] = unvobjects_entity
        model.addComponent('UniverseObjects', unvobjects)
        
        return model
    
    def parse_unvconditions(self, xmlElement, model):
        unvconditions = model.getComponent('UniverseConditions')
        if unvconditions is None:
            unvconditions = {}
        
        unvName = 'universeConditions'
        unvcond_entity = EntityDef(unvName)
        
        searchTags = ['UniverseCondition']
        for child in xmlElement:
            if child.tag in searchTags:
                if child.tag == 'UniverseCondition':
                    unvcond_entity = self.parse_unvcondition(child, unvcond_entity)
                    
        unvconditions[unvName] = unvcond_entity
        model.addComponent('UniverseConditions', unvconditions)
        
        return model
    
    def parse_unvobject(self, xmlElement, model):
        unvobject = model.getComponent('UniverseObject')
        if unvobject is None:
            unvobject = {}
        
        dName = xmlElement.get('name')
        unvobject_entity = EntityDef(dName)
        unvobject_entity.addProperty('name', xmlElement.get('name'))
        unvobject_entity.addProperty('class', xmlElement.get('class'))
        unvobject_entity.addProperty('extension', xmlElement.get('extension'))
        
        searchTags = ['ORDERNRO' ,'DESCRIPTION', 'OBJECTTYPE', 'OBJWHERE', 'QUALIFICATION', 
                      'PROMPTHIERARCHY', 'OBJSELECT', 'AGGREGATION']
        for child in xmlElement:
            if child.tag in searchTags:  
                strValue = xmlElement.find(child.tag).text
                if strValue is not None:
                    unvobject_entity.addProperty(child.tag, strValue.strip())
                    
        unvobject[dName] = unvobject_entity
        model.addComponent('UniverseObject', unvobject)
        
        return model
    
    def parse_unvcondition(self, xmlElement, model):
        unvcondition = model.getComponent('UniverseCondition')
        if unvcondition is None:
            unvcondition = {}
        
        dName = xmlElement.get('name')
        ucondition_entity = EntityDef(dName)
        ucondition_entity.addProperty('name', xmlElement.get('name'))
        ucondition_entity.addProperty('class', xmlElement.get('class'))
        ucondition_entity.addProperty('extension', xmlElement.get('extension'))
        
        searchTags = ['ORDERNRO' ,'MULTISELECTION', 'CONDOBJCLASS', 'CONDOBJECT', 'AUTOGENERATE', 
                      'DESCRIPTION', 'PROMPTTEXT', 'CONDWHERE', 'FREETEXT']
        for child in xmlElement:
            if child.tag in searchTags:
                strValue = xmlElement.find(child.tag).text
                if strValue is not None:
                    ucondition_entity.addProperty(child.tag, strValue.strip())
                    
        unvcondition[dName] = ucondition_entity
        model.addComponent('UniverseCondition', unvcondition)
        
        return model
    