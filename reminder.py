import discord
import asyncio

from interpretation import Interpretation
from discord_utils import slow_send

class Reminder(Interpretation):
    alias = {
        "one":1,
        "two":2,
        "three":3,
        "four":4,
        "five":5,
        "six":6,
        "seven":7,
        "eight":8,
        "nine":9,
        "ten":10,
        "eleven":11,
        "twelve":12,
        "thirteen":13,
        "fourteen":14,
        "fifteen":15,
        "sixteen":16,
        "seventeen":17,
        "eighteen":18,
        "nineteen":19,
        "twenty":20,
        "thirty":30
    }

    def __init__(self, client):
        self.client = client
        
    @asyncio.coroutine
    def rate(self, msg, tokens=None, **kwargs):
        return 1 if ("reminder" in tokens or "remind" in tokens) else 0

    @asyncio.coroutine
    def apply(self, msg, tokens=None, **kwargs):
        last_num = None
        reminder = []
        hours = 0
        minutes = 0
        seconds = 0
        recording = False
        recording_number = False
        for t in tokens:
            try:
                converted = int(t)
            except ValueError:
                converted = None

            if t == "\"":
                recording = not recording
            elif recording:
                reminder.append(t)
            elif t in self.alias:
                last_num = self.alias[t]
            elif converted is not None:
                last_num = converted
            elif t == "hours" or t == "hour":
                hours = last_num if last_num else 1
                last_num = None
            elif t == "minutes" or t == "minute":
                minutes = last_num if last_num else 1
                last_num = None
            elif t == "seconds" or t == "second":
                seconds = last_num if last_num else 1
                last_num = None
        if last_num:
            minutes = last_num
        if hours + minutes + seconds == 0:
            hours = 1

        if len(reminder):
            prefix = "I will remind you " + " ".join(reminder) + " in "
        else:
            prefix = "I will remind you in "

        time_output = []
        if hours:
            time_output.append("{} hours".format(hours))
        if minutes:
            time_output.append("{} minutes".format(minutes))
        if seconds:
            time_output.append("{} seconds".format(seconds))

        yield from slow_send(self.client, msg.channel, prefix + ", ".join(time_output) + ".")
        
