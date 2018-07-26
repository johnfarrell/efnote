from sys import argv
from enum import Enum
import os
import errno
import argparse

# Handles background code
class EFNote:

    def __init__(self):
        # Listen for 
        linein = input("What would you like to do? [n/v/e] > ")
        print(linein)


    def ParseFormatFile(self, file_name):
        for line in open(file_name, 'r+'):
            contents = line.split(' ')
            print(contents)

    

        


# Application setup/close handling
PATH = os.getenv('HOME', os.path.expanduser('~')) + '/.efnote'

# Logs debug messages to the command-line
def DebugLog(message):
    print("LOG: {}".format(message))

# Loads the format file and parses all formats
def LoadFormatFile(format_file):
    DebugLog("Loading format file...")

    # Create ~/.efnote directory if it doesn't exist
    if not os.path.exists(PATH):
        try:
            os.mkdir(os.path.dirname(format_file))
            DebugLog("{} directory created.".format(format_file))
        except OSError:
            if OSError.errno != errno.EEXIST:
                raise

    # Open format file for parsing
    with open(os.path.join(PATH, format_file), 'w+') as opened_file:
        DebugLog("{} opened.".format(format_file))


# TODO: Convert ParseArgs to use ArgParse
def ParseArgs(arguments):

    parser = argparse.ArgumentParser(description="Note-taking app for easy creation of custom format notes.")
    parser.add_argument()
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

def MainLoop():
    
    while True:
        # Wait for input
        # read input
        # Render based on input
        continue


if __name__ == '__main__':
    # Make sure 
    application = EFNote()        
    application.ParseFormatFile("formats.config")