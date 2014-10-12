#!/usr/bin/env python3
__author__ = 'micomicona'

import getopt,os,sys


def main(argv):
    """
    :param argv:
    :return:
    """

    inputfile = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        printusage()
        sys.exit(2)
    for opt, arg in opts:
        if opt.lower() in ("-h", "--help"):
            printusage()
            sys.exit()
        elif opt in ("-g", "--replaygain"):
            inputfile = arg
    print('Input file is "', inputfile)
    print('Output file is "', outputfile)

def printusage():
    print('%s -i <inputfile> -o <outputfile>' % (os.path.basename(__file__)))

if __name__ == "__main__":
   main(sys.argv[1:])