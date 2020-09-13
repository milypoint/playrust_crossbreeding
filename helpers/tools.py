import sys


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def disable(self):
        self.__class__.HEADER = ''
        self.__class__.OKBLUE = ''
        self.__class__.OKGREEN = ''
        self.__class__.WARNING = ''
        self.__class__.FAIL = ''
        self.__class__.ENDC = ''
        self.__class__.BOLD = ''
        self.__class__.UNDERLINE = ''


class ColorOutput:
    @staticmethod
    def gene(g):
        gene_colours = {
            'Y': bcolors.OKGREEN,
            'G': bcolors.OKGREEN,
            'H': bcolors.OKGREEN,
            'X': bcolors.FAIL,
            'W': bcolors.FAIL
        }
        return "".join([f"{gene_colours[_g]}{_g}{bcolors.ENDC}" for _g in g])

    @staticmethod
    def purple(text):
        return f'{bcolors.HEADER}{text}{bcolors.ENDC}'

    @staticmethod
    def blue(text):
        return f'{bcolors.OKBLUE}{text}{bcolors.ENDC}'

    @staticmethod
    def green(text):
        return f'{bcolors.OKGREEN}{text}{bcolors.ENDC}'

    @staticmethod
    def yellow(text):
        return f'{bcolors.WARNING}{text}{bcolors.ENDC}'

    @staticmethod
    def red(text):
        return f'{bcolors.FAIL}{text}{bcolors.ENDC}'

    @staticmethod
    def bold(text):
        return f'{bcolors.BOLD}{text}{bcolors.ENDC}'

    @staticmethod
    def underline(text):
        return f'{bcolors.UNDERLINE}{text}{bcolors.ENDC}'


def die(msg=None, items=False):
    if msg is not None:
        if items:
            for i in msg:
                print(i)
        else:
            print(msg)
    sys.exit()


def print_list(l):
    for i in l:
        print(i)
