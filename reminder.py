import discord
import asyncio
from time import localtime, strftime

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
    def rate(self, msg, tokens=None, me=None, **kwargs):
        if not me:
            return 0
        if not me.mentioned_in(msg):
            return 0
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
            time_output.append("{} hour".format(hours))
            if hours != 1:
                time_output[-1] += "s"
        if minutes:
            time_output.append("{} minute".format(minutes))
            if minutes != 1:
                time_output[-1] += "s"
        if seconds:
            time_output.append("{} second".format(seconds))
            if seconds != 1:
                time_output[-1] += "s"

        send_time = localtime()
        yield from slow_send(self.client, msg.channel, prefix + ", ".join(time_output) + ".")
        yield from asyncio.sleep(seconds + minutes * 60 + hours * 360)
        yield from self.reminder_callback(" ".join(reminder), msg.author, send_time)

    @asyncio.coroutine
    def reminder_callback(self, reminder, target, send_time):
        if reminder:
            reminder = " " + reminder

        now = localtime()
        same_day = (now.tm_year == send_time.tm_year) \
                and (now.tm_mon == send_time.tm_mon) \
                and (now.tm_mday == send_time.tm_mday)
        time_format = "%I:%M %p" if same_day else "%A %I:%M %p"
        content = ["This is a reminder", reminder, ". [Set at ", strftime(time_format, send_time), "]"]

        yield from slow_send(self.client, target, "".join(content))
