'''
Created on Mar 1, 2018

@author: ebrifol
'''

import os
import traceback
from os.path import expanduser

from Utilities import Print_formatter
from GIT import Git_interface
from ModMan import ModuleManager
from Impacts import ImpactsEngine, ImplValidator, ActionList

from com.ericsson.PMMB import CLI

class PMMB_CLI(CLI):
    
    def __init__(self):
        self.modmanager = ModuleManager()
        self.printer = Print_formatter()
        self.homedirectory = expanduser('~') + '/PMMB'
        self.GitRepo = self.homedirectory + '/ES_TP'
        self.nodesDir = self.GitRepo + '/Node'
        self.FeaturesDir = self.GitRepo + '/Feature'
        self.TPsDir = self.GitRepo + '/TP'
        self.ImplsDir = self.GitRepo + '/Impl'

    def run_command_prompt(self, args):
        try:
            
            # create the home directory if it doesnt exist
            if not os.path.exists(self.homedirectory):
                os.makedirs(self.homedirectory)
            
            if len(args) == 2:
                self.printer.Pink('Validating input arguments', True)
                
                node_model_name = args[0]
                new_node_input = args[1]
                
                if not node_model_name.endswith('.xml'):
                    node_model_name = node_model_name + '.xml'
                
                #Test if the input file path exists
                if os.path.exists(new_node_input):
                    #Clone the GIT repo to check if the node input exists. 
                    self.cloneGitRepo()
                    #Test if the node model exist in the GIT repo
                    print self.nodesDir + '/' + node_model_name
                    if os.path.exists(self.nodesDir + '/' + node_model_name):
                        self.printer.Green('Valid arguments provided', True)
                        
                        existing_node_model, new_node_model = self.CompareNodeModels(self.nodesDir + '/' + node_model_name, new_node_input)
                        
                        actionList = ActionList()
                        impacted_featues = self.findImpactedImpls(new_node_model)
                        for feature, impls in impacted_featues.iteritems():
                            for impl in impls:
                                actions = ImplValidator().Validate(impl)
                                actionList.merge(actions)
                                
                                impactsengine = ImpactsEngine(self.homedirectory, self.GitRepo)
                                actions = impactsengine.determineImpact(new_node_model, impl)
                                actionList.merge(actions)
                        
                    else:
                        self.printer.Yellow('Node model ' + args[0] + ' does not exist', True)
                        self.printHelp()
                    
                else:
                    self.printer.Yellow('Input file ' + args[1] + ' does not exist', True)
                    self.printHelp()
                
            else:
                self.printHelp()
        
        except:
            self.printer.Red('\nError during execution', True)
            traceback.print_exc()
            self.printer.Red('\n', True)
        
    
    def cloneGitRepo(self):
        if not os.path.exists(self.GitRepo):
            self.printer.White('Cloning GIT Repository', True) 
            Git_interface(self.homedirectory).clone('F:\ES_TP')
        else:
            self.printer.White('Pulling latest GIT Repository', True)
            Git_interface(self.GitRepo).pull()
    
    
    def CompareNodeModels(self, existing_node, new_node):
        self.printer.White('Loading ' + existing_node, True) 
        params = {}
        params['filepath'] = existing_node
        existing_node_model = self.modmanager.executeMethod('XML_PMIM_Parser', 'parse', params)
        
        self.printer.White('Loading ' + new_node, True)
        params['filepath'] = new_node
        new_node_model = self.modmanager.executeMethod(existing_node_model.getProperty('ParsedBy'), 'parse', params)
        
        self.printer.White('Finding differences between the node versions', True)
        difference = existing_node_model.difference(new_node_model)
        if difference == None:
            self.printer.Green('No differences found between node versions', True)
        else:
            outputfilename = self.homedirectory + '/' + difference.getName() + '.xml'
            self.printer.Green('Differences found. Delta file written to ' + outputfilename, True)
            outputFile = open(outputfilename, 'w+')
            difference.toXML(outputfile=outputFile)
            outputFile.close()
        
        return existing_node_model, new_node_model
    
    
    def findImpactedImpls(self, node_model):
        features = os.listdir(self.FeaturesDir)
        impactedFeatures = {}
        for feature in features:
            params = {}
            params['filepath'] = self.FeaturesDir + '/' + feature
            feature_model = self.modmanager.executeMethod('XML_PMIM_Parser', 'parse', params)
            if self.isNodeReferenced(feature_model, node_model.getName()):
                impls = self.findImplFile(feature_model, node_model.getName())
                if len(impls) > 0:
                    self.printer.White(len(impls) + ' implementations from feature ' + feature_model.getName() + ' reference ' + node_model.getName(), True)
                    impactedFeatures[feature_model] = impls
        return impactedFeatures
       
            
    def isNodeReferenced(self, model, nndName):
        nnds = model.getComponent('Node')
        if nnds is not None:
            for nnd in nnds.itervalues():
                if nnd.getEntityName() == nndName:
                    return True 
        return False
    
    
    def findImplFile(self, solution, nndName):
        impactedImpl = []
        impls = solution.getComponent('IMPL')
        if impls is not None:
            for impl in impls.itervalues():
                params = {}
                params['filepath'] = self.ImplsDir + '/' + impl.getSourceName()
                model = self.modmanager.executeMethod('XML_PMIM_Parser', 'parse', params)
                if self.isNNDReferenced(model, nndName):
                    impactedImpl.append(model)             
        else:
            self.printer.printWarning(solution.getName() + ' contains no implementations. A new Implementation is required', True)
        
        return impactedImpl
    
        
    def printHelp(self):
        docs = self.modmanager.describeModules()
        for name, doc in docs.iteritems():
            print name
            print '\t' + doc
        
    
    
    
                
        