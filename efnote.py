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
        self.config_file = os.path.join(self.root_path, "formats.config")
        self.formats = self.ParseFormatFile()
        self.LoadFiles()


    def ParseFormatFile(self):
        """Reads in config file (defaults to formats.config) to read supported formats"""
        current_format = ""
        loaded_formats = {}
        
        for line in open(self.config_file, 'r+'):
            contents = line.split(' ')

            if(contents[0] == '<#'):
                current_format = contents[1].rstrip('\n')
                loaded_formats[current_format] = []
            if(contents[0] == '<@'):
                loaded_formats[current_format].append(contents[1].strip('\n'))

        return loaded_formats



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

        if(results.command == None):
            DebugLog("No passed command") 
            self.PromptForCommand()
        elif(results.command == 'new'):
            DebugLog("Create new note command")
            self.CreateNewNote(results.entry_type)
        elif(results.command == 'view'):
            DebugLog("View notes command")
            self.ViewNotes(results.entry_type)

    def PromptForCommand(self):
        command = input("\nNEW | VIEW | QUIT [n/v/q] > ")
        
        if(command == 'n'):
            self.CreateNewNote(None)
        elif(command == 'v'):
            self.ViewNotes(None)
        elif(command == 'q'):
            quit()
        else:
            print("Unrecognized command...")
            self.PromptForCommand()

    def CreateNewNote(self, note_type):
        if(note_type is None):
            req_type = self.PromptForNoteType()
        else:
            req_type = note_type

        print(req_type)

        self.Exit()

    def PromptForNoteType(self):
        supported_types = ""
        counter = 0
        for curr_type in self.formats:
            supported_types += curr_type

            if(counter != len(self.formats) - 1):
                supported_types += " | "
                counter += 1

        print("{0} total format(s)...\n{1}".format(counter + 1, supported_types))
        return input("Which format would you like to create? > ")



    def ViewNotes(self, note_type):
        for file in self.file_list:
            print("File {0:15} (last modified: {1:30})".format(file,
                    os.stat(os.path.join(self.root_path, file)).st_mtime))

        self.Exit()

    def Exit(self):
        cont = input("\nAny further action? [y/n] > ")

        if(cont == 'y'):
            self.PromptForCommand()
        elif(cont == 'n'):
            quit()
        else:
            print("Unrecognized command...quitting...")
            quit()

# Application setup/close handling
# PATH = os.getenv('HOME', os.path.expanduser('~')) + '/.efnote'

# Logs debug messages to the command-line
def DebugLog(message):
    print("LOG: {}".format(message))