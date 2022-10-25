####################################################################################################
#                                                                                                  #
#                                       write_doc_file_header                                      #
#                                                                                                  #
####################################################################################################

def cpp_write_doc_file_header(file, file_name, author, date, description = ""):
    """
    Write the doxygen header to a file.
    """
    __group_1_write_doc_file_header(file, file_name, author, date, description)

def c_write_doc_file_header(file, file_name, author, date, description = ""):
    """
    Write the doxygen header to a file.
    """
    __group_1_write_doc_file_header(file, file_name, author, date, description)

def __group_1_write_doc_file_header(file, file_name, author, date, description = ""):
    """
    Write the doxygen header to a file.
    """
    file.write("/**\n")
    file.write(f" * @file {file_name}\n")
    file.write(" *\n")

    if description != "":
        file.write(f" * @brief {description}\n")
    else:
        file.write(" * @brief Brief description of the file\n")

    file.write(" *\n")
    file.write(f" * @author {author}\n")
    file.write(f" * @date {date}\n")
    file.write(" */\n\n")

####################################################################################################
#                                                                                                  #
#                                         write_doc_method                                         #
#                                                                                                  #
####################################################################################################

def __group_1_write_doc_universal(file, return_type, parameters, description = "", is_method = False):
    file.write(f"/**\n")

    if description != "":
        file.write(f" * @brief {description}\n")
    elif is_method:
        file.write(" * @brief Brief description of method\n")
    else:
        file.write(" * @brief Brief description of function\n")

    if len(parameters) != 0 or len(return_type) != 0:
        file.write(f" *\n")

    for param in parameters:
        file.write(f" * @param {param.getElementsByTagName('name')[0].childNodes[0].nodeValue}\n")
        if param == parameters[-1] and len(return_type) != 0:
            file.write(f" *\n")

    if return_type != "":
        file.write(f" * @return {return_type}\n")
        
    file.write(f" */\n")

def __group_1_write_doc_method(file, return_type, parameters, description = ""):
    """
    Write the doxygen documentation template of a method.
    """
    __group_1_write_doc_universal(file, return_type, parameters, description, True)
    pass
    
def __group_1_write_doc_function(file, return_type, parameters, description = ""):
    """
    Write the doxygen documentation template of a function.
    """
    __group_1_write_doc_universal(file, return_type, parameters, description, False)

# +----------------------------------------------------------------------+

def cpp_write_doc_method(file, return_type, parameters, description = ""):
    """
    Write the doxygen documentation template of a method.
    """
    __group_1_write_doc_method(file, return_type, parameters, description)

def cpp_write_doc_function(file, return_type, parameters, description = ""):
    """
    Write the doxygen documentation template of a function.
    """
    __group_1_write_doc_function(file, return_type, parameters, description)
