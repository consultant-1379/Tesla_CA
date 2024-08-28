'''
Created on Oct 25, 2017

@author: xarjsin
'''
from Actions import ApplyWeekBHModificationMissingKey,ApplyMonthBHModificationMissingKey,ApplyDayBHModificationMissingKey

class IsValidMissingKeyBHModificationRule(object):
    
    def runRule(self,collectionBH, actionModel):
        print 'Rule to check if table is a valid BH (DUBH) type for this modification'
        validBH = self.checkIfValid(collectionBH)
        if len(validBH) > 0:
            print 'Modification to be applied to ' + str(len(validBH)) + ' tables'
            actionModel = ApplyWeekBHModificationMissingKey().runAction(validBH,actionModel)
            actionModel = ApplyMonthBHModificationMissingKey().runAction(validBH,actionModel)
            actionModel = ApplyDayBHModificationMissingKey().runAction(validBH,actionModel)
        else:
            print 'Modfications will not be applied'
        return actionModel
            
            
    def checkIfValid(self,collectionBH):
        
        valBH = {}
        ambBH = collectionBH.copy()
        for meas in collectionBH.iterkeys():
            bhTab = meas.split('::')
            if bhTab[0].endswith('DUBH'):
                valBH[meas] = collectionBH[meas]
                del ambBH[meas]
                
        if len(ambBH) > 0:
            self.decisionOnTable(ambBH)
            
        return valBH
    
    def decisionOnTable(self,ambiguousTables):
        pass#print 'Decision point for ambiguous ' + str(len(ambiguousTables)) + ' tables'