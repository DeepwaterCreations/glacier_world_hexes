#!/usr/bin/env python3
import os

import discord
from dotenv import load_dotenv

from hexgen import get_hex, SUCCESS, NO_OPEN_HEXES, HIT_QUOTA

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!hex"):
        args = message.content.split()
        if len(args) == 1:
            subcommand = "help"
        else:
            subcommand = args[1]

        if subcommand in ["help", "--help", "-h", "h", "?"]:
            help_message = """***HEXBOT***
            Looking for something to do while we're waiting for players?
            Or just kinda bored?
            Why not contribute some hexes to the campaign map?

            Ask, and Hexbot will deliver a hexagon template to your DMs
            and request a particular type of terrain or map feature.

            Doodle that terrain on the hexagon, using the template's 
            suggested foreground and background colors to help 
            keep things looking consistent (if you want), and send it back. 
            Once you've sent it back, you can request another. (Actually,
            you can do two at a time.)

            I'll use your hex artwork to build the map! The more tile
            variety we have, the prettier it'll look! Maybe!

            Usage: 
            `!hexbot help`: Display this message
            `!hexbot get`: Get a new hex template
            `!hexbot submit`: Use as a comment on your image, send the finished
                image to me and hexbot will mark it off the list
            """
            await message.channel.send(help_message)
        elif subcommand in ["get", "--get", "-g", "g"]:
            player = message.author

            #Generate a hex
            result = get_hex(player.name)
            hex_file = None
            hex_image = None
            dm_message = None
            chat_message = None
            error_message = "Something weird happened. I dunno. Tell SeaWyrm you got `{}`"
            if result[0] == SUCCESS:
                details = result[1]
                dm_message = """
                Here is your template. Foreground/background colors are just a 
                suggestion. Use 'em if you wanna, or colors like them, or just do whatever.
                Please draw a tile with this on it: 
                ***{}***
                When you're done, send it back with `!hex submit` using the same filename
                and size, right here in your DMs."
                """.format(details["hex_type"])
                hex_file = details["filepath"]
                chat_message = "{} received a template for a {} tile. Check your DMs!".format(player, details["hex_type"])
            elif result[0] == NO_OPEN_HEXES:
                chat_message = "Thanks, but we've got all the hexes we need at the moment."
            elif result[0] == HIT_QUOTA:
                chat_message = "You want another hex? Finish what you've got first!"
            else:
                dm_message = error_message.format(result)

            #Send the messages
            if dm_message is not None:
                await player.create_dm()
                if hex_file is not None:
                    hex_image = discord.File(hex_file, filename=hex_file.name)
                await player.dm_channel.send(dm_message, file=hex_image)
            if chat_message is not None:
                await message.channel.send(chat_message)
        elif subcommand in ["submit", "--submit", "-s", "s"]:
            print("User wants to submit a hex")
        else:
            print("I dunno what {} is.".format(subcommand))

# @client.event
# async def 

client.run(TOKEN)
