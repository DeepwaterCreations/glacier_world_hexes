#!/usr/bin/env python3
import pathlib
import csv

from PIL import Image

from hexgen import HEX_FOLDER_NAME, HEX_SOURCE_FILE_NAME

def get_hex_filepath(filename, player_name):
    folderpath = pathlib.Path.home() / HEX_FOLDER_NAME / player_name
    filepath = folderpath / filename
    return filepath

def mark_completed(filename, player_name, hex_list_filepath=None):
    """Mark off the given file for completion.
    filename - the name of the submitted file.
    player_name - the name of the player who submitted it.
    Returns a tuple containing True or False depending on if the file was accepted and 
        a string telling the bot user what (if anything) went wrong.
    """
    if hex_list_filepath is None:
        hex_list_filepath = pathlib.Path.home() / HEX_FOLDER_NAME / HEX_SOURCE_FILE_NAME

    hex_filepath = get_hex_filepath(filename, player_name)

    with open(hex_list_filepath, mode='r', encoding="utf-8", newline='') as hex_list: 
        reader = csv.DictReader(hex_list, dialect="unix")
        fieldnames = [name.strip().strip('\0') for name in reader.fieldnames]
        hex_assignments = list(reader)

    list_entry = next((entry for entry in hex_assignments if entry["filename"] == filename), None)
    if list_entry is None:
        print("{} attempted to submit {}, but there's no entry for that in the list.".format(player_name, filename))
        return (False, """Wait, my records don't have a '{}' in them. Did you change the filename? As a bot, I'm very 
                        fussy when it comes to pointless bureaucracy. You'd better try again with a file that has the same 
                        filename as the template.
                        """.format(filename))
    else:
        list_entry["completed"] = True

    with open(hex_list_filepath, mode='w', encoding="utf-8", newline='') as hex_source:
        writer = csv.DictWriter(hex_source, fieldnames, dialect="unix")
        writer.writeheader()
        writer.writerows(hex_assignments)

    print("Marked {} as completed by {}.".format(filename, player_name))
    return (True, "")




if __name__ == "__main__":
    pass
