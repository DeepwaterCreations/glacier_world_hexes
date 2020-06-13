#!/usr/bin/env python3
import random
import sys
import pathlib

from PIL import Image, ImageDraw

HEX_FOLDER_NAME = "glacier_world_hexes"
HEX_TEMPLATE_MASK_PATH = "img/hex_template.png"

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
    hex_template_filepath = get_hex_filepath(player_name, hex_type)
    hex_template = generate_image((255,255,255), (128, 128, 255), savepath=hex_template_filepath)
    print("Generated {} for {}".format(hex_template_filepath, player_name))

