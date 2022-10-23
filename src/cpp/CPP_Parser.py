from enum import Enum
import xmlschema
import os

class cpp_types(Enum):
    CPP_WITH_CLASS = 1
    CPP_WITHOUT_CLASS = 2

def parse_xml_file(file, type:cpp_types):
    xml_schema = None
    match type:
        case cpp_types.CPP_WITH_CLASS:
            xml_schema = './gen.settings.cpp.class.xsd'
        case cpp_types.CPP_WITHOUT_CLASS:
            xml_schema ='./gen.settings.cpp.func.xsd'
    
    # get absolute path to xml schema
    xml_schema = os.path.join(os.path.dirname(__file__), xml_schema)

    xml_schema = xmlschema.XMLSchema(xml_schema)
    
    if xml_schema.is_valid(file):
        return True
    else:
        return False
