HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

PREFIX = ">> "

def __print_color(color, content):
    print(PREFIX + color + content + ENDC)

def print_success(*args, sep=" ") -> None:
    __print_color(OKGREEN, sep.join(args))

def print_error(*args, sep=" ") -> None:
    __print_color(FAIL, sep.join(args))

def print_info(*args, sep=" ") -> None:
    __print_color(OKBLUE, sep.join(args))

def print_line() -> None:
    __print_color(OKCYAN, "<<<<<<:>~")
