'''
Created on Mar 20, 2018

@author: ebrifol
'''

import os
from ModMan import ModuleManager
from Utilities import Print_formatter
from Impacts import ActionList

class ImpactsEngine(object):

    def __init__(self, homedirectory, gitDirectory):
        self.modmanager = ModuleManager()
        self.printer = Print_formatter()
        self.homedirectory = homedirectory
        self.gitDirectory = gitDirectory
        self.nodesDir = self.gitDirectory + '/Node'
        self.FeaturesDir = self.gitDirectory + '/Feature'
        self.TPsDir = self.gitDirectory + '/TP'
        self.ImplsDir = self.gitDirectory + '/Impl'
    
    
    def determineImpact(self, node_model, impl_model):
        Actionlist = ActionList()
        
        tps = impl_model.getComponent('TP')
        if tps is not None:
            for tp in tps.itervalues():
                params = {}
                params['filepath'] = self.TPsDir + '/' + tp.getSourceName()
                tp_model = self.modmanager.executeMethod('XML_PMIM_Parser', 'parse', params)
        else:
            raise Exception('Implementation ' + impl_model.getName() + ' has no referenced TP')
            
        params = {}
        params['Node'] = node_model
        params['TP'] = tp_model
        
        for measurement in node_model.getComponent('Measurements').itervalues():
            rule = self.findRelevantRule(measurement, impl_model.getComponent('Rules'), 'Measurements', Actionlist)
            if rule is not None:
                params['measurement'] = measurement
                params['Rule'] = rule
                self.runRuleImpactAnalysis(rule.getProperty('Rule'), params)
            
            for attribute in measurement.getComponent('Attributes').itervalues():
                rule = self.findRelevantRule(attribute, impl_model.getComponent('Rules'), 'Measurements', Actionlist)
                if rule is not None:
                    params['attribute'] = attribute
                    self.runRuleImpactAnalysis(rule.getProperty('Rule'), params)
        
    
    def findRelevantRule(self, model_entity, rules_model, area, Actionlist):
        if not rules_model.hasComponent(area):
            Actionlist.addRedAction('Missing Rule area', 'Missing rule area for ' + area)
            return Actionlist, None
        else:
            rule_area = rules_model.getComponent(area)
            
            
        
        
        
        
        if rule_area.hasComponent('Rules'):
            pass
        for variant in rule_area.getComponent('Rules'):
            pass
        
        
        
        ignore = rules_model.getComponent('Ignore')
        if ignore.hasProperty(area):
            ignorelist = ignore.getProperty(area).split(',')
            if model_entity.getName() in ignorelist:
                return None
        
        areaVariants = rules_model.getComponent(area)
        for variant in areaVariants.getComponents().itervalues():
            if self.RuleConditionsMatch(variant.getProperties(), model_entity):
                return variant
        
        return rules_model.getComponent(area)
    
    def RuleConditionsMatch(self, properties, model_entity):
        match = False
        for key, value in properties.iteritems():
            if key.startswith('id:'):
                property = key.split(':')[1]
                if property.lower() == 'name':
                    if model_entity.getName == value:
                        match = True
                
                if model_entity.hasProperty(property):
                    if model_entity.getProperty(property) == value:
                        match = True
        
        return match
    
    def runRuleImpactAnalysis(self, rule, params):
        red, yellow, green = self.modmanager.executeMethod(rule, 'analyse_impact', params)
        
            
        
    