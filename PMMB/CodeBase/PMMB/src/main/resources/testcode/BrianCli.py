'''
Created on Feb 13, 2018

@author: ebrifol
'''

import timeit
import os
from Parsers import Classic_MIM_Parser, XML_PMIM_Parser, TP_Parser

if __name__ == '__main__':
    
#     inputpath = 'C:/Users/ebrifol/Documents/Development/ToolingSuite/InputFiles/'
#     outputpath = 'C:/Users/ebrifol/Documents/Development/ToolingSuite/OutputFiles/'
    
#     inputpath = 'C:/Users/ebrifol/Documents/Development/ToolingSuite\/codebase/PMIM/testFiles/'
#     outputpath = 'C:/Users/ebrifol/Documents/Development/ToolingSuite\/codebase/PMIM/testFiles/'
#     
#     
#     
#     params = {}
# #     params['filepath'] = inputpath + 'NodeMomLimited_L17B_R27B01.xml'
#     params['filepath'] = inputpath + 'ECIM_TestFile.xml'
#     
#     
#     start = timeit.default_timer()
#     print 'Parsing ECIM'
#     parser = ECIM_Parser(params)
#     Nodemodel = parser.parse()    
#     stop = timeit.default_timer()
#     print stop - start
#     print 'Parsing done\n'
#     
#     start = timeit.default_timer()
#     print 'Writing XML File'
#     outputFile = open(outputpath + Nodemodel.getName() + '.xml', 'w+')
#     Nodemodel.toXML(outputfile=outputFile)
#     outputFile.close()
#     stop = timeit.default_timer()
#     print stop - start
#     print 'XML Complete\n'
#     
#     start = timeit.default_timer()
#     print 'Writing JSON File'
#     outputFile = open(outputpath + Nodemodel.getName() + '.json', 'w+')
#     outputFile.write(Nodemodel.toJSON())
#     outputFile.close()
#     stop = timeit.default_timer()
#     print stop - start
#     print 'JSON Complete\n'
#     
#     start = timeit.default_timer()
#     print 'Parse XML PMIM file'
#     params['filepath'] = outputpath + Nodemodel.getName() + '.xml'
#     parser = XML_PMIM_Parser(params)
#     Nodemodel = parser.parse()
#     stop = timeit.default_timer()
#     print stop - start
#     print 'Parsing XML Complete\n'
#     
#     start = timeit.default_timer()
#     print 'Parse JSON PMIM file'
#     params['filepath'] = outputpath + Nodemodel.getName() + '.json'
#     parser = JSON_PMIM_Parser(params)
#     Nodemodel = parser.parse()
#     stop = timeit.default_timer()
#     print stop - start
#     print 'Parsing JSON Complete\n'
#     
#     start = timeit.default_timer()
#     print 'Re-writing JSON File'
#     outputFile = open(outputpath + Nodemodel.getName() + '_rewrite.json', 'w+')
#     outputFile.write(Nodemodel.toJSON())
#     outputFile.close()
#     stop = timeit.default_timer()
#     print stop - start
#     print 'JSON Complete\n'
#     

# 
#     inputFilesDir =  'C:/Users/ebrifol/Documents/Projects/TPD/ES_TP/NND/'
#         
#     params = {}
#     
# #     outputFile = open(inputFilesDir + Nodemodel.getName() + '.xml', 'w+')
# #     Nodemodel.toXML(outputfile=outputFile)
#          
#     params['filepath'] = inputFilesDir + 'ERBS.xml'
#     parser = XML_PMIM_Parser(params)
#     model = parser.parse()
#     
#     print model.getProperties()

    inputpath = 'C:/Users/ebrifol/Documents/Projects/PMIM/InputFiles/'
    
    params = {}
    params['filepath'] = inputpath + 'DC_E_ERBS_167_R26A.xml'
    print 'Parsing TP'
    parser = TP_Parser(params)
    TPmodel = parser.parse()
    print 'Parsing done'
      
    print 'Writing File'
    outputFile = open(inputpath + TPmodel.getName() + '.pmim', 'w+')
    TPmodel.toXML(outputfile=outputFile)
    outputFile.close()
    print 'Complete\n'

    
    