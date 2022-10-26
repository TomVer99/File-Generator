import modules.c.__shared as shared

import os

__parsers = ['gen.settings.c.xsd']

def get_types():
    return shared.supported_types

def get_xsd():
    xsd = []
    for file in __parsers:
        xsd.append(os.path.join(os.path.dirname(__file__), file))
    return xsd
    