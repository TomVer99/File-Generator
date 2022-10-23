import xml.dom.minidom
import os

def __check_for_attribute(element, attribute):
    if element.hasAttribute(attribute):
        v = '\033[92m' + "Found '" + attribute + "' attribute: " + element.getAttribute(attribute) + '\033[0m'
        return [True, v]
    else:
        v = '\033[91m' + "Missing '" + attribute + "' attribute" + '\033[0m'
        return [False, v]

def __check_for_child_elements(element, child_element_name, optional=False):
    elements = element.getElementsByTagName(child_element_name)
    if elements:
        if len(elements) > 1:
            v = '\033[92m' + "Found " + str(len(elements)) + " '" + child_element_name + "' elements" + '\033[0m'
            return [True, v]
        else:
            v = '\033[92m' + "Found '" + child_element_name + "' element" + '\033[0m'
            return [True, v]
    elif not optional:
        v = '\033[91m' + "Missing '" + child_element_name + "' element" + '\033[0m'
        return [False, v]
    else:
        return [True, ""]

def __tab(tabs):
    return "|\t" * tabs

def parse_xml_file(file):
    print('\033[93m' + "Parsing file: " + file + '\033[0m' + "\n")
    xml_file = xml.dom.minidom.parse(file)
    root = xml_file.documentElement

    print('\033[93m' + "Checking 'files' element" + '\033[0m')
    result = __check_for_attribute(root, "type")
    print(__tab(1) + result[1])
    result = __check_for_child_elements(root, "export_location")
    print(__tab(1) + result[1])
    result = __check_for_child_elements(root, "author")
    print(__tab(1) + result[1])
    result = __check_for_child_elements(root, "namespace")
    print(__tab(1) + result[1])
    result = __check_for_child_elements(root, "file")
    print(__tab(1) + result[1])

    print(__tab(1) + '\033[93m' + "Checking 'author' element" + '\033[0m')
    author = root.getElementsByTagName('author')[0]
    result = __check_for_attribute(author, "name")
    print(__tab(2) + result[1])

    print(__tab(1) + '\033[93m' + "Checking 'namespace' element" + '\033[0m')
    namespace = root.getElementsByTagName('namespace')[0]
    result = __check_for_attribute(namespace, "name")
    print(__tab(2) + result[1])

    print(__tab(1) + '\033[93m' + "Checking 'file' element(s)" + '\033[0m')
    files = root.getElementsByTagName('file')
    for index, file in enumerate(files):
        print(__tab(2) + '\033[93m' + "Checking file " + str((index + 1)) + '\033[0m')
        result = __check_for_attribute(file, "name")
        print(__tab(3) + result[1])
        if result[0]:
            file_name = file.getAttribute("name")
        result = __check_for_child_elements(file, "class")
        print(__tab(3) + result[1])
        if result[0]:
            print(__tab(3) + '\033[93m' + "Checking 'class' element" + '\033[0m')
            class_element = file.getElementsByTagName('class')[0]
            result = __check_for_attribute(class_element, "name")
            print(__tab(4) + result[1])
            if result[0]:
                class_name = class_element.getAttribute("name")


        print(__tab(3) + '\033[93m' + "Checking 'method' element(s)" + '\033[0m')
        methods = file.getElementsByTagName('method')
        ctor_detected = False
        dtor_detected = False
        for index, method in enumerate(methods):
            print(__tab(4) + '\033[93m' + "Checking method " + str((index + 1)) + '\033[0m')
            result = __check_for_attribute(method, "name")
            print(__tab(5) + result[1])
            if result[0]:
                method_name = method.getAttribute("name")

            if method_name != file_name and method_name != '~' + file_name:
                result = __check_for_child_elements(method, "return", True)
                print(__tab(5) + result[1])
            elif method_name == file_name:
                ctor_detected = True
            elif method_name == '~' + file_name:
                dtor_detected = True

            result = __check_for_child_elements(method, "parameter", True)
            print(__tab(5) + result[1])

        if not ctor_detected:
            print(__tab(4) + '\033[91m' + "Missing constructor" + '\033[0m')
        if not dtor_detected:
            print(__tab(4) + '\033[91m' + "Missing destructor" + '\033[0m')
        
        if file_name == class_name and ctor_detected and dtor_detected:
            print(__tab(3) + '\033[92m' + "Class complete '" + class_name + "'" + '\033[0m')
        else:
            print(__tab(3) + '\033[91m' + "Class incomplete '" + class_name + "'" + '\033[0m')
            if not ctor_detected:
                print(__tab(4) + '\033[91m' + "Missing constructor" + '\033[0m')
            if not dtor_detected:
                print(__tab(4) + '\033[91m' + "Missing destructor" + '\033[0m')
            if file_name != class_name:
                print(__tab(4) + '\033[91m' + "File name and class name do not match" + '\033[0m')

# TODO: remove this
if __name__ == "__main__":
    parse_xml_file(os.path.join(os.path.dirname(__file__), "..", "gen.source.xml"))
