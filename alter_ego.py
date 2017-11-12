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
from calendar_manager import CalendarManager

with open("conf.json") as conf:
    params = json.load(conf)

token = params["token"]

client = discord.Client()
webfetcher = WebFetcher(client)
reminder = Reminder(client)
cal_manager = CalendarManager(client, params["calendar_path"])

interpreters = [webfetcher, reminder, cal_manager]
conversations = []

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

    cal_manager.calendar.save_file()
    yield from slow_send(client, BOTSPAM, "Alter Ego, checking in! Please ignore me for now.".format(ME))

@client.event
@asyncio.coroutine
def on_message(msg):
    if msg.author == ME: return  # Alter Ego should not respond to her own messages

    # Check non-linguistic commands
    caught = yield from check_hard_commands(msg)
    if caught: return

    # Register the sentence with the users Markov session
    text = msg.content
    MARKOV.register(msg.author.id, text)

    tokens = tokenize(text)

    # Check ongoing conversations
    matches = []
    for conv in conversations:
        match = yield from conv.expected_next(msg, tokens=tokens, me=ME)
        if match:
            conv.apply(msg, tokens=tokens, me=ME)
            return

    # Check linguistic commands
    rates = []
    for interp in interpreters:
        rate = yield from interp.rate(msg, tokens=tokens, me=ME)
        rates.append(rate)
    
    # Apply match
    if max(rates) > 0:
        interp = interpreters[rates.index(max(rates))]
        new_conv = yield from interp.apply(msg, tokens=tokens, loop=client.loop)
        if new_conv:
            conversations.append(new_conv)

try:
    client.run(token)
except: 
    pass
finally:
    sys.exit(reboot_on_shutdown)
