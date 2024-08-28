'''
Created on 8 Mar 2018

@author: xarjsin
'''
from Model import EntityDef,EntityRef
import RulesRepository
import inspect
import sys
import Utilities as Utils

class TPRules_Engine(object):
    '''
    Rules Engine for Techpacks - Takes Node model and Implementation model as inputs
    Upgrade/create a ENIQ-Stats TP
    '''
    def __init__(self, params):
        '''
        Sends Node (NND), Techpack and Implementation model
        '''
        self.execute = False
        self.NodeModel = params['NodeModel']
        self.TPModel = params['TPModel']
        self.RulesImpl = params['ImplementationModel']
        self.result = {}
        if 'ActionList' in params.keys():
            self.execute = True
            self.ImplActionList = params['ActionList']
        
    def runRules(self):
        '''
        Take latest node model and create a TP by running it against corresponding implementation 
        '''
        if(self.execute):
            NewTpModel = self.TPModel
            parameters = {}
            if(self.checkForRedYellow()):
                print "Updating " + self.TPModel.getName()
                validChanges = self.ImplActionList.getComponent('GREEN')
                for ruleName, ruleEntity in validChanges.iteritems():
                    for name, obj in inspect.getmembers(RulesRepository,inspect.isclass):
                        if ruleName == name:
                            parameters['NewTPModel'] = NewTpModel
                            parameters['RuleEntity'] = ruleEntity
                            rule = obj(parameters)
                            NewTpModel = rule.execute()
            else:
                print "There are RED and/or YELLOW FLAGS, Model will not be updated"
            self.result['UpdatedModel'] = NewTpModel
        else:
            print "Running rules for " + self.TPModel.getName()
            ActionTitle = 'ActionList_' + self.TPModel.getName()
            ActionList = EntityDef(ActionTitle)
            for l1Name, l1Obj in self.NodeModel.getComponents().iteritems():
                ruleParams = {}
                ruleParams['RuleObject'] = l1Name
                ruleParams['ActionList'] = ActionList
                res = self.runRule(ruleParams,"RootComponents")
                ActionList = res['ActionList']
                if 'Ignore' not in res:
                    res['Ignore'] = True
                if res['Ignore'] == False:
                    for moName, moDetails in l1Obj.iteritems():
                        try:
                            for attrName, attrDetails in moDetails.getComponent("Attributes").iteritems():
                                if self.checkNewCounterEvent(moName,attrName):
                                    ruleParams = {}
                                    ruleParams['ActionList'] = ActionList
                                    ruleParams['MoName'] = moName
                                    ruleParams['CounterName'] = attrName
                                    ruleParams['CounterDetails'] = attrDetails
                                    ruleParams['TPModel'] = self.TPModel
                                    res = self.runRule(ruleParams,"NewCounterEvent")

                                    ActionList = res['ActionList']
                        except AttributeError:
                            print moName + " has no attribute"
                        
            self.result['ActionList'] = ActionList
        
        return self.result
    
    def checkForRedYellow(self):
        redComp = self.ImplActionList.getComponent("RED")
        if any(redComp):
            return False
        
        yellowComp = self.ImplActionList.getComponent("YELLOW")
        if any(yellowComp):
            return False
        
        return True
    
    def runRule(self,ruleParams,RuleEvent):
        resultParams ={}
        ruleToRun = self.getRuleFromImpl(RuleEvent)
        ActionList = ruleParams['ActionList']
        if ruleToRun == None:
            ActionList = self.ruleNotFound(ActionList,RuleEvent)
            resultParams['ActionList'] = ActionList
        else:
            for name, ruleObj in inspect.getmembers(sys.modules[RulesRepository.__name__],inspect.isclass):
                if name == ruleToRun:
                    rule = ruleObj(ruleParams)
                    resultParams = rule.prep()
                
        return resultParams
    
    def getRuleFromImpl(self,RuleEvent):
        Rules = self.RulesImpl.getComponent("Rules")
        for name, obj in Rules.iteritems():
            if RuleEvent == name:
                if obj.hasProperty('Rule'):
                    return obj.getProperty('Rule')
                else:
                    return None

        return None

    def ruleNotFound(self,ActionList,RuleEvent):
        redComponent = ActionList.getComponent('RED')
        if redComponent is None:
            redComponent = Utils.odict()
            
        actionEntity = EntityDef(RuleEvent)
        actionEntity.addProperty('ERROR', "RULE NOT FOUND FOR " + RuleEvent)
        actionEntity.addComponent('AVAILABLE RULES',self.getAvailableRulesComponent(RuleEvent))
        redComponent[RuleEvent] = actionEntity
        ActionList.addComponent('RED', redComponent)
        return ActionList
    
    def getAvailableRulesComponent(self,Event):
        ruleComponent = {}
        for name, obj in inspect.getmembers(RulesRepository,inspect.isclass):
            if name.endswith("_Rule"):
                rule = EntityDef(name)
                rule.addProperty('Description',obj.__doc__)
                ruleComponent[name] = rule
            
        return ruleComponent
    
    def checkNewCounterEvent(self,MoName,attrName):
        if attrName.startswith('pm'):
            attList = []
            for parserName, parspec  in self.TPModel.getComponent('ETL').iteritems():
                for tabName, tabDetails in parspec.getComponent('Tables').iteritems():
                    if 'TableTags' in tabDetails.listComponentNames():
                        for refName, ref in tabDetails.getComponent('TableTags').iteritems():
                            if MoName == ref.getEntityName():
                                attList.extend(tabDetails.getProperties().values())
                            
            if attList:
                if attrName not in attList:
                    print "Counter " + attrName + " is new in MO " + MoName
                    return True

        return False
        
        
    