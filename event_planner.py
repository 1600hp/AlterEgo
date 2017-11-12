import asyncio

from conversation import Conversation
from discord_utils import slow_send

class EventPlanner(Conversation):
    def __init__(self, client, author, calendar):
        self.author = author
        self.calendar = calendar
        self.client = client
        self.slow_send(client, author, "What would you like to name your new event?")

    @asyncio.coroutine
    @abstractmethod
    def expected_next(self, msg, **kwargs):
        pass

    @asyncio.coroutine
    @abstractmethod
    def apply(self, msg, **kwargs):
        pass
