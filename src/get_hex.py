#!/usr/bin/env python3
import random
import sys
import pathlib

HEX_FOLDER_NAME = "glacier_world_hexes"

def write_hex_template(player_name, hex_type):
    """player_name - the name of the player the hex is being generated for.
    Writes a blank hex with an appropriate filename to the player folder.
    Returns the local filepath to the file.
    """

    #Generate the file path
    #It should go in a subdirectory of the user's home folder, in a sub-subdirectory
    #   named after the player the hex is being generated for
    folderpath = pathlib.Path.home() / HEX_FOLDER_NAME / player_name
    #Create the directories if they don't already exist
    folderpath.mkdir(parents=True, exist_ok=True)

    extension = "png"
    number = 0
    filepath = None
    #Make sure our file path has a unique number by incrementing until we find one that doesn't exist
    while filepath is None or filepath.exists():
        if filepath is not None:
            print("Found existing file: {}".format(filepath))
        filename = "hex_{hex_type}_{player_name}_{number}.{extension}" \
            .format(hex_type=hex_type, player_name=player_name, number=number, extension=extension)
        filepath = folderpath / filename
        number += 1

    #Create the file
    try:
        filepath.touch(exist_ok=False) 
    except ValueError:
        print("Does {} exist? {}".format(str(filepath), filepath.exists()))
        raise SystemExit("Couldn't create {}".format(filepath))

    return filepath.expanduser()

if __name__ == "__main__":

    try:
        source_file = sys.argv[1]
        player_name = sys.argv[2]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <hex list file> <player name>") 

    with open(source_file, mode='r+') as hex_source: 
        needed_hexes = hex_source.readlines()

        if len(needed_hexes) == 0:
            print("All hexes accounted for!")
            sys.exit(0)

        new_hex = random.choice(needed_hexes)
        needed_hexes.remove(new_hex)
        hex_source.truncate(0)
        hex_source.writelines(needed_hexes)


    hex_type = new_hex.strip().strip('\0')
    hex_template_filepath = write_hex_template(player_name, hex_type)
    print("Generated {} for {}".format(hex_template_filepath, player_name))

