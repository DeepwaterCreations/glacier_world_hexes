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
            print("Help requested")
        elif subcommand in ["get", "--get", "-g", "g"]:
            print("User wants a hex")
        elif subcommand in ["submit", "--submit", "-s", "s"]:
            print("User wants to submit a hex")
        else:
            print("I dunno what {} is.".format(subcommand))


client.run(TOKEN)
