import cpp.__shared as shared

__parsers = ['/cpp/gen.settings.cpp.class.xsd', '/cpp/gen.settings.cpp.func.xsd']

def parse_language(type):
    for index, types in enumerate(shared.supported_types):
        if type == types:
            return __parsers[index]
    return None
