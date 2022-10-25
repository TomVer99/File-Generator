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
        file.write(f"#include \"{include}\"\n\n")
    else:
        file.write(f"#include <{include}>\n\n")

# +----------------------------------------------------------------------+

def __write_enum(file, enum_root):
    enum_name = enum_root.getAttribute("name")
    file.write(f"enum {enum_name}\n{{\n")

    members = enum_root.getElementsByTagName("member")

    for member in members:
        member_name = member.getElementsByTagName("name")[0].childNodes[0].nodeValue
        member_value = None
        file.write(f"    {member_name}")
        try:
            member_value = member.getElementsByTagName("value")[0].childNodes[0].nodeValue
            file.write(f" = {member_value}")
        except:
            pass

        # if last member
        if member != members[-1]:
            file.write(",\n")
        else:
            file.write("\n")

    file.write(f"}}; // enum {enum_name}\n\n")

# +----------------------------------------------------------------------+

def __write_struct(file, struct_root):
    struct_name = struct_root.getAttribute("name")
    file.write(f"struct {struct_name}\n{{\n")

    members = struct_root.getElementsByTagName("member")

    for member in members:
        member_type = member.getElementsByTagName("type")[0].childNodes[0].nodeValue
        member_name = member.getElementsByTagName("name")[0].childNodes[0].nodeValue
        file.write(f"    {member_type} {member_name};\n")

    file.write(f"}}; // struct {struct_name}\n\n")

# +----------------------------------------------------------------------+

def __structs_and_enums(file, file_root, is_global):
    wrapper_root = None
    try:
        if is_global:
            wrapper_root = file_root.getElementsByTagName('global')[0]
        else:
            wrapper_root = file_root.getElementsByTagName('local')[0]
    except:
        return
    
    enums = wrapper_root.getElementsByTagName('enum')

    for enum in enums:
        __write_enum(file, enum)

    structs = wrapper_root.getElementsByTagName('struct')

    for struct in structs:
        __write_struct(file, struct)

# +----------------------------------------------------------------------+

def __write_method_or_function(file, element_root, class_name, is_source, is_method, is_destructor = False):
    element_name = None
    if element_root.hasAttribute("name"):
        element_name = element_root.getAttribute("name")
    elif is_destructor:
        element_name = '~' + class_name
    else:
        element_name = class_name

    element_return_type = None
    try:
        element_return_type = element_root.getElementsByTagName('return')[0].childNodes[0].nodeValue
    except:
        element_return_type = ""

    element_parameters = None
    try:
        element_parameters = element_root.getElementsByTagName('parameter')
    except:
        element_parameters = None

    if not is_source:
        if is_method:
            DG.cpp_write_doc_method(file, element_return_type, element_parameters)
        else:
            DG.cpp_write_doc_function(file, element_return_type, element_parameters)

    spacer = 2

    if is_method:
        spacer += len(class_name) + 2
        if element_return_type == "":
            file.write(f"{class_name}::{element_name}(")
        else:
            file.write(f"{element_return_type} {class_name}::{element_name}(")
    else:
        file.write(f"{element_return_type} {element_name}(")

    if len(element_parameters) == 0:
        file.write(")")

    for parameter in element_parameters:
        param_type = parameter.getElementsByTagName('type')[0].childNodes[0].nodeValue
        param_name = parameter.getElementsByTagName('name')[0].childNodes[0].nodeValue
        
        if len(element_parameters) == 1:
            file.write(f"{param_type} {param_name})")

        else:
            if parameter == element_parameters[0]:               # first parameter
                file.write(f"{param_type} {param_name},\n")

            elif parameter == element_parameters[-1]:            # last parameter
                file.write(" " * ((len(element_return_type) + len(element_name)) + spacer))
                file.write(f"{param_type} {param_name})")

            else:                                               # other parameter
                file.write(" " * ((len(element_return_type) + len(element_name)) + spacer))
                file.write(f"{param_type} {param_name},\n")

    if is_source:
        file.write("\n{\n")
        file.write("    // TODO: Implement\n")
        if element_return_type != "" and element_return_type != "void":
            file.write(f"    {element_return_type} dummy;\n")
            file.write("    return dummy;\n")
        file.write("}\n\n")
    else:
        file.write(";\n\n")

# +----------------------------------------------------------------------+

def __generate_header_file(file, file_root, author_name, 
                                        namespace_name, date, file_name,
                                        comment_block_width, comment_block_height, comment_block_end_of_file_height,
                                        has_class):
    file_name_with_extension = file_name + __header_file_extension
    __write_file_intro(file, file_name_with_extension, False, date, author_name, comment_block_width, comment_block_height)

    __write_include_guard(file, file_name, True)

    CBG.write_comment_block(file, 'Own Includes', comment_block_width, comment_block_height, __comment_type)
    CBG.write_comment_block(file, 'System Includes', comment_block_width, comment_block_height, __comment_type)
    __write_namespace(file, namespace_name, True)
    CBG.write_comment_block(file, 'Global constants / Defines', comment_block_width, comment_block_height, __comment_type)
    __structs_and_enums(file, file_root, True)

    if has_class:
        CBG.write_comment_block(file, file_name + ' Class', comment_block_width, comment_block_height, __comment_type)
        class_root = file_root.getElementsByTagName("class")[0]
        __generate_class(file, class_root, file_name, False)
    else:
        CBG.write_comment_block(file, 'Functions', comment_block_width, comment_block_height, __comment_type)
        __write_functions(file, file_root, False)

    __write_namespace(file, namespace_name, False)
    __write_include_guard(file, file_name, False)
    CBG.write_comment_block(file, 'End of File', comment_block_width, comment_block_end_of_file_height, __comment_type, True, True)

# +----------------------------------------------------------------------+

def __generate_source_file(file, file_root, author_name, 
                                        namespace_name, date, file_name,
                                        comment_block_width, comment_block_height, comment_block_end_of_file_height,
                                        has_class):
    file_name_with_extension = file_name + __source_file_extension
    __write_file_intro(file, file_name_with_extension, True, date, author_name, comment_block_width, comment_block_height)

    CBG.write_comment_block(file, 'Own Includes', comment_block_width, comment_block_height, __comment_type)
    __write_include(file, file_name + __header_file_extension, True)
    CBG.write_comment_block(file, 'System Includes', comment_block_width, comment_block_height, __comment_type)
    __write_namespace(file, namespace_name, True)
    CBG.write_comment_block(file, 'Local constants / Defines', comment_block_width, comment_block_height, __comment_type)
    __structs_and_enums(file, file_root, False)
    
    if has_class:
        CBG.write_comment_block(file, file_name + ' Class Methods', comment_block_width, comment_block_height, __comment_type)
        class_root = file_root.getElementsByTagName("class")[0]
        __generate_class(file, class_root, file_name, True)
    else:
        CBG.write_comment_block(file, 'Functions', comment_block_width, comment_block_height, __comment_type)
        __write_functions(file, file_root, True)

    __write_namespace(file, namespace_name, False)
    CBG.write_comment_block(file, 'End of File', comment_block_width, comment_block_end_of_file_height, __comment_type, True, True)

# +----------------------------------------------------------------------+
# |                                                                      |
# |                        Generation with class                         |
# |                                                                      |
# +----------------------------------------------------------------------+

def __generate_class(file, class_root, class_name, is_source):
    if not is_source:
        file.write(f"class {class_name}\n{{\n")
        file.write("private:\n\n")
        file.write("public:\n\n")

    constructor = class_root.getElementsByTagName("constructor")[0]
    destructor = class_root.getElementsByTagName("destructor")[0]
    methods = class_root.getElementsByTagName("method")

    __write_method_or_function(file, constructor, class_name, is_source, True)
    __write_method_or_function(file, destructor, class_name, is_source, True, True)

    for method in methods:
        __write_method_or_function(file, method, class_name, is_source, True)

    if not is_source:
        file.write(f"}}; // class {class_name}\n\n")

# +----------------------------------------------------------------------+

def __generate_files_with_class(export_dir, xml_root, author_name, 
                                namespace_name, date, comment_block_width,
                                comment_block_height, comment_block_end_of_file_height):
    for file_element in xml_root.getElementsByTagName("file"):
        file_name = str(file_element.getAttribute('name')).upper().capitalize()
        # +------------------------------------------------------------------------------------------------------------+
        s_file = open(os.path.join(export_dir, file_name + __source_file_extension), 'w')
        __generate_source_file(s_file, file_element, author_name,
                                            namespace_name, date, file_name,
                                            comment_block_width, comment_block_height, comment_block_end_of_file_height,
                                            True)
        s_file.close()
        # +------------------------------------------------------------------------------------------------------------+
        h_file = open(os.path.join(export_dir, file_name + __header_file_extension), 'w')
        __generate_header_file(h_file, file_element, author_name,
                                            namespace_name, date, file_name,
                                            comment_block_width, comment_block_height, comment_block_end_of_file_height,
                                            True)
        h_file.close()
        # +------------------------------------------------------------------------------------------------------------+

    return True

# +----------------------------------------------------------------------+
# |                                                                      |
# |                       Generation without class                       |
# |                                                                      |
# +----------------------------------------------------------------------+

def __write_functions(file, file_root, is_source):
    for function in file_root.getElementsByTagName("function"):
        __write_method_or_function(file, function, "", is_source, False)

# +----------------------------------------------------------------------+

def __generate_files_without_class(export_dir, xml_root, author_name, 
                                    namespace_name, date, comment_block_width,
                                    comment_block_height, comment_block_end_of_file_height):
    for file_element in xml_root.getElementsByTagName("file"):
        file_name = str(file_element.getAttribute('name')).upper().capitalize()
        # +------------------------------------------------------------------------------------------------------------+
        s_file = open(os.path.join(export_dir, file_name + __source_file_extension), 'w')
        __generate_source_file(s_file, file_element, author_name,
                                            namespace_name, date, file_name,
                                            comment_block_width, comment_block_height, comment_block_end_of_file_height,
                                            False)
        s_file.close()
        # +------------------------------------------------------------------------------------------------------------+
        h_file = open(os.path.join(export_dir, file_name + __header_file_extension), 'w')
        __generate_header_file(h_file, file_element, author_name,
                                            namespace_name, date, file_name,
                                            comment_block_width, comment_block_height, comment_block_end_of_file_height,
                                            False)
        h_file.close()
        # +------------------------------------------------------------------------------------------------------------+

    return True

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
