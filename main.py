#!/bin/python3

import argparse
import sqlite3
import os
import shutil

argument_parser = argparse.ArgumentParser(
    prog="python main.py",
    description="Link and name your quaver maps to another folder",
)
argument_parser.add_argument("--verbose", "-v", action='store_true',
            help="show outputted files in output")
argument_parser.add_argument("--quaver-path",
            help="the path quaver is installed at",
)
argument_parser.add_argument("--output-path",
            help="the path to output the sound files",
)
argument_parser.add_argument("--format",
            help="the format to use when naming the output files,"
            + " defaults to \"{{ARTIST}} - {{TITLE}}\"",
            default="{{ARTIST}} - {{TITLE}}",
)

cmd_args = argument_parser.parse_args()

if cmd_args.quaver_path:
    quaver_path = cmd_args.quaver_path
else:
    import platform
    match platform.system():
        case 'Windows':
            quaver_path = 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Quaver'
        case 'Linux':
            quaver_path = '~/.local/share/Steam/steamapps/common/Quaver'
        case _:
            print("FATAL: Unable to guess your quaver install," 
                  + "try manually specifying it with --quaver-path")
            quit(1)
    
    print(f"Quaver path not specified, guessing {quaver_path}")

quaver_path = os.path.expanduser(quaver_path)

if cmd_args.output_path:
    output_path = cmd_args.output_path
else:
    output_path = os.curdir
    print("Output path not specified, guessing current working directory")

db_path = os.path.join(quaver_path, "quaver.db")

if not os.path.exists(db_path):
    if cmd_args.quaver_path:
        print("FATAL: Invalid quaver install, try another")
    else:
        print("FATAL: Unable to guess your quaver install," 
            + "try manually specifying it with --quaver-path")
    quit(1)

connection = sqlite3.connect(db_path)
cursor = connection.cursor()
cursor.execute("SELECT Title, Artist, Directory, AudioPath FROM Map GROUP BY Directory")
songs = cursor.fetchall()
cursor.close()
connection.close()

copy_used = False
for song in songs:
    # Sanitize song name and artist
    bad_chars = ['/','\\',':','<','>','?','|','*','"']

    song_title = song[0]
    for bad_char in bad_chars:
        song_title = song_title.replace(bad_char,' ')

    song_artist = song[1]
    for bad_char in bad_chars:
        song_artist = song_artist.replace(bad_char,' ')
    

    output_file = cmd_args.format + ".mp3"
    output_file = output_file.replace('{{ARTIST}}', song_artist)
    output_file = output_file.replace('{{TITLE}}', song_title)

    source_file = os.path.join(quaver_path, 'Songs', song[2], song[3])
    output_file = os.path.join(output_path, output_file)

    if cmd_args.verbose:
        print(source_file + " -> " + output_file)

    try:
        try:
            os.symlink(
                source_file,
                output_file
            )
        except OSError:
            if cmd_args.verbose:
                print("WARN: Insufficient permission to symlink, copying")
            copy_used = True
            shutil.copy(
                source_file,
                output_file
            )
    except FileExistsError:
        if cmd_args.verbose:
            print("The file already exists, skipping")
        continue
    except FileNotFoundError:
        print(f"WARN: Failed to copy {source_file}, file does not exist")

if copy_used:
    print("WARN: You don't have permission to create symbolic links,"
          + " the files were copied instead")

print("Finished " + str(len(songs)) + " songs")