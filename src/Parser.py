import cpp.parser as parser
import xml.dom.minidom
import GeneratorLogging as GL
import xmlschema
import os

parsers_location:str = '.'

def __parse_xml_file_language(file):
    xml_file = xml.dom.minidom.parse(file)
    try:
        root = xml_file.documentElement
    except:
        return [False, '']
    else:
        if root.hasAttribute('type'):
            type = root.getAttribute('type')
            return [True, type]
        else:
            return [False, '']

def parse_xml_file(file):
    """
    Takes absolute path to xml file\n
    returns [bool, type]\n
    [ if file is valid (true = valid), language type ]
    """

    valid_base_file = __parse_xml_file_language(file)

    xml_schema = None

    if valid_base_file[0]:

        # cpp
        if xml_schema == None: # supported language not yet detected
            xml_schema = parser.parse_language(valid_base_file[1])
        
        # c
        # TODO

        if xml_schema == None: # no supported language was detected
            GL.log_error('Language not supported: ' + valid_base_file[1])
            return [False, '']
    else:
        GL.log_error('Invalid xml file: ' + file)
        return [False, '']

    # get absolute path to xml schema
    xml_schema = parsers_location + xml_schema
    xml_schema = os.path.join(os.path.dirname(__file__), xml_schema)

    xml_schema = xmlschema.XMLSchema(xml_schema)

    if xml_schema.is_valid(file):
        GL.log_success('Valid ' + valid_base_file[1] + ' xml file: ' + file)
        return [True, valid_base_file[1]]
    else:
        GL.log_error('Invalid ' + valid_base_file[1] + ' xml file: ' + file)
        return [False, '']

# TODO: remove this
if __name__ == "__main__":
    result = parse_xml_file(os.path.join(os.path.dirname(__file__), "..", "gen.source.new.version.xml"))

    if result[0]:
        GL.log_notify('Language: ' + result[1])
