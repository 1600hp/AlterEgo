#!/usr/bin/env python3

import sys
import discord
import asyncio
import time
import json

from web_fetcher import WebFetcher
from dual_markov import DualMarkov
from discord_utils import slow_send, tokenize
from reminder import Reminder

with open("conf.json") as conf:
    params = json.load(conf)

token = params["token"]

client = discord.Client()
webfetcher = WebFetcher(client)
reminder = Reminder(client)

interpreters = [webfetcher, reminder]

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

    yield from slow_send(client, BOTSPAM, "Alter Ego, checking in! Please ignore me for now.".format(ME))

@client.event
@asyncio.coroutine
def on_message(msg):
    if msg.author == ME: return  # Alter Ego should not respond to her own messages

    caught = yield from check_hard_commands(msg)
    if caught: return

    text = msg.content
    MARKOV.register(msg.author.id, text)

    tokens = tokenize(text)

    rates = []
    for interp in interpreters:
        rate = yield from interp.rate(msg, tokens=tokens, me=ME)
        rates.append(rate)
    interp = interpreters[rates.index(max(rates))]
    yield from interp.apply(msg, tokens=tokens, loop=client.loop)

try:
    client.run(token)
except: 
    pass
finally:
    sys.exit(reboot_on_shutdown)
