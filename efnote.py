import sqlite3
from sqlite3 import Error
import os
import argparse
import shutil


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

    def RunStatement(self, sql_statement):
        """
        Runs a SQL statement on the notes db. This is used to create and remove
        format tables.
        """
        try:
            conn = self.notes_db
            cursor = conn.cursor()
            cursor.execute(sql_statement)
            vals = cursor.fetchall()
            self.notes_db.commit()
            return vals
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

        # TODO: Find a better way to do this
        for curr_format in loaded_formats:
            sql_statement = """CREATE TABLE IF NOT EXISTS {0} (
                               """.format(curr_format)

            for field in loaded_formats[curr_format]:
                sql_statement += "{} text,".format(field)

            sql_statement = sql_statement.rstrip(",")
            sql_statement += ");"

            self.RunStatement(sql_statement)

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
            description="""Note-taking app for easy creation of custom formatted notes."""
        )

        parser.add_argument(
            'command',
            nargs='?',
            action='store',
            choices=('new', 'view')
        )
        parser.add_argument(
            '--debug',
            type=parseBoolCmd,
            nargs='?',
            action='store',
            default='false'
        )
        parser.add_argument(
            'entry_type',
            nargs='?',
            action='store'
        )

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

        function_map = {
            "NEW": self.CreateNewNote,
            "N": self.CreateNewNote,
            "VIEW": self.ViewNotes,
            "V": self.ViewNotes,
            "QUIT": quit,
            "Q": quit,
        }

        command = input("\nNEW | VIEW | QUIT [n/v/q] > ")

        try:
            function_map[command.capitalize()](None)
        except KeyError:
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
            new_format = input("""There is no '{0}' format {1} Would you like to create one? [y/n] > """
                               .format(req_type, os.linesep))

            if new_format == 'y':
                self.CreateNewFormat(req_type)
            else:
                self.Exit()

        print("Creating new {} entry".format(req_type))

        # Make sure that the format type is valid
        assert req_type in self.formats

        new_entry = {}
        for format_field in self.formats[req_type]:
            print("---- {0:^15} ----".format(format_field))
            new_entry[format_field] = input()

        save_entry = input("\nSave entry? [y/n] > ")

        if parseBoolCmd(save_entry):
            sql_value_string = self.createSQLEntryString(new_entry)
            sql_str = "INSERT INTO {} VALUES {}".format(req_type,
                                                        sql_value_string)
            
            self.RunStatement(sql_str)

    def createSQLEntryString(self, entry_items):
        """
        Concatenates a list of strings into a format for easy entry into
        a SQL table
        """
        print(entry_items)
        return_str = "("
        for entry_type in entry_items:
            return_str += "'" + entry_items[entry_type] + "'" + ','
        return return_str.rstrip(',') + ")"

    def CreateNewFormat(self, format_name):
        """
        Guides user through easy creation of new formats

        Creates a new table in the storage db for the format.

        TO-DO: Finish implementation
        """

        # Test if format_name already exists
        if format_name in self.formats:
            print("Format already exists...")
            return

    def PromptForNoteType(self, action="create"):
        """
        Prompts user to enter a note format.
        (optional) action -> Modifies the input prompt to accurately depict
        what the note format will be used for (viewing, creating, etc.)
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
        return input("Which format would you like to {}? > ".format(action)).lower()

    def ViewNotes(self, note_type):
        """
        Views notes of specific type; views all notes if none provided

        TODO: Implement database lookup and listing
        """
        # retrieves terminal size
        term_size = shutil.get_terminal_size()
        concatenated_note = False

        if note_type is None:
            note_type = self.PromptForNoteType("view")
        statement = "SELECT * FROM {}".format(note_type)
        notes = self.RunStatement(statement)

        if notes is None:
            print("No {} entries... (check your spelling?)".format(note_type))
        else:
            note_map = {}
            note_number = 1
            for note in notes:
                temp_str = "{}: ".format(note_number)
                for val in note:
                    temp_str += val + " "

                note_map[note_number] = temp_str  # Memoize the note for potential later retrieval
                if len(temp_str) > term_size.columns - 5:
                    temp_str = (temp_str[:term_size.columns - 7] + '..')
                    concatenated_note = True
                else:
                    temp_str = temp_str.rstrip(" ")

                print(temp_str)

                note_number += 1

            if concatenated_note:
                print(os.linesep + "There appears to be one (or more) notes that are concatenated")
                view_note = input("If you would like to expand a note, enter the number (otherwise, n) > ")
                try:
                    note_index = int(view_note)
                    print(os.linesep + note_map[note_index])
                except ValueError:
                    # The value of view_note is not an integer, so continue
                    pass
                except KeyError:
                    # The input WAS a number, but it isn't a valid note number
                    print("That is not a valid note number.")
                    pass

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
