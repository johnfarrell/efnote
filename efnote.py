from sys import argv
from enum import Enum
import os
import errno

DEBUG_MODE = False
PATH = os.getenv('HOME', os.path.expanduser('~')) + '/.efnote'



# Logs debug messages to the command-line
def DebugLog(message):
    print("LOG: {}".format(message))

def LoadFormatFile(format_file):
    DebugLog("Loading format file...")

    # Create ~/.efnote directory if it doesn't exist
    if not os.path.exists(os.path.dirname(format_file)):
        try:
            os.mkdir(os.path.dirname(format_file))
            DebugLog("{} directory created.".format(format_file))
        except OSError:
            if OSError.errno != errno.EEXIST:
                raise

    with open(format_file, 'w+') as opened_file:
        DebugLog("{} opened.".format(format_file))

        


def main(args):
    print("EF Note v0")

    LoadFormatFile(PATH + "/formats.txt")
        

if __name__ == '__main__':
    main(argv);