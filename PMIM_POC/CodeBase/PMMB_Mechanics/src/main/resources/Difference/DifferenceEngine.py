'''
Created on Oct 24, 2017

@author: ebrifol
'''

from Model import EntityDef, EntityRef
from Actions import NewKeyCounter, NewTable

class DifferenceEngine(object):
    '''
    Assumption that the baseModel is a TP and the compare Model is a node
    The user should also have defined which parser to apply the difference against. 
    '''

    def performDiff(self, baseModel, compareModel, ETLname):
        self.actionModel = EntityDef('Actions')
        self.baseModel = baseModel
        
        ETLlayer = baseModel.getComponent('ETL')[ETLname]
        tablesCollection = ETLlayer.getComponent('Tables')
        
        TPtableTags = []
        
        for tablename, table in tablesCollection.iteritems(): #iterate over each of the tables in the ETL layer
            
            if 'TableTags' in table.listComponentNames(): #if that table has a tag
                for referencename, entityref in table.getComponent('TableTags').iteritems():
                    nodeClasses = compareModel.getComponent(entityref.getEntityType())

                    if entityref.getEntityName() in nodeClasses:
                        nodeClass = compareModel.getComponent(entityref.getEntityType())[entityref.getEntityName()]
                        self.diffAttributes(table, nodeClass)
                        
                        if entityref.getEntityName() not in TPtableTags:
                            TPtableTags.append(entityref.getEntityName())
                        
                    else:
                        print 'Unable to find corresponding class for ' + entityref.getEntityName()
        
        
        nodeClasses = compareModel.getComponent('Classes').keys()
        differences = list(set(TPtableTags) - set(nodeClasses))
#         if len(differences) > 0:
#             print 'New tags found'
#             print differences
#         print '\n'
        
        return self.actionModel
                  
    
    def diffAttributes(self, TPtable, NodeClass):
        scenario = NewKeyCounter()
        TPattributes = TPtable.getProperties().values()
        NodeAttributes = NodeClass.getComponent('Attributes').keys()
        
        differences = list(set(NodeAttributes) - set(TPattributes))
        self.actionModel = scenario.addCounter(self.baseModel, TPtable.getName(), NodeClass, differences, self.actionModel)
        
#         if len(differences) > 0:
#             print TPtable.getName()
#             print len(differences)
#             print differences
#         print '\n'
         
         

        