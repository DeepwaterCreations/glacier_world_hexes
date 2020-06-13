#!/usr/bin/env python3
import random
import sys
import pathlib
import csv

from PIL import Image, ImageDraw

HEX_FOLDER_NAME = "glacier_world_hexes"
HEX_TEMPLATE_MASK_PATH = "img/hex_template.png"
MAX_HEX_PER_PLAYER = 2

def get_hex_filepath(player_name, hex_type, extension="png"):
    """player_name - the name of the player the hex is being generated for.
    hex_type - the name of the hex terrain.
    Returns a filepath for saving the generated hex template
    """
    #It should go in a subdirectory of the user's home folder, in a sub-subdirectory
    #   named after the player the hex is being generated for
    folderpath = pathlib.Path.home() / HEX_FOLDER_NAME / player_name
    #Create the directories if they don't already exist
    folderpath.mkdir(parents=True, exist_ok=True)

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

    return filepath.expanduser()

    
def generate_image(fg_color, bg_color, savepath):
    """Creates a hexagon template image with two colors.
    fg_color - the color of a circle in the hex's center.
    bg_color - the color surrounding the circle.
    """
    template_mask = Image.open(HEX_TEMPLATE_MASK_PATH)

    #Generate the base image 
    color_bands = [Image.new('L', template_mask.size, color=bg_color[color_idx]) for color_idx in range(3)]
    background = Image.merge("RGB", color_bands)

    #Apply alpha mask
    alpha = template_mask.getchannel('A')
    background.putalpha(alpha)
    
    #Draw the foreground color
    #We'll create it as a separate image and then blend,
    #for the sake of being fancy.
    foreground = Image.new('RGBA', template_mask.size, color=(0,0,0,0))
    draw = ImageDraw.Draw(foreground)

    def add_ellipse(color, r, a):
        c_x = template_mask.width/2
        c_y = template_mask.height/2
        draw.ellipse([(c_x - r, c_y - r),(c_x + r, c_y + r)], fill=(fg_color + tuple([a])))

    add_ellipse(fg_color, 28, 64)
    add_ellipse(fg_color, 24, 128)
    add_ellipse(fg_color, 20, 255)
    
    template = Image.alpha_composite(background, foreground)
    template.save(savepath)


if __name__ == "__main__":

    try:
        source_file = sys.argv[1]
        player_name = sys.argv[2]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <hex list file> <player name>") 

    #Get hex list from file
    with open(source_file, mode='r', encoding="utf-8", newline='') as hex_source: 
        reader = csv.DictReader(hex_source, dialect="unix")
        fieldnames = [name.strip().strip('\0') for name in reader.fieldnames]
        hex_assignments = list(reader)
        
    #Check if the player has hit their quota
    #TODO: Use the contents of the player folder, not the csv, since there
    #   might be multiple csvs.
    already_assigned = filter(lambda d: d["assigned"].strip() == player_name, hex_assignments)
    if len(list(already_assigned)) >= MAX_HEX_PER_PLAYER:
        print("You have enough for now, don't you think?")
        sys.exit(0)

    #Pick randomly from the unpicked rows
    unassigned = list(filter(lambda d: d["assigned"].strip() == "", hex_assignments))
    if len(unassigned) == 0:
        print("All the hexes are spoken for!")
        sys.exit(0)
    else:
        new_hex = random.choice(unassigned)

    #Assign the given hex to the player in the csv
    new_hex["assigned"] = player_name

    #Write new assignment back to the file
    with open(source_file, mode='w', encoding="utf-8", newline='') as hex_source:
        writer = csv.DictWriter(hex_source, fieldnames, dialect="unix")
        writer.writeheader()
        writer.writerows(hex_assignments)

    hex_type = new_hex["terrain"].strip().strip('\0')
    hex_template_filepath = get_hex_filepath(player_name, hex_type)

    fg_color = (int(new_hex['fg_r']), int(new_hex['fg_g']), int(new_hex['fg_b']))
    bg_color = (int(new_hex['bg_r']), int(new_hex['bg_g']), int(new_hex['bg_b']))
    hex_template = generate_image(fg_color, bg_color, savepath=hex_template_filepath)

    print("Generated {} for {}".format(hex_template_filepath, player_name))

