#!/usr/bin/env python3
__author__ = 'micomicona'

#import getopt,os,sys
import os,sys

def main(argv):
    """
    :param argv:
    :return:
    """
    errors = []
    commands = []
    arguments = []
    if len(argv) == 0:
        printusage()
        sys.exit(2)
    for arg in argv:
        if arg.lower() in ('-h', '--help'):
            printusage()
            sys.exit(2)
        elif arg.lower() in ("-g", "--replaygain"):
            commands.append(replayGain)
        else:
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
        printusage()
        sys.exit(2)
    '''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        printusage()
        sys.exit(2)
    for opt, arg in opts:
        if opt.lower() in ("-h", "--help"):
            printusage()
            sys.exit()
        elif opt in ("-g", "--replaygain"):
            commands.add(replayGain)
    #print('Input file: ', inputfile)
    #print('Output file: ', outputfile)
    #print('Files: ', args)
    '''

def printusage():
    print('%s [COMMANDS]... [FILES]...' % (os.path.basename(__file__)))
    print('\nSupported commands:')
    print('  -g, --replaygain             Set ReplayGain values')

def replayGain():
    print("Calcular ReplayGain")

if __name__ == "__main__":
   main(sys.argv[1:])