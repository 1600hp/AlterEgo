import discord
import asyncio

from interpretation import Interpretation
from discord_utils import slow_send
from croissant.calendar import Calendar
from event_planner import EventPlanner

class CalendarManager(Interpretation):
    def __init__(self, client, fname):
        self.client = client
        self.calendar = Calendar(fname)
        
    @asyncio.coroutine
    def rate(self, msg, tokens=None, me=None, **kwargs):
        if not me:
            return 0
        if not me.mentioned_in(msg):
            return 0
        rating = 0
        if "schedule" in tokens:
            rating += 0.75
        if "event" in tokens or "events" in tokens:
            rating += 0.75
        return rating

    @asyncio.coroutine
    def apply(self, msg, tokens=None, **kwargs):
        yield from slow_send(self.client, msg.channel, "Sure, I'll pm you for the details.")
        yield from slow_send(self.client, msg.author, "What would you like to name your new event?")
        return EventPlanner(self.client, msg.author, self.calendar)
