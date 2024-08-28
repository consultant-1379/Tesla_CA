'''
Created on Nov 3, 2017

@author: ebrifol
'''

class ExampleDiff(object):
    '''
    classdocs
    '''

    def execute(self, params):
        print 'hello'
        
        #Do some stuff here that finds me a difference. 
        configmanager = params['configManager']
        actionsconfig = configmanager.getMechanicComponent('Actions')
        
        for OptionName, config in actionsconfig.iteritems():
            #Not sure if these should be run in a specific sequence or not
            for DiffName, value in config.getProperties().iteritems():
                configmanager.executeMechanism('Actions', value, params)