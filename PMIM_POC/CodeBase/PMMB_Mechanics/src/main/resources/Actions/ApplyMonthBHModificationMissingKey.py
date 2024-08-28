'''
Created on Oct 25, 2017

@author: xarjsin
'''
from Model import EntityDef,EntityRef
import Utilities as Utils

class ApplyMonthBHModificationMissingKey(object):
    
    def runAction(self, inputToModification, actionModel):
        
        tables = actionModel.getComponent('Tables')
        if tables is None:
            tables = Utils.odict()
            
        print 'Applying modification for MonthBH query'
        for eachCase in inputToModification:
            eachTable = eachCase.split('::')[1]
            if eachTable in tables:
                tableEntity = tables[eachTable]
            else:
                tableEntity = EntityDef(eachTable)
                
            etlActions = tableEntity.getComponent('ETLActions')
            if etlActions is None:
                etlActions = Utils.odict()
            
            actionEntity = EntityDef('MonthBH')
            actionEntity.addProperty('actionType','ModifyActionContents')
            actionEntity.addProperty('actionName','RemoveWhereClauseKeys')
            actionEntity.addProperty('WhereClauseKeys', ','.join(inputToModification[eachCase]))
            etlActions['MonthBH'] = actionEntity
            tableEntity.addComponent('ETLActions',etlActions)
            tables[eachTable] = tableEntity
        
        actionModel.addComponent('Tables', tables)
        return actionModel