'''
Created on Nov 3, 2017

@author: ebrifol
'''

from MechConfigManager import MechConfigManager

class DifferenceMechanism(object):

    def __init__(self, params):
        self.params = params
    
    def determineActionList(self):
        configmanager = MechConfigManager(self.params)
        
        differenceconfig = configmanager.getMechanicComponent('Difference')
        self.params['configManager'] = configmanager
        
        for OptionName, config in differenceconfig.iteritems():
            #Not sure if these should be run in a specific sequence or not
            for DiffName, value in config.getProperties().iteritems():
                configmanager.executeMechanism('Difference', value, self.params)
        