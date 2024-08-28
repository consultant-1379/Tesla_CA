'''
Created on Oct 25, 2017

@author: xarjsin
'''
    
    
class IsElemBHModificationRule(object):
    
    def runRule(self,collectionBH):
        print 'Rule to check if table is ELEM type - modification does not apply to ELEMBH tables'
        nonElemBH = self.checkIfELEM(collectionBH)
        return nonElemBH
        
    def checkIfELEM(self,collectionBH):
        
        ElemBHMeas = []
        nonEleBH = collectionBH.copy()
        for meas in collectionBH.iterkeys():
            bhTab = meas.split('::')
            if bhTab[0].endswith('ELEMBH'):
                ElemBHMeas.append(bhTab[1])
                del nonEleBH[meas]
                
        print 'Ignored for ' + str(len(ElemBHMeas)) + ' cases since ELEMBH'
        return nonEleBH