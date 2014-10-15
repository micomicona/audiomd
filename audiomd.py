#!/usr/bin/env python3
import glob
import os
import sys

__author__ = 'micomicona'


def main(argv):

    errors = []
    commands = []
    arguments = []
    # Flag used to indicate that the program is reading file names
    # Once this happens no more commands should be added
    # In other words: force program usage to first accept commands and later file names
    reading_arguments = False;
    # Flag used to indicate if the program should traverse directories recursively
    recursive = False;

    if len(argv) == 0:
        print_usage()
        sys.exit(2)

    for arg in argv:
        if arg.lower() in ('-h', '--help'):
            if reading_arguments:
                errors.append("Commands should be specified before file names (%s)" % arg)
            print_usage()
            sys.exit(2)
        elif arg.lower() in ("-g", "--replaygain"):
            if reading_arguments:
                errors.append("Commands should be specified before file names (%s)" % arg)
            commands.append(replay_gain)
        elif arg.lower() in ("-r", "--recursive"):
            recursive = True;
        else:
            reading_arguments = True
            arguments.append(arg)

    if len(commands) == 0:
        errors.append("Nothing to do! Please specify at least one command")
    if len(arguments) == 0:
        errors.append("No files specified")

    if len(errors) > 0:
        print("Errors found. Please check the following messages for more information:")
        for error in errors:
            print(error)
        print()
        print_usage()
        sys.exit(2)

    if recursive:
        for path, dirs, files in os.walk("."):
            print("PATH: " + path)
            for argument in arguments:
                for file in glob.glob(os.path.join(path, argument)):
                    print("FILE: " + file)
    else:
        for argument in arguments:
            for file in glob.glob(argument):
                print("FILE: " + file)

    sys.exit(0)


def print_usage():
    print('%s [COMMANDS]... [FILES]...' % (os.path.basename(__file__)))
    print('\nSupported commands:')
    print('  -g, --replaygain             Set ReplayGain values')
    print('  -r, --recursive              Recursively traverse directories (one album per directory)')


def replay_gain():
    print("Calcular ReplayGain")

if __name__ == "__main__":
   main(sys.argv[1:])