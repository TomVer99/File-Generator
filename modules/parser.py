import modules.cpp.parser as cpp

import os
import re
import xml.dom.minidom
import xmlschema

# +----------------------------------------------------------------------+

def __scan_for_language_type(file):
    tree = xml.dom.minidom.parse(file)
    root = tree.documentElement

    if root.hasAttribute('type'):
        return root.getAttribute('type')
    else:
        return None

# +----------------------------------------------------------------------+

def __get_element_content(file, element_name, tag=False, tag_name=''):
    """
    Will always pick the first element with the given name.\n
    Returns content of element if found, None otherwise.
    """
    tree = xml.dom.minidom.parse(file)
    root = tree.documentElement

    element = None

    try:
        element = root.getElementsByTagName(element_name)[0]
    except:
        return None

    if tag:
        if element.hasAttribute(tag_name):
            return element.getAttribute(tag_name)
        else:
            return None
    else:
        return element.childNodes[0].nodeValue

# +----------------------------------------------------------------------+

def __parse_export_location(project_dir, file):
    """
    Parse the export location from a source file.\n
    Returns [True, export_location] if successful, [False, error_message] otherwise.
    """
    location = __get_element_content(file, 'export_location')
    location = os.path.abspath(location)

    # if export location is located in project directory return false
    if location.startswith(project_dir):
        return [False, 'Export location intrudes on generator directory']

    # if export location does not exist create it
    if not os.path.exists(location):
        try:
            os.makedirs(location)
        except:
            return [False, 'Could not create export location']

    # if export location exists make sure it is empty
    if os.listdir(location):
        return [False, 'Export location already exists and is not empty. Stopping to prevent data loss.']

    return [True, '']

# +----------------------------------------------------------------------+

def parse_source_file(project_dir, file):
    """
    Parse a source file.\n
    Returns [True, language_type] if successful, [False, error_message] otherwise.
    """

    supported_types = []
    supported_types_xsd = []

# +----------------------------------------------------------------------+
# |                                                                      |
# |                     Add supported languages here                     |
# |                                                                      |
# +----------------------------------------------------------------------+

    # cpp
    supported_types += cpp.get_types()
    supported_types_xsd += cpp.get_xsd()

# +----------------------------------------------------------------------+
# |                                                                      |
# |                       End supported languages                        |
# |                                                                      |
# +----------------------------------------------------------------------+

    language_type = __scan_for_language_type(file)

    for index, type in enumerate(supported_types):
        if language_type == type:
            xsd = supported_types_xsd[index]
            xsd = xmlschema.XMLSchema(xsd)
            if xsd.is_valid(file):
                export_check = __parse_export_location(project_dir, file)
                if export_check[0]:
                    return [True, language_type]
                else:
                    return [False, export_check[1]]
            else:
                return [False, 'File is not valid according to XSD']

    return [False, 'Language type not supported']

# +----------------------------------------------------------------------+

def scan_for_settings_file(dir):
    """
    Scan for gen.settings.xml file and accompanying XSD file.\n
    Returns the absolute file path if found, None otherwise.
    """
    settings_file = os.path.join(dir, 'gen.settings.xml')
    settings_xsd = os.path.join(dir, 'gen.settings.xsd')

    if not os.path.exists(settings_file) or not os.path.exists(settings_xsd):
        return None
    else:
        xsd = xmlschema.XMLSchema(settings_xsd)
        if xsd.is_valid(settings_file):
            return settings_file
        else:
            return None

# +----------------------------------------------------------------------+

def scan_for_source_files(dir):
    """
    Scan for source files.\n
    Returns a list of absolute file paths.
    """
    files = []

    for file in os.listdir(dir):
        if re.match('gen.source.+.xml', file) or re.match('gen.source.xml', file):
            files.append(file)
    
    return files
