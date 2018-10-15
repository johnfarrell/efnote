import sqlite3
from sqlite3 import Error
import os
import argparse


# Handles background code
class EFNote:
    """
    Enables use of formattable note taking in the command line
    """

    def __init__(self, main_path):
        """
        Initializes class variables
        """
        # Listen for
        self.debug_mode = False
        self.root_path = main_path
        self.config_file = os.path.join(self.root_path, "formats.config")
        self.notes_db = self.ConnectDB()
        self.formats = self.ParseFormatFile()
        self.LoadFiles()

    def ConnectDB(self):
        """
        Connect to the notes database which is used to store all notes
        """
        try:
            db_path = os.path.join(self.root_path, "data/notes.db")
            db = sqlite3.connect(db_path)
            return db
        except Error as e:
            print(e)

        return None

    def RunStatement(self, conn, sql_statement):
        """
        Runs a SQL statement on the notes db. This is used to create and remove
        format tables.
        """
        try:
            cursor = conn.cursor()
            cursor.execute(sql_statement)
            self.notes_db.commit()
        except Error as e:
            print(e)

    def ParseFormatFile(self):
        """
        Reads in config file (defaults to formats.config) to read supported
        formats and add necessary tables to DB if not already in.
        """
        current_format = ""
        loaded_formats = {}

        for line in open(self.config_file, 'r+'):
            contents = line.split(' ')

            if contents[0] == '<#':
                current_format = contents[1].rstrip('\n').lower()
                loaded_formats[current_format] = []

            if contents[0] == '<@':
                loaded_formats[current_format].append(contents[1].strip('\n'))

        conn = self.ConnectDB()
        for curr_format in loaded_formats:
            sql_statement = """CREATE TABLE IF NOT EXISTS {0} (
                               id integer PRIMARY KEY,""".format(curr_format)

            for field in loaded_formats[curr_format]:
                sql_statement += "{} text,".format(field)

            sql_statement = sql_statement.rstrip(",")
            sql_statement += ");"

            self.RunStatement(conn, sql_statement)

        return loaded_formats

    def LoadFiles(self):
        """
        Gets list of files in the root directory
        """
        self.file_list = os.listdir(self.root_path)
        self.file_list.sort(
            key=lambda x: os.stat(os.path.join(self.root_path, x)).st_mtime,
            reverse=True)

    def Run(self):
        """
        The main loop of this program, handles arguments from user
        """

        parser = argparse.ArgumentParser(
            description="""Note-taking app for easy
creation of custom formatted notes.""")

        parser.add_argument(
            'command',
            nargs='?',
            action='store',
            choices=('new', 'view'))
        parser.add_argument(
            '--debug',
            type=parseBoolCmd,
            nargs='?',
            action='store',
            default='false')
        parser.add_argument(
            'entry_type',
            nargs='?',
            action='store')

        results = parser.parse_args()

        if results.debug:
            self.debug_mode = True

        if results.command is None:
            DebugLog("No passed command", self.debug_mode)
            self.PromptForCommand()
        elif results.command == 'new':
            DebugLog("Create new note command", self.debug_mode)
            self.CreateNewNote(results.entry_type)
        elif results.command == 'view':
            DebugLog("View notes command", self.debug_mode)
            self.ViewNotes(results.entry_type)

    def PromptForCommand(self):
        """
        Prompts the user for an action if none was provided in program args
        """

        command = input("\nNEW | VIEW | QUIT [n/v/q] > ")

        if command == 'n':
            self.CreateNewNote(None)
        elif command == 'v':
            self.ViewNotes(None)
        elif command == 'q':
            quit()
        else:
            print("Unrecognized command...")
            self.PromptForCommand()

    def CreateNewNote(self, note_type):
        """
        Creates a new note of a specified type; prompts user if
        no type is specified
        """

        # Make sure that a certain journal type is being used.
        if note_type is None:
            req_type = self.PromptForNoteType()
        else:
            req_type = note_type.lower()

        # Ensure requested type exists, prompt user
        # for type creation if it doesn't.
        if req_type not in self.formats:
            new_format = input("""There is no '{}' format,
would you like to create one? [y/n] > """.format(req_type))

            if new_format == 'y':
                self.CreateNewFormat(req_type)
            else:
                self.Exit()

        print("Creating new {} entry".format(req_type))

        # Make sure that the format type is valid
        assert req_type in self.formats

        new_entry = {}
        for format_field in self.formats[req_type]:
            print("---- {0:15} ----".format(format_field))
            new_entry[format_field] = input()

        save_entry = input("\nSave entry? [y/n] > ")

    def CreateNewFormat(self, format_name):
        """
        Guides user through easy creation of new formats

        TO-DO: Finish implementation
        """

        # Test if format_name already exists
        if format_name in self.formats:
            print("Format already exists...")

    def PromptForNoteType(self):
        """
        Prompts user to enter a note format.
        """
        supported_types = ""
        counter = 0

        # Loop through the current supported formats
        # and concatenate them to a string for printing.
        for curr_type in self.formats:
            supported_types += curr_type

            if counter != len(self.formats) - 1:
                supported_types += " | "
                counter += 1
            # Format wrapping of type output so it doesn't overflow
            # small terminals.
            if counter % 5 == 0:
                supported_types += "\n"

        print("Supported Formats:\n{0}".format(supported_types))
        return input("Which format would you like to create? > ").lower()

    def ViewNotes(self, note_type):
        """
        Views notes of specific type; views all notes if none provided
        """
        for file in self.file_list:
            print("File {0:15} (last modified: {1:30})".format(
                file,
                os.stat(os.path.join(self.root_path, file)).st_mtime))

        self.Exit()

    def Exit(self):
        """
        Handles program loop exiting
        """
        cont = input("\nAny further action? [y/n] > ")

        if cont == 'y':
            self.PromptForCommand()
        elif cont == 'n':
            self.notes_db.close()
            quit()
        else:
            print("Unrecognized command...quitting...")
            quit()
# Application setup/close handling
# PATH = os.getenv('HOME', os.path.expanduser('~')) + '/.efnote'


# Logs debug messages to the command-line
def DebugLog(message, status):
    """
    Prints a message to the terminal if debug mode is enabled
    """
    if status:
        print("LOG: {}".format(message))


def parseBoolCmd(cmd):
    """
    Parses possible values of a boolean passed as argparse argument
    """
    if cmd.lower() in ('1', 'y', 'yes', 't', 'true'):
        return True
    elif cmd.lower() in ('0', 'n', 'no', 'f', 'false'):
        return False

    return argparse.ArgumentTypeError("Expected boolean")
