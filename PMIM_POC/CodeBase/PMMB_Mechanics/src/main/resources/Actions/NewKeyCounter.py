'''
Created on Oct 25, 2017

@author: xarjsin
'''

import Utilities as Utils
from Model import EntityDef

class NewKeyCounter(object):
    
    def addCounter(self, TPmodel, tablename, NodeClass, differences, actionsModel):
        
        tableEntity = TPmodel.getComponent('Tables')[tablename]
        
        for attname in differences:
            if self.addCounterCriteria(tableEntity, NodeClass, attname):
                actionsModel = self.addAction(actionsModel, tablename, attname)
        
        return actionsModel
                    

    def addCounterCriteria(self, TPtable, NodeClass, attname):
        if TPtable.getName().endswith('_FLEX'):
            if attname.startswith('pmFlex'):
                return True
        
        if TPtable.hasProperty('VECTORSUPPORT') and not attname.startswith('pmFlex'):
            attDef = NodeClass.getComponent('Attributes')[attname]
            if TPtable.getProperty('VECTORSUPPORT') == '1':
                if attname.startswith('pm') and attDef.getProperty('counterType') == 'PDF':
                    return True
        
            if TPtable.getProperty('VECTORSUPPORT') == '0' and not TPtable.getName().endswith('_FLEX'):
                if attname.startswith('pm') and attDef.getProperty('counterType') != 'PDF':
                    return True
        
        return False
    
    def addAction(self, actionsModel, tablename, attname):
        tables = actionsModel.getComponent('Tables')
        if tables is None:
            tables = Utils.odict()
            
        tableEntity = None
        if tablename in tables:
            tableEntity = tables[tablename]
        else:
            tableEntity = EntityDef(tablename)
        
        attributes = tableEntity.getComponent('Attributes')
        if attributes is None:
            attributes = Utils.odict()
        
        attEntity = EntityDef(attname)
        attributes[attname] = attEntity
        
        tableEntity.addComponent('Attributes', attributes)
        tables[tablename] = tableEntity
        
        actionsModel.addComponent('Tables', tables)
        
        return actionsModel
        
            
        
        
        
        
        
        
        
        