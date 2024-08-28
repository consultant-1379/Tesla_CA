'''
Created on Nov 13, 2017

@author: xarjsin
'''

from Model import EntityDef,EntityRef
import Utilities as Utils

class ApplyVectorInformation(object):
    
    def runAction(self, actionModel, vecFromNode, vectorCounter, case):
        
        actions = actionModel.getComponent('Vectors')
        if actions is None:
            actions = Utils.odict()
        actionEntity = vecFromNode
        release = actionEntity.getName()
        actionEntity.setName(vectorCounter)
        actionEntity.addProperty('actionType',case)
        actionEntity.addProperty('RELEASE',release)
        actions[vectorCounter] = actionEntity
        actionModel.addComponent('Vectors', actions)
        
        return actionModel
    
    
    