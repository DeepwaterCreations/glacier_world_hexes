#!/usr/bin/env python3
import os

import discord
from dotenv import load_dotenv

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
            print("User wants a hex")
        elif subcommand in ["submit", "--submit", "-s", "s"]:
            print("User wants to submit a hex")
        else:
            print("I dunno what {} is.".format(subcommand))


client.run(TOKEN)
