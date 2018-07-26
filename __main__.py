# Handles program entry/exit protocol

import os
import errno
import efnote


PATH = os.path.join(os.getenv('HOME', os.path.expanduser('~')), '.efnote/')

if not os.path.isdir(PATH):
    print("Root directory not found!")
    generate = input("Would you like to generate it? (y/n/q) > ")

    if generate == "y" or generate == "yes":
        try:
            os.mkdir(PATH)
        except:
            print("Directory Write Error!")
            print("Attempting to write to {}".format(PATH))
            print("Check permissions maybe?")
            print("Quitting...\n")
            quit()

    elif generate == "n" or generate == "no":
        print("EFNote needs to generate this directory")
        print("You know where to find me if you change your mind\n")
        quit()

    elif generate == "q" or generate == "quit":
        quit()

if not os.path.isfile(os.path.join(PATH, "formats.config")):
    try:
        with open(os.path.join(PATH, "formats.config"), "w") as out:
            out.write("<# Journal\n<@ Date\n<@ Content")
    except:
        print("File Write Error!")
        print("How did this even happen?")
        quit()

application = efnote.EFNote(PATH)
application.ParseFormatFile()
application.Run()