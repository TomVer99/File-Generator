from datetime import datetime
import xml.dom.minidom
import src.CPPGenerator as cpp_gen
import os
import re

def generate_files_based_on_xml(xml_file):
    # setup
    tree = xml.dom.minidom.parse(xml_file)
    root = tree.documentElement

    # project info
    date = datetime.now().strftime("%Y-%m-%d")
    author_name = root.getElementsByTagName('author')[0].getAttribute('name')
    namespace = root.getElementsByTagName('namespace')[0].getAttribute('name')

    # get comment_block settings
    settings = xml.dom.minidom.parse('./src/gen.settings.xml')
    settings_root = settings.documentElement
    comment_blocks = settings_root.getElementsByTagName('comment_blocks')[0]
    comment_block_width = int(comment_blocks.getElementsByTagName('width')[0].childNodes[0].nodeValue)
    comment_block_height = int(comment_blocks.getElementsByTagName('height')[0].childNodes[0].nodeValue)
    comment_block_end_of_file_height = int(comment_blocks.getElementsByTagName('end_of_file_height')[0].childNodes[0].nodeValue)
    
    # get export location
    export_location = root.getElementsByTagName('export_location')[0].childNodes[0].nodeValue
    if re.match(export_location, "./src/+"):
        export_location = export_location.replace("./src/", "./src2/")
        print('\033[91m' + "Export location intruded on src folder, changed to: " + export_location + '\033[0m')

    # get files to be generated
    files = root.getElementsByTagName('file')

    print('\033[93m' + "Exporting " + str(len(files)) + " files to: " + export_location + '\033[0m')

    source_files_type = root.getAttribute('type')
    match source_files_type:
        case "cpp":
            for index, file in enumerate(files):
                print('\033[93m' + '\t' + "Generating file " + str(index + 1) + "..." + '\033[0m')
                generate_cpp_files(export_location,
                                    author_name,
                                    date,
                                    file,
                                    namespace,
                                    comment_block_width,
                                    comment_block_height,
                                    comment_block_end_of_file_height)

def generate_cpp_files(location,
                        author_name,
                        date,
                        file,
                        namespace,
                        comment_block_width,
                        comment_block_height,
                        comment_block_end_of_file_height):
    cpp_gen.generate_cpp_class_file(location,
                                    author_name,
                                    date,
                                    file.getAttribute('name'),
                                    namespace,
                                    file.getElementsByTagName('class'),
                                    comment_block_width,
                                    comment_block_height,
                                    comment_block_end_of_file_height)

    cpp_gen.generate_hpp_class_file(location,
                                    author_name,
                                    date,
                                    file.getAttribute('name'),
                                    namespace,
                                    file.getElementsByTagName('class'),
                                    comment_block_width,
                                    comment_block_height,
                                    comment_block_end_of_file_height)

if __name__ == '__main__':
    # get current working directory
    cwd = os.getcwd()

    # get the xml files
    valid_files_count = 0
    valid_files = []
    print("--------------------------------------------------------------------------------")
    print('\033[93m' + "Scanning for files..." + '\033[0m')
    print('\033[93m' + str(len(os.listdir(cwd)) - 1), "files/folders found" + '\033[0m')
    for file in os.listdir(cwd):
        if re.match("gen.source.+.xml", file) or re.match("gen.source.xml", file):
            valid_files_count += 1
            valid_files.append(file)
            print('\033[92m' + "\tCorrectly named file found: " + file + '\033[0m')

    if valid_files_count == 0:
        print('\033[91m' + "No xml files found with a valid name" + '\033[0m')
    else:
        print('\033[92m' + str(valid_files_count) + " Correctly named files found\n" + '\033[0m')

    for file in valid_files:
        print('\033[93m' + "Generating files based on " + file + "..." + '\033[0m')
        generate_files_based_on_xml(file)
        print('\033[92m' + "Done!\n" + '\033[0m')
    print("--------------------------------------------------------------------------------")
