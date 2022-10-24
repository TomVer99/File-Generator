from enum import Enum

class Color(Enum):
    NOTIFY = '\033[93m'
    SUCCESS = '\033[92m'
    FAIL = '\033[91m'
    INFO = '\033[36m'
    END = '\033[0m'

def log(message:str, color:Color, tabs:int = 1, end:str = '\n'):
    print(color.value + '  ' * tabs + message + Color.END.value, end=end)

def log_error(message:str, tabs:int = 1, end:str = '\n'):
    log(message, Color.FAIL, tabs, end)

def log_success(message:str, tabs:int = 1, end:str = '\n'):
    log(message, Color.SUCCESS, tabs, end)

def log_notify(message:str, tabs:int = 1, end:str = '\n'):
    log(message, Color.NOTIFY, tabs, end)

def log_info(message:str, tabs:int = 1, end:str = '\n'):
    log(message, Color.INFO, tabs, end)

def log_divider(tabs:int = 1):
    log('------------------------------------------------------------------------', Color.INFO, tabs)
