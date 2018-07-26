from sys import argv
from enum import Enum
import os
import errno
import argparse

# Handles background code
class EFNote:

    def __init__(self, main_path):
        # Listen for
        self.root_path = main_path
        self.formats = {}
        self.ParseFormatFile()
        self.LoadFiles()

    # Reads in formats.config file to read supported formats
    def ParseFormatFile(self, file_name="formats.config"):
        current_format = ""
        for line in open(file_name, 'r+'):
            contents = line.split(' ')

            if(contents[0] == '<#'):
                current_format = contents[1].rstrip('\n')
                self.formats[current_format] = []
            
            if(contents[0] == '<@'):
                self.formats[current_format].append(contents[1].strip('\n'))


    def LoadFiles(self):
        """Gets list of files in the root directory"""
        self.file_list = os.listdir(self.root_path)
        self.file_list.sort(key=lambda x: os.stat(os.path.join(self.root_path, x)).st_mtime, reverse=True)


    def Run(self):
        """
        The main loop of this program, handles arguments from user
        """

        parser = argparse.ArgumentParser(description="Note-taking app for easy creation of custom formatted notes.")

        parser.add_argument('command', nargs='?', action='store', choices=['new', 'view'])
        parser.add_argument('entry_type', nargs='?', action='store')

        results = parser.parse_args()

        print(results.command)
        print(results.entry_type)



        while True:
            # Wait for input
            linein = input("What would you like to do? [n/v/q] > ")
            # read input
            if linein == "v" or linein == "view":
            # Render based on input
                for file in self.file_list:
                    print("File {0:15} (last modified: {1:30})".format(file,
                                                                os.stat(os.path.join(self.root_path, file)).st_mtime))
            if linein == "q" or linein == "quit":
                print("\nbye bitch\n")
                quit()


# Application setup/close handling
# PATH = os.getenv('HOME', os.path.expanduser('~')) + '/.efnote'

# Logs debug messages to the command-line
def DebugLog(message):
    print("LOG: {}".format(message))