#!/usr/bin/python3

# LogBot
# Simple discord server logging bot

__title__ = 'logbot-discord'
__author__ = 'Goopypanther'
__license__ = 'GPL'
__copyright__ = 'Copyright 2018 Goopypanther'
__version__ = '0.1'

import discord
import os
import errno
import datetime as datetime


# Fail if api not set
try:
    discord_token = os.environ["DISCORD_API_KEY"]
except KeyError:
    print("Discord api key not set.")
    quit()

# Set default logfile path if none is specified
try:
    logfile_path = os.environ["LOGBOT_LOG_PATH"]
except KeyError:
    logfile_path = "./logbot-logs"

client = discord.Client()


## Checks for file path and creates it if it does not exist
#
# @param file_path String containing path to check
def ensure_path(file_path):
    directory = os.path.dirname(file_path)
    
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


@client.event
async def on_message(message):

    path = logfile_path + "/" + message.server.id + "/" + message.channel.id + "/" + message.timestamp.strftime("%F") + ".txt"
    ensure_path(path) # Create path if it does not exist

    logline = message.timestamp.strftime("%F-%H-%M-%S") + " " + message.server.name + ":" + message.channel.name + ":" + message.author.name + "#" + message.author.discriminator + ": " + message.content + "\n"

    with open(path, 'a') as log:
        log.write(logline)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(discord_token)
