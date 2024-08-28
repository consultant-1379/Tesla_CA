'''
Created on Oct 12, 2017

@author: ebrifol
'''

from XML import XML_Parser
from Model import EntityDef, EntityRef
import Utilities as Utils


class ECIM_Parser(XML_Parser):
    '''
    This parser should be used to parse ECIM based node inputs
    '''
    Tags_To_Parse = {'mim' : 'parse_mim', 'class' : 'parse_class', 'struct' : 'parse_struct', 'enum' : 'parse_enum'}
    Tags_for_Reference = {'enumRef' : 'Enums', 'moRef' : 'Classes', 'structRef' : 'Structs'}
    Tags_for_datatypes = {'long', 'string', 'longlong'}
    
    
    def __init__(self, params):
        super(self.__class__, self).__init__(params, self)
        self.params = params
    
    def parse_mim(self, xmlElement, model):
        model.setName(xmlElement.get('name'))

        model.addProperty('Revision', xmlElement.get('revision'))
        model.addProperty('Version', xmlElement.get('version'))
        model.addProperty('Release', xmlElement.get('release'))
        model.addProperty('Date', xmlElement.get('date'))
        
        #Get the applicationTag
        model.addProperty('ApplicationTag', xmlElement.find('.//applicationTag').text)
        
        return model
    
    def parse_class(self, xmlElement, model):
        classes = model.getComponent('Classes')
        if classes is None:
            classes = Utils.odict()
        
        classname = xmlElement.get('name')
        class_entity = EntityDef(classname)
        
        searchTags = ['description' ,'deprecated', 'SystemCreated', 'attribute']
        for child in xmlElement:
            if child.tag in searchTags:
                if child.tag != 'attribute':
                    class_entity.addProperty(child.tag, xmlElement.find(child.tag).text.strip())
                else:
                    class_entity = self.parse_attribute(child, class_entity, model)
                    
        classes[classname] = class_entity
        model.addComponent('Classes', classes)
        
        return model
    
    def parse_attribute(self, xmlElement, model, fullmodel):
        attributes = model.getComponent('Attributes')
        if attributes is None:
            attributes = Utils.odict()
            
        attname = xmlElement.get('name')
        att_entity = EntityDef(attname)
        
        for child in xmlElement:
            if child.tag != 'dataType':
                att_entity.addProperty(child.tag, child.text)
            else:
                for child in xmlElement:
                    if child.tag == 'sequence':           
                        att_entity = self.parse_datatype_variants(child, att_entity, fullmodel)
                    else:
                        att_entity = self.parse_datatype_variants(xmlElement, att_entity, fullmodel)
        
        attributes[attname] = att_entity
        model.addComponent('Attributes', attributes)
        
        return model
    
    def parse_enum(self, xmlElement, model):
        enums = model.getComponent('Enums')
        if enums is None:
            enums = Utils.odict()
        
        enumName = xmlElement.get('name')
        enum_entity = EntityDef(enumName)
        
        for child in xmlElement:
            if child.tag == 'enumMember':
                enum_entity = self.parse_enumMember(child, enum_entity)
            else:
                enum_entity.addProperty(child.tag, child.text)
        
        enums[enumName] = enum_entity
        model.addComponent('Enums', enums)
        return model
    
    def parse_enumMember(self, xmlElement, model):
        members = model.getComponent('EnumMembers')
        if members is None:
            members = Utils.odict()
        
        enumMemberName = xmlElement.get('name')
        enumMember_entity = EntityDef(enumMemberName)
        
        for child in xmlElement:
            enumMember_entity.addProperty(child.tag, child.text)

        members[enumMemberName] = enumMember_entity
        model.addComponent('EnumMembers', members)
        return model
    
    def parse_struct(self, xmlElement, model):
        structs = model.getComponent('Structs')
        if structs is None:
            structs = Utils.odict()
        
        structName = xmlElement.get('name')
        structName_entity = EntityDef(structName)
        
        for child in xmlElement:
            if child.tag == 'structMember':
                structName_entity = self.parse_structMembers(child, structName_entity, model)
            else:
                structName_entity.addProperty(child.tag, child.text)
        
        structs[structName] = structName_entity
        model.addComponent('Structs', structs)
        return model
    
    def parse_structMembers(self, xmlElement, model, fullmodel):
        structs = model.getComponent('StructMembers')
        if structs is None:
            structs = Utils.odict()
        
        structname = xmlElement.get('name')
        struct_entity = EntityDef(structname)
        
        sequence = xmlElement.find('sequence')
        if sequence is None:
            struct_entity = self.parse_datatype_variants(xmlElement, struct_entity, fullmodel)
        else:
            struct_entity = self.parse_datatype_variants(sequence, struct_entity, fullmodel)
 
        structs[structname] = struct_entity
        model.addComponent('StructMembers', structs)
        return model
    
    def parse_datatype_variants(self, xmlElement, model, fullmodel):
        for child in xmlElement:
            if child.tag in self.Tags_for_Reference:
                model = self.parse_reference(child, model, fullmodel)
            
            if child.tag in self.Tags_for_datatypes:
                model = self.parse_datatype(child, model, xmlElement.tag)                
            
            if child.tag not in self.Tags_for_Reference and child.tag not in self.Tags_for_datatypes:
                model.addProperty(child.tag, child.text)
                for innerchild in child:
                    model.addProperty(innerchild.tag, innerchild.text)
                
        return model
    
    def parse_reference(self, xmlElement, model, fullmodel):
        refname = xmlElement.get('name')
        reference_entity = EntityRef(refname)
        reference_entity.setSource(fullmodel.getName(), 'Node')
        reference_entity.setEntity(refname , self.Tags_for_Reference[xmlElement.tag])
        
        reference = Utils.odict()
        reference[refname] = reference_entity
        model.addComponent('EntityRef', reference)
        
        return model
    
    def parse_datatype(self, xmlElement, model, parentTag=''):
        data_type = xmlElement.tag
        datatype_entity = EntityDef(data_type)
        
        for child in xmlElement:
            if child.tag == 'range':
                range_entity = EntityDef('Range')
                for innerchild in child: 
                    range_entity.addProperty(innerchild.tag, innerchild.text)
                
                rangeDict = Utils.odict()
                rangeDict['Range'] = range_entity   
                
                datatype_entity.addComponent('Ranges', rangeDict)
            
            else:
                datatype_entity.addProperty(child.tag, child.text)
        
        if parentTag == 'sequence':
            datatype_entity.addProperty(parentTag, '')
        
        datatype = Utils.odict()
        datatype[data_type] = datatype_entity
        
        model.addComponent('DataType', datatype)
        return model
        
        
        
        
        
        