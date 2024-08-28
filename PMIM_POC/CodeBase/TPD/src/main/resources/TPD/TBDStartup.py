'''
Created on Oct 11, 2017

@author: ebrifol
'''

import Utilities as Utils
from Parsers import ECIM_Parser, TP_Parser, PMIM_Parser
from Difference import DifferenceEngine, VectorDescriptionCheck, CheckMissingKeyBHModification
#import os


if __name__ == '__main__':
    #ECIM = Utils.fileToXMLObject('C:/Users/ebrifol/Documents/Projects/PMIM/InputFiles/NodeMomLimited_L17B_R27B01.xml')
    
    #Brians paths
#    inputpath = 'C:/Users/ebrifol/Documents/Projects/PMIM/InputFiles/'
#    outputpath = 'C:/Users/ebrifol/Desktop/VC_Test/'
    
    #Arjuns Paths
    inputpath = 'H:/Transformation/PMIM/PMIM/InputFiles/'
    outputpath = 'H:/Transformation/PMIM/PMIM/OutputResult/'
    
    
#     os.chdir(outputpath)
#     print os.system('git clone F:\ES_TP ')
#     print '\n'
#     outputpath = outputpath + 'ES_TP/'
#       
    params = {}
    params['filepath'] = inputpath + 'NodeMomLimited_L17_Q4_R27V01.xml'
    print 'Parsing ECIM'
    parser = ECIM_Parser(params)
    Nodemodel = parser.parse()
    print 'Parsing done'
        
#    print 'Writing File'
#    outputFile = open(outputpath + Nodemodel.getName() + '.pmim', 'w+')
#    Nodemodel.toXML(outputfile=outputFile)
#    outputFile.close()
#    print 'Complete\n'
  
    params['filepath'] = inputpath + 'DC_E_ERBS_201_R27F.xml'
    print 'Parsing TP'
    parser = TP_Parser(params)
    TPmodel = parser.parse()
    print 'Parsing done'
      
#    print 'Writing File'
#    outputFile = open(outputpath + TPmodel.getName() + '.pmim', 'w+')
#    TPmodel.toXML(outputfile=outputFile)
#    outputFile.close()
#    print 'Complete\n'
       
    print 'Finding differences\n'
    difference = DifferenceEngine()
    actionModel = difference.performDiff(TPmodel, Nodemodel, 'mdc')
       
#    print 'Checking Scenarios'
#    manMod = CheckMissingKeyBHModification()
#    actionModel = manMod.checkCriteria(TPmodel, actionModel)
    
    vecChk = VectorDescriptionCheck()
    actionModel = vecChk.runRule(Nodemodel, TPmodel, actionModel, 'L17.Q4+')

#    print '\nWriting actions file'
#    outputFile = open(outputpath + actionModel.getName() + '.pmim', 'w+')
#    actionModel.toXML(outputfile=outputFile)
#    outputFile.close()
#    print 'Complete'
       
#     os.chdir(outputpath)
#     print os.system('git add .')
#     print os.system('git commit -a -m "Testing the git interaction" ')
#     print '\n'
#       
#     print os.system('git push ')
#      
#     parsers = TPmodel.getComponent('ETL')
#     ETLlayer = parsers['mdc']
#     tablesCollection = ETLlayer.getComponent('Tables')
#     newTables = Utils.odict()
#     for tablename, table in tablesCollection.iteritems():
#         newtablename = tablename + '_updated'
#         table.setName(newtablename)
#         newTables[newtablename] = table
#      
#     ETLlayer.addComponent('Tables', newTables)
#     parsers['mdc'] = ETLlayer
#     TPmodel.addComponent('ETL', parsers)
#  
#     print 'Writing File'
#     outputFile = open(outputpath + TPmodel.getName() + '.pmim', 'w+')
#     TPmodel.toXML(outputfile=outputFile)
#     outputFile.close()
#     print 'Complete\n'
#       
#     print os.system('git commit -a -m "Testing the git interaction updating" ')
#     print '\n'
#      
#     print os.system('git push ')


#    inputpath = 'C:/Users/ebrifol/Documents/Projects/PMIM/InputFiles/'
#    params = {}
#    params['filepath'] = inputpath + 'mechanics.pmim'

#    from Mechanics import DifferenceMechanism
#    diff = DifferenceMechanism(params)
    
#    diff.determineActionList()
    
