import modules.cpp.__shared as shared

import os

import modules.comment_block_generator as CBG
import modules.doxygen_generator as DG

# +----------------------------------------------------------------------+
# |                                                                      |
# |                              Universal                               |
# |                                                                      |
# +----------------------------------------------------------------------+

__comment_type = '//'
__source_file_extension = '.cpp'
__source_file_name = 'C++'
__header_file_extension = '.hpp'
__header_file_name = 'H++'

# +----------------------------------------------------------------------+

def __write_file_intro(file, file_name, is_source,
                        date, author_name, comment_block_width,
                        comment_block_height):
    CB_name = None

    if is_source:
        CB_name = __source_file_name + ' File'
    else:
        CB_name = __header_file_name + ' File'

    CBG.write_comment_block(file, CB_name, comment_block_width, comment_block_height, __comment_type)

    DG.cpp_write_doc_file_header(file, file_name, author_name, date)

# +----------------------------------------------------------------------+

def __write_include_guard(file, file_name, is_open):
    if is_open:
        file.write(f"#ifndef {file_name.upper()}_HPP\n")
        file.write(f"#define {file_name.upper()}_HPP\n\n")
    else:
        file.write(f"#endif // {file_name.upper()}_HPP\n\n")

# +----------------------------------------------------------------------+

def __write_namespace(file, namespace, is_open):
    namespace = namespace.upper()
    if is_open:
        file.write(f"namespace {namespace}\n{{\n\n")
    else:
        file.write(f"}} // namespace {namespace}\n\n")

# +----------------------------------------------------------------------+

def __write_include(file, include, local):
    if local:
        file.write(f"#include \"{include}\"\n")
    else:
        file.write(f"#include <{include}>\n")

# +----------------------------------------------------------------------+
# |                                                                      |
# |                        Generation with class                         |
# |                                                                      |
# +----------------------------------------------------------------------+

def __write_method(file, method_root, class_name, is_source, is_destructor = False):
    method_name = None
    if method_root.hasAttribute("name"):
        method_name = method_root.getAttribute("name")
    elif is_destructor:
        method_name = '~' + class_name
    else:
        method_name = class_name

    method_return_type = None
    try:
        method_return_type = method_root.getElementsByTagName('return')[0].childNodes[0].nodeValue
    except:
        method_return_type = ""

    method_parameters = None
    try:
        method_parameters = method_root.getElementsByTagName('parameter')
    except:
        method_parameters = None

    if not is_source:
        DG.cpp_write_doc_method(file, method_return_type, method_parameters)

    if method_return_type == "":
        file.write(f"{class_name}::{method_name}(")
    else:
        file.write(f"{method_return_type} {class_name}::{method_name}(")

    if len(method_parameters) == 0:
        file.write(")")

    for parameter in method_parameters:
        param_type = parameter.getElementsByTagName('type')[0].childNodes[0].nodeValue
        param_name = parameter.getElementsByTagName('name')[0].childNodes[0].nodeValue
        
        if len(method_parameters) == 1:
            file.write(f"{param_type} {param_name})")

        else:
            if parameter == method_parameters[0]:               # first parameter
                file.write(f"{param_type} {param_name},\n")

            elif parameter == method_parameters[-1]:            # last parameter
                file.write(" " * ((len(method_return_type) + len(class_name) + len(method_name)) + 4))
                file.write(f"{param_type} {param_name})")

            else:                                               # other parameter
                file.write(" " * ((len(method_return_type) + len(class_name) + len(method_name)) + 4))
                file.write(f"{param_type} {param_name},\n")

    if is_source:
        file.write("\n{\n")
        file.write("    // TODO: Implement\n")
        if method_return_type != "" and method_return_type != "void":
            file.write(f"    {method_return_type} dummy;\n")
            file.write("    return dummy;\n")
        file.write("}\n\n")
    else:
        file.write(";\n\n")

# +----------------------------------------------------------------------+

def __generate_class(file, class_root, class_name, is_source):
    if not is_source:
        file.write(f"class {class_name}\n{{\n")
        file.write("private:\n\n")
        file.write("public:\n\n")

    constructor = class_root.getElementsByTagName("constructor")[0]
    destructor = class_root.getElementsByTagName("destructor")[0]
    methods = class_root.getElementsByTagName("method")

    __write_method(file, constructor, class_name, is_source)
    __write_method(file, destructor, class_name, is_source, True)

    for method in methods:
        __write_method(file, method, class_name, is_source)

    if not is_source:
        file.write(f"}}; // class {class_name}\n\n")

# +----------------------------------------------------------------------+

def __generate_source_file_with_class(file, file_root, author_name, 
                                        namespace_name, date, file_name,
                                        comment_block_width, comment_block_height, comment_block_end_of_file_height):
    file_name_with_extension = file_name + __source_file_extension
    __write_file_intro(file, file_name_with_extension, True, date, author_name, comment_block_width, comment_block_height)

    CBG.write_comment_block(file, 'Own Includes', comment_block_width, comment_block_height, __comment_type)
    __write_include(file, file_name + __header_file_extension, True)
    CBG.write_comment_block(file, 'System Includes', comment_block_width, comment_block_height, __comment_type)
    __write_namespace(file, namespace_name, True)
    CBG.write_comment_block(file, 'Local constants / Defines', comment_block_width, comment_block_height, __comment_type)
    CBG.write_comment_block(file, file_name + ' Class Methods', comment_block_width, comment_block_height, __comment_type)

    class_root = file_root.getElementsByTagName("class")[0]
    __generate_class(file, class_root, file_name, True)

    __write_namespace(file, namespace_name, False)
    CBG.write_comment_block(file, 'End of File', comment_block_width, comment_block_end_of_file_height, __comment_type, True, True)

# +----------------------------------------------------------------------+

def __generate_header_file_with_class(file, file_root, author_name, 
                                        namespace_name, date, file_name,
                                        comment_block_width, comment_block_height, comment_block_end_of_file_height):
    file_name_with_extension = file_name + __header_file_extension
    __write_file_intro(file, file_name_with_extension, False, date, author_name, comment_block_width, comment_block_height)

    __write_include_guard(file, file_name, True)

    CBG.write_comment_block(file, 'Own Includes', comment_block_width, comment_block_height, __comment_type)
    CBG.write_comment_block(file, 'System Includes', comment_block_width, comment_block_height, __comment_type)
    __write_namespace(file, namespace_name, True)
    CBG.write_comment_block(file, 'Global constants / Defines', comment_block_width, comment_block_height, __comment_type)
    CBG.write_comment_block(file, file_name + ' Class', comment_block_width, comment_block_height, __comment_type)

    class_root = file_root.getElementsByTagName("class")[0]
    __generate_class(file, class_root, file_name, False)

    __write_namespace(file, namespace_name, False)
    __write_include_guard(file, file_name, False)
    CBG.write_comment_block(file, 'End of File', comment_block_width, comment_block_end_of_file_height, __comment_type, True, True)

# +----------------------------------------------------------------------+

def __generate_files_with_class(export_dir, xml_root, author_name, 
                                namespace_name, date, comment_block_width,
                                comment_block_height, comment_block_end_of_file_height):
    for file_element in xml_root.getElementsByTagName("file"):
        file_name = str(file_element.getAttribute('name')).upper().capitalize()
        # +------------------------------------------------------------------------------------------------------------+
        s_file = open(os.path.join(export_dir, file_name + __source_file_extension), 'w')
        __generate_source_file_with_class(s_file, file_element, author_name,
                                            namespace_name, date, file_name,
                                            comment_block_width, comment_block_height, comment_block_end_of_file_height)
        s_file.close()
        # +------------------------------------------------------------------------------------------------------------+
        h_file = open(os.path.join(export_dir, file_name + __header_file_extension), 'w')
        __generate_header_file_with_class(h_file, file_element, author_name,
                                            namespace_name, date, file_name,
                                            comment_block_width, comment_block_height, comment_block_end_of_file_height)
        h_file.close()
        # +------------------------------------------------------------------------------------------------------------+

    return True

# +----------------------------------------------------------------------+
# |                                                                      |
# |                       Generation without class                       |
# |                                                                      |
# +----------------------------------------------------------------------+

def __generate_files_without_class(export_dir, xml_root, author_name, 
                                    namespace_name, date, comment_block_width,
                                    comment_block_height, comment_block_end_of_file_height):
    return False

# +----------------------------------------------------------------------+
# |                                                                      |
# |                                 Main                                 |
# |                                                                      |
# +----------------------------------------------------------------------+

def generate_files(export_dir, xml_root, type,
                    date, comment_block_width, comment_block_height,
                    comment_block_end_of_file_height):

    author_name = xml_root.getElementsByTagName('author')[0].childNodes[0].nodeValue
    namespace_name = xml_root.getElementsByTagName('namespace')[0].childNodes[0].nodeValue

    if type == shared.supported_types[0]:
        return __generate_files_with_class(export_dir, xml_root, author_name,
                                            namespace_name, date, comment_block_width,
                                            comment_block_height, comment_block_end_of_file_height)
    elif type == shared.supported_types[1]:
        return __generate_files_without_class(export_dir, xml_root, author_name,
                                                namespace_name, date, comment_block_width,
                                                comment_block_height, comment_block_end_of_file_height)
    return False

# +----------------------------------------------------------------------+

def get_types():
    return shared.supported_types
