import src.DoxygenGenerator as doxy
import src.CommentBlockGenerator as c_block
import os

__comment_type = '//'

def generate_cpp_class_file(location,
                            author,
                            date,
                            file_name,
                            namespace_name, 
                            class_object,
                            comment_block_width,
                            comment_block_height,
                            comment_block_end_of_file_height):
    """
    Generate a C++ source file.
    """

    class_present = __check_class_object(class_object)

    if class_present:
        class_object = class_object[0]

    if not os.path.exists(location):
        os.makedirs(location)

    file = open(location + file_name + '.cpp', 'w')

    c_block.write_comment_block(file, 'C++ Source File', comment_block_width, comment_block_height, __comment_type)
    doxy.cpp_write_doc_file_header(file, file_name + '.cpp', author, date)

    c_block.write_comment_block(file, 'Own Includes', comment_block_width, comment_block_height, __comment_type)
    __write_include(file, f'"{file_name}.hpp"')

    c_block.write_comment_block(file, 'System Includes', comment_block_width, comment_block_height, __comment_type)
    __write_namespace(file, namespace_name, True)
    c_block.write_comment_block(file, 'Local constants / Defines', comment_block_width, comment_block_height, __comment_type)
    c_block.write_comment_block(file, 'Functions / Methods', comment_block_width, comment_block_height, __comment_type)

    if class_present:
        __write_methods(file, class_object, True)

    __write_namespace(file, namespace_name, False)
    c_block.write_comment_block(file, 'End of File', comment_block_width, comment_block_end_of_file_height, __comment_type, True, True)

    file.close()

def generate_hpp_class_file(location,
                            author,
                            date,
                            file_name,
                            namespace_name, 
                            class_object,
                            comment_block_width,
                            comment_block_height,
                            comment_block_end_of_file_height):
    """
    Generate a C++ header file.
    """
    
    class_present = __check_class_object(class_object)

    if class_present:
        class_object = class_object[0]

    if not os.path.exists(location):
        os.makedirs(location)

    file = open(location + file_name + '.hpp', 'w')

    c_block.write_comment_block(file, 'C++ Header File', comment_block_width, comment_block_height, __comment_type)
    doxy.cpp_write_doc_file_header(file, file_name + '.hpp', author, date)

    __write_include_guard(file, file_name, True)

    c_block.write_comment_block(file, 'Own Includes', comment_block_width, comment_block_height, __comment_type)

    c_block.write_comment_block(file, 'System Includes', comment_block_width, comment_block_height, __comment_type)
    __write_namespace(file, namespace_name, True)
    c_block.write_comment_block(file, 'Global constants / Defines', comment_block_width, comment_block_height, __comment_type)
    c_block.write_comment_block(file, 'Class', comment_block_width, comment_block_height, __comment_type)

    if class_present:
        __write_class(file, class_object, True)

        __write_methods(file, class_object, False)

        __write_class(file, class_object, False)

    __write_namespace(file, namespace_name, False)

    __write_include_guard(file, file_name, False)

    c_block.write_comment_block(file, 'End of File', comment_block_width, comment_block_end_of_file_height, __comment_type, True, True)

    file.close()

def __write_namespace(file, namespace, is_open):
    """
    Write a namespace to a file.
    """
    namespace = namespace.upper()
    if is_open:
        file.write(f"namespace {namespace}\n{{\n\n")
    else:
        file.write(f"}} // namespace {namespace}\n\n")

def __write_include(file, include):
    """
    Write an include to a file.
    """
    file.write(f"#include {include}\n\n")

def __write_methods(file, class_object, is_source):
    """
    Write the methods to a source file.
    """

    # get class name
    try:
        class_name = class_object.getAttribute('name')
    except:
        class_name = "error"

    # write methods
    try:
        methods = class_object.getElementsByTagName('method')
    except:
        return

    for method in methods:
        __write_method(file, class_name, method, is_source)

def __write_method(file, class_name, method, is_source):
    """
    Write a method to a source file.
    """

    # get return type
    try:
        return_type = method.getElementsByTagName('return')[0].childNodes[0].nodeValue
    except:
        return_type = ""

    # get method name
    try:
        method_name = method.getAttribute('name')
    except:
        method_name = "error"
    else:
        if method_name == "":
            method_name = "error"

    # get parameters
    try:
        parameters = method.getElementsByTagName('parameter')
    except:
        parameters = None

    if not is_source:
        doxy.cpp_write_doc_method(file, return_type, parameters)

    if return_type == "":
        file.write(f"{class_name}::{method_name}(")
    else:
        file.write(f"{return_type} {class_name}::{method_name}(")
    
    if len(parameters) == 0:
        file.write(")")
    
    for parameter in parameters:
        param_type = parameter.getElementsByTagName('type')[0].childNodes[0].nodeValue
        param_name = parameter.getElementsByTagName('name')[0].childNodes[0].nodeValue
        
        if len(parameters) == 1:
            file.write(f"{param_type} {param_name})")

        else:
            if parameter == parameters[0]:        # first parameter
                file.write(f"{param_type} {param_name},\n")

            elif parameter == parameters[-1]:         # last parameter
                file.write(" " * ((len(return_type) + len(class_name) + len(method_name)) + 4))
                file.write(f"{param_type} {param_name})")

            else:                                   # other parameter
                file.write(" " * ((len(return_type) + len(class_name) + len(method_name)) + 4))
                file.write(f"{param_type} {param_name},\n")

    if is_source:
        file.write("\n{\n")
        file.write("    // TODO: Implement\n")
        file.write("}\n\n")
    else:
        file.write(";\n\n")

def __write_class(file, class_object, is_open):
    """
    Write a class to a header file
    """

    # get class name
    try:
        class_name = class_object.getAttribute('name')
    except:
        class_name = "error"

    if is_open:
        file.write(f"class {class_name}\n")
        file.write("{\n")
        file.write("private:\n\n")
        file.write("public:\n\n")
    else:
        file.write(f"}}; // class {class_name}\n\n")

def __write_include_guard(file, file_name, is_open):
    """
    Write an include guard to a header file.
    """
   
    if is_open:
        file.write(f"#ifndef {file_name.upper()}_HPP\n")
        file.write(f"#define {file_name.upper()}_HPP\n\n")
    else:
        file.write(f"#endif // {file_name.upper()}_HPP\n\n")

def __check_class_object(class_object):
    """
    Check if a class object is valid.
    """
    try:
        class_object = class_object[0]
    except:
        return False
    else:
        return True
