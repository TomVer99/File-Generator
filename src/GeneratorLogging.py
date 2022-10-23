from enum import Enum

class Color(Enum):
    NOTIFY = '\033[93m'
    SUCCESS = '\033[92m'
    FAIL = '\033[91m'
    END = '\033[0m'

def print_to_console(message:str, color:Color, tabs:int = 1, end:str = '\n'):
    print(color.value + '  ' * tabs + message + Color.END.value, end=end)
