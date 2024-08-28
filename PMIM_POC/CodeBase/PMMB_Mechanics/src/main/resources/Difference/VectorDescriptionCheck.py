'''
Created on Nov 8, 2017

@author: xarjsin
'''

from Model import EntityDef, EntityRef
from Actions import ApplyVectorInformation

class VectorDescriptionCheck(object):
    
    
    def runRule(self, nodeModel, tpModel, actionModel, nodeRelease):
        print "Rule to check vector indices"
        nodeVectorDesc = self.parseVectorNode(nodeModel, nodeRelease)
        tpVectorInd = self.parseVectorTP(tpModel)
        for key in tpVectorInd:
            if key in nodeVectorDesc:
                if self.isEqualVectors(tpVectorInd[key].getComponent('Vectors'), nodeVectorDesc[key].getComponent('Vectors')) == 0:
                    actionModel = ApplyVectorInformation().runAction(actionModel, nodeVectorDesc[key], key, 'VALID')
                elif self.isEqualVectors(tpVectorInd[key].getComponent('Vectors'), nodeVectorDesc[key].getComponent('Vectors')) < 0:
                    actionModel = ApplyVectorInformation().runAction(actionModel, nodeVectorDesc[key], key, 'USER CONFIRMATION REQUIRED')
                else:
                    actionModel = ApplyVectorInformation().runAction(actionModel, tpVectorInd[key], key, 'NEW RULE REQUIRED')
            else:
                if key.find('_Events') == -1:
                    print "Vector " + key + " deprecated"
        
        for key in nodeVectorDesc:
            if key in tpVectorInd:
                pass
            else:
                print "Vector " + key + " not available in TP"
                
        return actionModel
    
    
    def isEqualVectors(self, tpVec, nodeVec):
        result = 0
        for tpIndName, tpIndProp in tpVec.iteritems():
            try:
                nodeIndProp = nodeVec[tpIndName]
            except KeyError:
                return 2
            
            if not (nodeIndProp.hasProperty('MEASURE') and nodeIndProp.hasProperty('VFROM') and nodeIndProp.hasProperty('VTO')):
                return 1
            
            if (tpIndProp.getProperty('QUANTITY') != nodeIndProp.getProperty('QUANTITY') 
                or tpIndProp.getProperty('MEASURE') != nodeIndProp.getProperty('MEASURE') 
                or tpIndProp.getProperty('VFROM') != nodeIndProp.getProperty('VFROM') 
                or tpIndProp.getProperty('VTO') != nodeIndProp.getProperty('VTO')):
                result = result - 1
            else:
                pass
            
        return result
        
        
    def parseVectorNode(self,nodeModel, nodeRelease):
        vectorIndex = {}
        classLayer = nodeModel.getComponent('Classes')
        for moid, moProps in classLayer.iteritems():
            attLayer = moProps.getComponent('Attributes')
            if attLayer:
                for attName, attProps in attLayer.iteritems():
                    if attProps.hasProperty('counterType'):
                        if attProps.getProperty('counterType') == 'PDF':
                            if (attProps.getProperty('description').lower().find('compressed: true') == -1 
                                and attProps.getProperty('description').lower().find('pdf ranges') != -1):
                                vectorIndVal = self.getVectorEntity(attProps.getProperty('description'), nodeRelease)
                                vectorIndex[moid + '::' + attName] = vectorIndVal

        return vectorIndex
            
    
    def getVectorEntity(self, vectorDescription, nodeRelease):
        vecIndexModel = EntityDef(nodeRelease)
        vecIndex = {}
        vecIndexList = vectorDescription.split('\n')
        for line in vecIndexList:
            if line.startswith('['):# or line.startswith('.'):
                pdfRange = line.split(':')
                if len(pdfRange) != 2:
                    continue
                
                index = pdfRange[0].lstrip('[')
                index = index.rstrip(']')
                props = pdfRange[1].strip()
                individualIndexModel = EntityDef(index)
                individualIndexModel.addProperty('QUANTITY', '0')
                if props.startswith('[') or props.startswith(']'):
                    if props.startswith('['):
                        vFrom = props[1:props.find('..')]
                    elif props.startswith(']'):
                        try:
                            vFrom = int(props[1:props.find('..')]) + 1
                        except ValueError:
                            vFrom = float(props[1:props.find('..')]) + 0.1
                            
                    individualIndexModel.addProperty('VFROM', str(vFrom))
                    vTo = props[props.find('..') + 2:len(props)]
                    if vTo.find(']') != -1:
                        meas = vTo[vTo.find(']') + 1:len(vTo)].strip()
                        vTo = vTo[0:vTo.find(']')]
                    else:
                        meas = vTo[vTo.find('[') + 1:len(vTo)].strip()
                        try:
                            vTo = int(vTo[0:vTo.find('[')]) - 1
                        except ValueError:
                            vTo = float(vTo[0:vTo.find('[')]) - 0.1
                    
                    if meas.endswith(','):
                        meas = meas.strip(',')

                    individualIndexModel.addProperty('VTO', str(vTo))
                    individualIndexModel.addProperty('MEASURE', str(meas))
                elif props.startswith('=') or props.startswith('>') or props.startswith('<'):
                    individualIndexModel.addProperty('VFROM', '')
                    vTo = props[0:props.rfind(' ')]
                    vTo = vTo.replace(' ','')
                    individualIndexModel.addProperty('VTO', vTo)
                    meas = props[props.rfind(' '):len(props)].strip()
                    if meas.endswith(','):
                        meas = meas.strip(',')
                        
                    individualIndexModel.addProperty('MEASURE', meas)
                elif props[0].isalpha():
                    individualIndexModel.addProperty('MEASURE', props.strip())
                    individualIndexModel.addProperty('VFROM', '')
                    individualIndexModel.addProperty('VTO', '')

                vecIndex[index] = individualIndexModel
                
        vecIndexModel.addComponent('Vectors', vecIndex)
        return vecIndexModel
        
    
    def parseVectorTP(self,tpModel):
        vectorIndex = {}
        tablesLayer = tpModel.getComponent('Tables')
        for tabName, tabDef in tablesLayer.iteritems():
            if tabDef.getProperty('tableType') == 'Measurement' and tabDef.getProperty('RANKINGTABLE') == '0':
                etlLayer = tpModel.getComponent('ETL')['mdc'].getComponent('Tables')[tabName].getComponent('TableTags')
                if etlLayer:
                    sourceName = etlLayer[etlLayer.keys()[0]].getSourceName()
                    attLayer = tabDef.getComponent('Attributes')
                    for attName, attDef in attLayer.iteritems():
                        if attDef.getProperty('attributeType') == 'measurementCounter':
                            if attDef.getProperty('COUNTERTYPE') == 'VECTOR':
                                if attDef.getComponent('VectorReleases'):
                                    vecLayer = attDef.getComponent('VectorReleases')
                                    for version, release in vecLayer.iteritems():
                                        if version == 'L17.Q4':
                                            vectorIndex[sourceName + '::' + attName] = release
        
        return vectorIndex
    
                                