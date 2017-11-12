from abc import ABCMeta, abstractmethod
import asyncio

class Conversation:
    __metaclass__ = ABCMeta

    @asyncio.coroutine
    @abstractmethod
    def expected_next(self, msg, **kwargs):
        pass

    @asyncio.coroutine
    @abstractmethod
    def apply(self, msg, **kwargs):
        pass
