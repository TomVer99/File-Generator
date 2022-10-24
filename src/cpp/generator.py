import os
import cpp.__shared as shared

def generate_file(xml_source, xml_settings, export_location, type):
    """
    Generate a file from a xml source and xml settings file.
    First 2 parameters are file paths.
    Third parameter is a folder path.
    First 3 parameters need to be absolute paths.
    """

    # check if xml_source exists
    if not os.path.exists(xml_source):
        return False

    # check if xml_settings exists
    if not os.path.exists(xml_settings):
        return False

    # check if export_location exists else create it
    if not os.path.exists(export_location):
        os.makedirs(export_location)

    # check if type is supported
    type_supported = False
    for types in shared.supported_types:
        if type == types:
            type_supported = True
            break

    pass
