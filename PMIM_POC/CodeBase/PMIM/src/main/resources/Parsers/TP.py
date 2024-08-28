'''
Created on 13 Oct 2017

@author: xshubor
'''

from XML import XML_Parser
from Model import EntityDef, EntityRef
import Utilities as Utils

class TP_Parser(XML_Parser):
    '''
    This parser should be used to parse Tech pack inputs
    '''
    
    Tags_To_Parse = {'Versioning' : 'parse_versioning', 'Tables' : 'parse_tables', 
                     'BusyHours' : 'parse_busyhours', 'ExternalStatements' : 'parse_externalstmts'}#,
#                      'Interfaces' : 'parse_interfaces'}    
    
    def __init__(self, params):
        super(self.__class__, self).__init__(params, self)
        self.params = params
    
    def parse_versioning(self, xmlElement, model):
                        
        for child in xmlElement:     
            if child.tag == 'TECHPACK_NAME':
                model.setName(child.text)
            else:
                if child.tag == 'SupportedVendorReleases':
                    model = self.parse_supportedVendorRelease(child, model)
                elif child.tag == 'Dependencies':
                    model = self.parse_dependencies(child, model)
                else:
                    model.addProperty(child.tag, child.text.strip())
        
        return model
    
    def parse_supportedVendorRelease(self, xmlElement, model):
        supportVendorRelease = model.getComponent('SupportedVendorReleases')
        if supportVendorRelease is None:
            supportVendorRelease = Utils.odict()
        
        for child in xmlElement:
            refname = child.text
            reference_entity = EntityRef(refname)
            reference_entity.setSource(refname, 'PMIM')
            reference_entity.setEntity(refname , 'Node')
            supportVendorRelease[refname] = reference_entity
            
        model.addComponent('SupportedVendorReleases', supportVendorRelease)

        return model
    
    def parse_dependencies(self, xmlElement, model):
        dependency = model.getComponent('Dependencies')
        if dependency is None:
            dependency = Utils.odict()
         
        for child in xmlElement:
            reference_entity = EntityRef(child.tag)
            reference_entity.setSource(child.tag, 'PMIM')
            reference_entity.setEntity(child.text , 'TECHPACK_VERSION')
            dependency[child.tag] = reference_entity
            
        model.addComponent('Dependencies', dependency)
 
        return model
    
    def parse_tables(self, xmlElement, model):
        tables = model.getComponent('Tables')
        if tables is None:
            tables = Utils.odict()
        
        for child in xmlElement:
            tablename = child.get('name')
            table_entity = EntityDef(tablename)
            table_entity.addProperty('tableType', child.get('tableType'))
            table_entity.addProperty('universeClass', child.get('universeClass'))  
                    
            for innerchild in child:
                if innerchild.tag == 'Attributes':
                    table_entity = self.parse_attributes(innerchild, table_entity)
                elif innerchild.tag == 'Parsers':
                    pass
                    model = self.parse_parsers(innerchild, model)
                elif innerchild.tag != 'Attributes' and innerchild.tag != 'Parsers':
                    table_entity.addProperty(innerchild.tag, innerchild.text)
         
            tables[tablename] = table_entity
            
        model.addComponent('Tables', tables)
 
        return model
    
    def parse_attributes(self, xmlElement, model):
        attributes = model.getComponent('Attributes')
        if attributes is None:
            attributes = Utils.odict()
        
        for child in xmlElement:
            attname = child.get('name')
            attr_entity = EntityDef(attname)
            attr_entity.addProperty('attributeType', child.get('attributeType'))
            
            for innerchild in child:
                if innerchild.tag == 'Vectors':
                    attr_entity = self.parse_vectors(innerchild, attr_entity)
                else:
                    attr_entity.addProperty(innerchild.tag, innerchild.text)
         
            attributes[attname] = attr_entity
            
        model.addComponent('Attributes', attributes)
 
        return model
    
    def parse_vectors(self, xmlElement, model):
        vectors = model.getComponent('VectorReleases')
        if vectors is None:
            vectors = Utils.odict()
        
        for child in xmlElement:
            VendorRelease = child.get('VendorRelease')
            
            vendor_entity = None
            if VendorRelease in vectors:
                vendor_entity = vectors[VendorRelease]
            else:
                vendor_entity = EntityDef(VendorRelease)
            
            vector_entity = self.parse_vector(child, vendor_entity)
             
            vectors[VendorRelease] = vector_entity
        
        if len(vectors) > 0:
            model.addComponent('VectorReleases', vectors)
 
        return model
    
    def parse_vector(self, xmlElement, model):
        vectors = model.getComponent('Vectors')
        if vectors is None:
            vectors = Utils.odict()
        
        index = xmlElement.get('index')
        vector_entity = EntityDef(index)
        
        for child in xmlElement:
            vector_entity.addProperty(child.tag, child.text)
        
        vectors[index] = vector_entity
        model.addComponent('Vectors', vectors)
        
        return model       

    def parse_parsers(self, xmlElement, model):
        parser = model.getComponent('ETL')
        if parser is None:
            parser = Utils.odict()
        
        for child in xmlElement:
            attname = child.get('type')
            
            parser_entity = None
            if attname in parser:
                parser_entity = parser[attname]
            else:
                parser_entity = EntityDef(attname)
             
            dataformatid = child.find('Dataformat').get('DataFormatID')
            tablename = dataformatid.split(':')[2]
              
            tables = parser_entity.getComponent('Tables')
            if tables is None:
                tables = Utils.odict()
                  
            table_entity = EntityDef(tablename)
                  
            for innerchild in child:
                if innerchild.tag == 'Dataformat':
                    table_entity = self.parse_dataformat(innerchild, table_entity)
                elif innerchild.tag == 'Transformations':
                    table_entity = self.parse_transformations(innerchild, table_entity)
              
            tables[tablename] = table_entity
            parser_entity.addComponent('Tables', tables)
            parser[attname] = parser_entity
            
        model.addComponent('ETL', parser)
 
        return model
    
    def parse_dataformat(self, xmlElement, model):
        tabletags = model.getComponent('TableTags')
        if tabletags is None:
            tabletags = Utils.odict()

        for child in xmlElement:
            if child.tag == 'TableTags':
                for innerchild in child:
                    refname = innerchild.text
                    sourcename = refname
                    if sourcename.endswith('_V') or sourcename.endswith('_FLEX'):
                        sourcename = sourcename.rsplit('_', 1)[0]
                    
                    reference_entity = EntityRef(refname)
                    reference_entity.setSource(sourcename, 'Node')
                    reference_entity.setEntity(sourcename , 'Classes')
                    tabletags[refname] = reference_entity
                 
            elif child.tag == 'attributeTags':
                for innerchild in child:
                    model.addProperty(innerchild.tag, innerchild.text)

        model.addComponent('TableTags', tabletags)
 
        return model

    def parse_transformations(self, xmlElement, model):
        transformation = model.getComponent('Transformations')
        if transformation is None:
            transformation = Utils.odict()
        
        for child in xmlElement:
            attname = child.get('index')
            trans_entity = EntityDef(attname)
            
            for innerchild in child:
                trans_entity.addProperty(innerchild.tag, innerchild.text)
             
            transformation[attname] = trans_entity
        model.addComponent('Transformations', transformation)
 
        return model

    def parse_externalstmts(self, xmlElement, model):
        statements = model.getComponent('ExternalStatements')
        if statements is None:
            statements = Utils.odict()

        for child in xmlElement:
            esName = child.get('name')
            stmt_entity = EntityDef(esName)
        
            for innerchild in child:
                stmt_entity.addProperty(innerchild.tag, innerchild.text)
                
            statements[esName] = stmt_entity
        model.addComponent('ExternalStatements', statements)
        
        return model
    
    def parse_busyhours(self, xmlElement, model):
        busyhours = model.getComponent('BusyHours')
        if busyhours is None:
            busyhours = Utils.odict()
        
        for child in xmlElement:
            bhName = child.get('name')
            bh_entity = EntityDef(bhName)
            
            for innerchild in child:
                if innerchild.tag == 'BusyHourSupportedTables':
                    bh_entity = self.parse_busyhourtables(innerchild, bh_entity, model)
                elif innerchild.tag == 'BusyHourTypes':
                    bh_entity = self.parse_busyhourtypes(innerchild, bh_entity)
                
            busyhours[bhName] = bh_entity
        model.addComponent('BusyHours', busyhours)
        
        return model
    
    def parse_busyhourtables(self, xmlElement, model, fullmodel):
        bhtables = model.getComponent('SupportedTables')
        if bhtables is None:
            bhtables = Utils.odict()
    
        for child in xmlElement:
            refname = child.text
            reference_entity = EntityRef(refname)
            reference_entity.setSource(fullmodel.getName(), 'TP')
            reference_entity.setEntity(refname , 'Tables')
                    
            bhtables[refname] = reference_entity
        model.addComponent('SupportedTables', bhtables)
        
        return model
    
    def parse_busyhourtypes(self, xmlElement, model):
        placeholders = model.getComponent('Placeholders')
        if placeholders is None:
            placeholders = Utils.odict()

        for child in xmlElement:
            phname = child.get('name')
            placeholder = EntityDef(phname)
            
            for innerchild in child:
                if innerchild.tag == 'BusyHourSourceTables':
                    placeholder = self.parse_bhsupportedTables(innerchild, placeholder)
                elif innerchild.tag == 'BusyHourRankKeys':
                    placeholder = self.parse_bhrankkeys(innerchild, placeholder)
                elif innerchild.tag != 'BusyHourRankKeys' and innerchild.tag != 'BusyHourSourceTables':
                    placeholder.addProperty(innerchild.tag, innerchild.text)
            
            if placeholder.getProperty('ENABLE') == '1':     
                placeholders[phname] = placeholder
        model.addComponent('Placeholders', placeholders)
        
        return model
    
    def parse_bhrankkeys(self, xmlElement, model):
        busyHour = model.getComponent('RankKeys')
        if busyHour is None:
            busyHour = Utils.odict()
        
        bhName = 'RankKeys'
        bh_entity = EntityDef(bhName)
        
        for child in xmlElement:
            bh_entity.addProperty(child.tag, child.text)
                    
        busyHour[bhName] = bh_entity
        model.addComponent('RankKeys', busyHour)
        
        return model
    
    def parse_bhsupportedTables(self, xmlElement, model):
        busyHour = model.getComponent('SupportedTables')
        if busyHour is None:
            busyHour = Utils.odict()
        
        bhName = 'SupportedTables'
        bh_entity = EntityDef(bhName)
        
        for child in xmlElement:
            bh_entity.addProperty(child.text, '')
                    
        if len(bh_entity.properties) > 0:
            busyHour[bhName] = bh_entity
            model.addComponent('SupportedTables', busyHour)
        
        return model
        
    
#     def parse_interfaces(self, xmlElement, model):
#         interfaces = model.getComponent('Interfaces')
#         if interfaces is None:
#             interfaces = Utils.odict()
#         
#         tpName = 'interfaces'
#         intf_entity = EntityDef(tpName)
#         
#         searchTags = ['Interface']
#         for child in xmlElement:
#             if child.tag in searchTags:
#                 intf_entity = self.parse_interface(child, intf_entity)
#                 
#         interfaces[tpName] = intf_entity
#         model.addComponent('Interfaces', interfaces)
#         
#         return model
#     
#     def parse_interface(self, xmlElement, model):
#         interface = model.getComponent('Interface')
#         if interface is None:
#             interface = Utils.odict()
#         
#         intfName = xmlElement.get('name')
#         interface_entity = EntityDef(intfName)
#         interface_entity.addProperty('name', xmlElement.get('name'))
#         
#         searchTags = ['IntfVersioning' ,'Dependencies', 'Techpacks', 'Configuration']
#         for child in xmlElement:
#             if child.tag in searchTags:
#                 if child.tag == 'IntfVersioning':
#                     interface_entity = self.parse_intfversioning(child, interface_entity)
#                 elif child.tag == 'Dependencies':
#                     interface_entity = self.parse_intfdependencies(child, interface_entity)
#                 elif child.tag == 'Techpacks':
#                     interface_entity = self.parse_intftechpack(child, interface_entity)
#                 elif child.tag == 'Configuration':
#                     interface_entity = self.parse_configuration(child, interface_entity)
#                     
#         interface[intfName] = interface_entity
#         model.addComponent('Interface', interface)
#         
#         return model
#     
#     def parse_intfversioning(self, xmlElement, model):
#         intfVersion = model.getComponent('IntfVersioning')
#         if intfVersion is None:
#             intfVersion = Utils.odict()
#         
#         intfName = xmlElement.get('intfVersion')
#         intfVersion_entity = EntityDef(intfName)
#         intfVersion_entity.addProperty('intfVersion', xmlElement.get('intfVersion'))
#         
#         searchTags = ['DATAFORMATTYPE' ,'DESCRIPTION', 'ELEMTYPE', 'INTERFACETYPE', 'RSTATE']
#         for child in xmlElement:
#             if child.tag in searchTags:
#                 strValue = xmlElement.find(child.tag).text
#                 if strValue is not None:
#                     intfVersion_entity.addProperty(child.tag, strValue.strip())
#                     
#         intfVersion[intfName] = intfVersion_entity
#         model.addComponent('IntfVersioning', intfVersion)
#         
#         return model
#     
#     def parse_intfdependencies(self, xmlElement, model):
#         dependencies = model.getComponent('Dependencies')
#         if dependencies is None:
#             dependencies = Utils.odict()
#         
#         dName = 'dependencies'
#         dependence_entity = EntityDef(dName)
#         dependence_entity.addProperty('intfVersion', xmlElement.get('intfVersion'))
#         
#         searchTags = ['DC_E_CPP' ,'DC_E_ERBS']
#         for child in xmlElement:
#             if child.tag in searchTags:
#                 strValue = xmlElement.find(child.tag).text
#                 if strValue is not None:
#                     dependence_entity.addProperty(child.tag, strValue.strip())
#                     
#         dependencies[dName] = dependence_entity
#         model.addComponent('Dependencies', dependencies)
#         
#         return model
#     
#     def parse_intftechpack(self, xmlElement, model):
#         intfTechpack = model.getComponent('Techpacks')
#         if intfTechpack is None:
#             intfTechpack = Utils.odict()
#         
#         intfName = 'interfaceTechpack'
#         intfTP_entity = EntityDef(intfName)
#         
#         searchTags = ['DC_E_CPP' ,'DC_E_ERBS']
#         for child in xmlElement:
#             if child.tag in searchTags:
#                 strValue = xmlElement.find(child.tag).text
#                 if strValue is not None:
#                     intfTP_entity.addProperty(child.tag, strValue.strip())
#                     
#         intfTechpack[intfName] = intfTP_entity
#         model.addComponent('Techpacks', intfTechpack)
#         
#         return model
#     
#     def parse_configuration(self, xmlElement, model):
#         configuration = model.getComponent('Configuration')
#         if configuration is None:
#             configuration = Utils.odict()
#         
#         config = 'configuration'
#         config_entity = EntityDef(config)
#         
#         searchTags = ['AS_Interval' ,'AS_SchBaseTime', 'MDCParser.HashData', 'MDCParser.UseVector',
#                       'MDCParser.createOwnFlexFile', 'MDCParser.createOwnVectorFile', 'MDCParser.hasFlexCounters',
#                       'MDCParser.readVendorIDFrom', 'MDCParser.vendorIDMask', 'ProcessedFiles.fileNameFormat', 
#                       'ProcessedFiles.processedDir', 'afterParseAction', 'archivePeriod', 'baseDir', 'dirThreshold',
#                       'doubleCheckAction', 'dublicateCheck', 'failedAction', 'inDir', 'interfaceName', 'loaderDir',
#                       'maxFilesPerRun', 'minFileAge', 'outDir', 'parserType', 'thresholdMethod', 'useZip', 'workers']
#         for child in xmlElement:
#             if child.tag in searchTags:
#                 strValue = xmlElement.find(child.tag).text
#                 if strValue is not None:
#                     config_entity.addProperty(child.tag, strValue.strip())
#                     
#         configuration[config] = config_entity
#         model.addComponent('Configuration', configuration)
#         
#         return model
    