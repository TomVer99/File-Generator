import cpp.CPP_Parser as cpp_parser
import xml.dom.minidom
import GeneratorLogging as GL

import os

def parse_xml_file(file):
    xml_file = xml.dom.minidom.parse(file)
    try:
        root = xml_file.documentElement
    except:
        return False
    else:
        if root.hasAttribute('type'):
            type = root.getAttribute('type')

    result = False

    match type:
        case 'cpp_class':
            result = cpp_parser.parse_xml_file(file, cpp_parser.cpp_types.CPP_WITH_CLASS)
        case 'cpp_func':
            result = cpp_parser.parse_xml_file(file, cpp_parser.cpp_types.CPP_WITHOUT_CLASS)
        case _:
            result = [False, 'Unknown type']

    if result:
        GL.print_to_console('xml file is valid', GL.Color.SUCCESS)
    else:
        GL.print_to_console('xml file is not valid', GL.Color.FAIL)

# TODO: remove this
if __name__ == "__main__":
    parse_xml_file(os.path.join(os.path.dirname(__file__), "..", "gen.source.new.version.xml"))
