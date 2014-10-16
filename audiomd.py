#!/usr/bin/env python3

# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Micomicona
# a.sexto@micomicona.com
# http://micomicona.com

# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Command-line script to keep your audio files healthy.
"""

import glob
import magic
import mutagen
import os
from rgain import rgcalc
from rgain import rgio
import sys

__author__ = 'micomicona'
__mime = magic.Magic(mime=True)

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
            commands.append(CommandReplayGain())
        elif arg.lower() in ("-r", "--recursive"):
            recursive = True;
        elif arg.lower() in ("-v", "--view"):
            commands.append(CommandView())
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

    folders_inspected = 0;
    files_processed = 0
    if recursive:
        for path, dirs, files in os.walk("."):
            folders_inspected += 1
            files_processed += process_album(path, arguments, commands)
    else:
        folders_inspected += 1
        files_processed += process_album(".", arguments, commands)

    print("%i files processed, %i folders inspected" %(files_processed, folders_inspected))
    sys.exit(0)


def process_album(path, arguments, commands):
    album_files = []
    files_processed = 0;
    for argument in arguments:
                for file in glob.glob(os.path.join(path, argument)):
                    if file_type_supported(file):
                        album_files.append(file)
                        files_processed += 1
    if len(album_files) == 0:
        return 0
    for command in commands:
        if command.works_with_whole_album():
            album_files = command.process_album(album_files)
        if command.works_with_individual_tracks():
            for counter, file in enumerate(album_files):
                album_files[counter] = command.process_track(file)
    return files_processed


def file_type_supported(file):
    mime_type = str(__mime.from_file(file))
    if mime_type == "b'audio/x-flac'":
        return True
    else:
        print("Error: Unsupported mime type %s found in %s" % (mime_type, file))
        return False


def print_usage():
    print('%s [COMMANDS]... [FILES]...' % (os.path.basename(__file__)))
    print('\nSupported commands:')
    print('  -g, --replaygain             Set ReplayGain values')
    print('  -r, --recursive              Recursively traverse directories (one album per directory)')
    print('  -v, --view                   View track information')


class CommandReplayGain:
    #def __init__(self):
    #    print("Calcular ReplayGain")

    def works_with_whole_album(self):
        return True

    def works_with_individual_tracks(self):
        return False

    def process_album(self, files):
        print("Calculating and updating album ReplayGain..." + str(files))
        rg = rgcalc.ReplayGain(files, True)
        rg.start()


class CommandView:
    #def __init__(self):
        #print("View track information")

    def works_with_whole_album(self):
        return False

    def works_with_individual_tracks(self):
        return True

    def process_track(self, file):
        print("Filename: %s" % file)

        formats_map = rgio.BaseFormatsMap()
        try:
            replaygain_trackdata, replaygain_albumdata = formats_map.read_gain(file)
        except Exception as ex:
            print("  <ERROR reading Replay Gain: %r>" % ex)
        if replaygain_albumdata:
            print("Album ReplayGain: gain=%.2f dB, peak=%.8f" % (replaygain_albumdata.gain, replaygain_albumdata.peak))
        else:
            print("Album ReplayGain: no information")
        if replaygain_trackdata:
            print("Track ReplayGain: gain=%.2f dB, peak=%.8f" % (replaygain_trackdata.gain, replaygain_trackdata.peak))
        else:
            print("Track ReplayGain: no information")

        #from mutagen.easyid3 import EasyID3
        #print(EasyID3.valid_keys.keys())

        tags = mutagen.File(file, easy=True)
        print("TAGS: %s" % str(tags))

        print()
        #tag = stagger.read_tag(file) # or stagger.default_tag()
        #try:
        #    print("Track title: %s" % tag.title)
        #except stagger.errors.NoTagError as ex:
        #    print("Track title: N/A")


if __name__ == "__main__":
   main(sys.argv[1:])