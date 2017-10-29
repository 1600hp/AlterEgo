import discord
import asyncio

from interpretation import Interpretation
from discord_utils import slow_send

class Reminder(Interpretation):
    def __init__(self, client):
        self.client = client
        
    @asyncio.coroutine
    def rate(self, msg):
        pass

    @asyncio.coroutine
    def apply(self, msg, **kwargs):
        pass
