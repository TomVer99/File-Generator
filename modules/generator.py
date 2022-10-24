import modules.cpp.generator as cpp

import datetime
import xml.dom.minidom

def generate_files(export_dir, xml_file, type, settings):

    xml_tree = xml.dom.minidom.parse(xml_file)
    xml_root = xml_tree.documentElement

    settings = xml.dom.minidom.parse(settings)
    settings = settings.documentElement

    comment_blocks_settings = settings.getElementsByTagName('comment_blocks')[0]

    comment_block_width = int(comment_blocks_settings.getElementsByTagName('width')[0].childNodes[0].nodeValue)
    comment_block_height = int(comment_blocks_settings.getElementsByTagName('height')[0].childNodes[0].nodeValue)
    comment_block_end_of_file_height = int(comment_blocks_settings.getElementsByTagName('end_of_file_height')[0].childNodes[0].nodeValue)

    date = datetime.datetime.now().strftime("%Y-%m-%d")

# +----------------------------------------------------------------------+
# |                                                                      |
# |                     Add supported languages here                     |
# |                                                                      |
# +----------------------------------------------------------------------+

    # cpp
    if type in cpp.get_types():
        return cpp.generate_files(export_dir, xml_root, type, date, comment_block_width, comment_block_height, comment_block_end_of_file_height)

# +----------------------------------------------------------------------+
# |                                                                      |
# |                       End supported languages                        |
# |                                                                      |
# +----------------------------------------------------------------------+
