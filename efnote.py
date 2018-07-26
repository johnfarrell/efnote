from sys import argv
from enum import Enum
import os
import errno

PATH = os.getenv('HOME', os.path.expanduser('~')) + '/.efnote'



# Logs debug messages to the command-line
def DebugLog(message):
    print("LOG: {}".format(message))

# Loads the format file and parses all formats
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

def ParseArgs(arguments):
    # Simulate 'help' arg if no arguments are passed
    if len(arguments) == 1:
        arguments = ['-h']
        
    for arg in enumerate(arguments):
        # Display useage instructions
        if (arg[1] == '-h') or (arg[1] == '--help'):
            print("usage: efnote [OPTIONS] <commands>\n")
            print("  Note-taking app for easy creation of custom format notes.\n")
            print("Commands:")
            print("  {0:8} {1}".format(
                "view",
                "Open the most recently edited entry"
            ))
            print("  {0:8} {1}".format(
                "new",
                "Create a new entry\n"
            ))
            print("Options:")
            print("  {0:8} {1:2} {2:6} {3}\n".format(
                "--help",
                "-h",
                "",
                "Show this dialog and exit"
            ))


if __name__ == '__main__':
    ParseArgs(argv)