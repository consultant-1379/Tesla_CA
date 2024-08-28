'''
Created on Oct 25, 2017

@author: xarjsin
'''

from Model import EntityDef, EntityRef
from Difference import IsElemBHModificationRule, IsValidMissingKeyBHModificationRule

class CheckMissingKeyBHModification(object):
    
    def checkCriteria(self,tpModel, actionModel):
        print 'Checking for manual modification requirement'
        tpName = tpModel.getName()
        bhLayer = tpModel.getComponent('BusyHours')
        bhModCollection = {}
        for bhName, bhDetail in bhLayer.iteritems():
            bhKeysList = []
            supportedTables = bhDetail.getComponent('SupportedTables').keys()
            bhTable = tpModel.getComponent('Tables')[tpName + '_' + bhName + 'BH']
            for bhKeyName, bhAtt in bhTable.getComponent('Attributes').iteritems():
                if bhAtt.getProperty('attributeType') == 'measurementKey':
                    bhKeysList.append(bhKeyName)
            for eachMeasTable in supportedTables:
                measKeysList = []
                modBHKey = 'DC_E_ERBS_' + bhName + 'BH' + '::' + eachMeasTable
                measTable = tpModel.getComponent('Tables')[eachMeasTable]
                for measKeyName, measAtt in measTable.getComponent('Attributes').iteritems():
                    if measAtt.getProperty('attributeType') == 'measurementKey':
                        measKeysList.append(measKeyName)
                differences = list(set(bhKeysList) - set(measKeysList))
                if len(differences) > 0:
                    bhModCollection[modBHKey] = differences
                
        if len(bhModCollection) > 0:
            print 'Criteria met for ' + str(len(bhModCollection)) + ' cases'
            #print bhModCollection
            actionModel = self.applyRules(bhModCollection, actionModel)
        else:
            print 'Criteria not met - modification is not required'
        
        return actionModel
            
    def applyRules(self,bhModCollection,actionModel):
        print 'Running rules for Missing BH Rank Key Scenario'
        nonElemBH = IsElemBHModificationRule().runRule(bhModCollection)
        if len(nonElemBH) > 0:
            actionModel = IsValidMissingKeyBHModificationRule().runRule(nonElemBH,actionModel)
        else:
            print 'Only ELEMBH tables meet criteria - modification not required'
            
        return actionModel
                
                
                
                
                
                
                