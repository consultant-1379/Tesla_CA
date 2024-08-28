'''
Created on Nov 28, 2017

@author: ebrifol
'''

import Utilities as Utils
from Parsers import ECIM_Parser, TP_Parser, PMIM_Parser
from Difference import DifferenceEngine, VectorDescriptionCheck, CheckMissingKeyBHModification
#import os


if __name__ == '__main__':
    #ECIM = Utils.fileToXMLObject('C:/Users/ebrifol/Documents/Projects/PMIM/InputFiles/NodeMomLimited_L17B_R27B01.xml')
    
    #Brians paths
    inputpath = 'C:/Users/ebrifol/Documents/Projects/PMIM/InputFiles/'
    outputpath = 'C:/Users/ebrifol/Documents/Projects/PMIM/OutputResult/'
    
    params = {}
    params['filepath'] = inputpath + 'mechanics_DiffBase.pmim'
    parser = PMIM_Parser(params)
    base = parser.parse()
    
    params['filepath'] = inputpath + 'mechanics_DiffComp.pmim'
    parser = PMIM_Parser(params)
    comp = parser.parse()

    delta = base.difference(comp)
    
    print 'Writing File'
    outputFile = open(outputpath + delta.getName() + '.pmim', 'w+')
    delta.toXML(outputfile=outputFile)
    outputFile.close()
    print 'Complete\n'