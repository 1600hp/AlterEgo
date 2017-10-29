#!/usr/bin/env python3

import sys
import discord
import asyncio
import time
import json

from web_fetcher import WebFetcher
from dual_markov import DualMarkov

with open("conf.json") as conf:
    params = json.load(conf)

token = params["token"]

client = discord.Client()
webfetcher = WebFetcher()

reboot_on_shutdown = 0

@asyncio.coroutine
def shutdown():
    yield from client.logout()

@asyncio.coroutine
def check_hard_commands(msg):
    global reboot_on_shutdown
    text = msg.content
    if "$reboot" in text:
        yield from shutdown()
        reboot_on_shutdown = 1
        return True
    elif "$shutdown" in text:
        yield from shutdown()
        return True
    else: return False

@asyncio.coroutine
def slow_send(dest, content=None, delay=1, tts=False, embed=None):
    yield from client.send_typing(dest)
    time.sleep(delay)
    yield from client.send_message(dest, content=content, tts=tts, embed=embed)

@client.event
@asyncio.coroutine
def on_ready():
    global SERVER
    global GENERAL
    global BOTSPAM
    global ME
    global MARKOV
    SERVER = client.get_server(params["server"])
    GENERAL = SERVER.get_channel(params["general"])
    BOTSPAM = SERVER.get_channel(params["botspam"])
    ME = client.user
    MARKOV = DualMarkov([m.id for m in SERVER.members])

    yield from slow_send(BOTSPAM, "Alter Ego, checking in! Please ignore me for now.".format(ME))

@client.event
@asyncio.coroutine
def on_message(msg):
    if msg.author == ME: return  # Alter Ego should not respond to her own messages

    caught = yield from check_hard_commands(msg)
    if caught: return

    text = msg.content
    MARKOV.register(msg.author.id, text)

    if webfetcher.rate(msg) > 0:
        webfetcher.apply(msg)
        return

    if "alter" in text.lower():
        yield from slow_send(msg.channel, 
            "Hello!  I am in the process of being rebuilt.  I'll have more to say later, promise.")

try:
    client.run(token)
except: 
    pass
finally:
    sys.exit(reboot_on_shutdown)
