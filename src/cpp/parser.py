__supported_types = ['cpp.class', 'cpp.func']

__parsers = ['/cpp/gen.settings.cpp.class.xsd', '/cpp/gen.settings.cpp.func.xsd']

def parse_language(type):
    for index, types in enumerate(__supported_types):
        if type == types:
            return __parsers[index]
    return None
