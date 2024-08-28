'''
Created on 9 Mar 2018

@author: xarjsin
'''
from Model import EntityDef,EntityRef
import Utilities as Utils

class NewCounter_Rule(object):
    '''
    Rule that defines behaviour if a new counter found
    '''


    def __init__(self, params):
        '''
        Initialises something, define later
        '''
        if 'RuleEntity' in params:
            self.ruleEntity = params['RuleEntity'] 
            self.UpdateModel = params['NewTPModel']
        else:
            self.ActionList = params['ActionList']
            self.MoName = params['MoName']
            self.attrName = params['CounterName']
            self.attrDetails = params['CounterDetails']
            self.TPModel = params['TPModel']
    
    def prep(self):
        '''
        Checks for new counter Event
        '''
        Result = {}
        self.checkCounterType()
        self.ActionList = self.addCounter()
        Result['ActionList'] = self.ActionList

        return Result
    
    def execute(self):
        '''
        Updates TP Model with New Counters
        '''
        for listTabName, listTabProps in self.ruleEntity.getComponent('Tables').iteritems():
            ETLLayer = self.UpdateModel.getComponent('ETL')
            for parserName, parspec  in ETLLayer.iteritems():
                TabLayer = parspec.getComponent('Tables')
                for tabName, tabDetails in TabLayer.iteritems():
                    if tabName == listTabName:
                        newTabEnt = tabDetails
                        for attrName in listTabProps.getComponent('Attributes'):
                            newTabEnt.addProperty(attrName, attrName)
                    
                        TabLayer[tabName] = newTabEnt
                parspec.addComponent('Tables',TabLayer)
                ETLLayer[parserName] = parspec
            
        self.UpdateModel.addComponent('ETL',ETLLayer)
        return self.UpdateModel
        
    
    def getEntity(self,entName):
        pass
    
    def checkCounterType(self):
        counterType = "NORMAL"
        if self.attrDetails.getProperty('counterType') == 'PDF':
            counterType = "VECTOR"
        if self.attrDetails.getName().startswith('pmFlex'):
            counterType = "FLEX"
            
        self.getTableFromMo(counterType)
    
    def getTableFromMo(self,Type):
        for parserName, parspec  in self.TPModel.getComponent('ETL').iteritems():
                for tabName, tabDetails in parspec.getComponent('Tables').iteritems():
                    if 'TableTags' in tabDetails.listComponentNames():
                        for refName, ref in tabDetails.getComponent('TableTags').iteritems():
                            if self.MoName == ref.getEntityName():
                                if Type == "NORMAL":
                                    if not(tabName.endswith('_V') or tabName.endswith('_FLEX')):
                                        self.tableName = tabName
                                elif Type == "VECTOR":
                                    if tabName.endswith('_V'):
                                        self.tableName = tabName
                                elif Type == "FLEX":
                                    if tabName.endswith('_FLEX'):
                                        self.tableName = tabName
        
        
    def addCounter(self):
        greenComp = self.ActionList.getComponent('GREEN')
        if self.__class__.__name__ in greenComp.keys():
            ruleEnt = greenComp[self.__class__.__name__]
            if 'Tables' in ruleEnt.listComponentNames():
                tabComp = ruleEnt.getComponent('Tables')
                if self.tableName in tabComp.keys():
                    actionEntity = tabComp[self.tableName]
                    if 'Attributes' in actionEntity.listComponentNames():
                        attrLayer = actionEntity.getComponent('Attributes')
                    else:
                        attrLayer = Utils.odict()
                else:
                    actionEntity = EntityDef(self.tableName)
                    attrLayer = Utils.odict()
            else:
                tabComp = Utils.odict()
                actionEntity = EntityDef(self.tableName)
                attrLayer = Utils.odict()
        else:
            ruleEnt = EntityDef(self.__class__.__name__)
            tabComp = Utils.odict()
            actionEntity = EntityDef(self.tableName)
            attrLayer = Utils.odict()
            
        
        attEntity = EntityDef(self.attrName)
        attrLayer[self.attrName] = attEntity
        actionEntity.addComponent('Attributes',attrLayer)
        tabComp[self.tableName] = actionEntity
        ruleEnt.addComponent('Tables',tabComp)
        greenComp[self.__class__.__name__] = ruleEnt
        self.ActionList.addComponent('GREEN',greenComp)
        return self.ActionList
        
    
    def validate(self):
        '''
        '''
        pass
    
    
    def test(self):
        '''
        '''
        pass
    
    