from abc import ABCMeta, abstractmethod
import asyncio

class Interpretation:
    __metaclass__ = ABCMeta

    @asyncio.coroutine
    @abstractmethod
    def rate(self, msg):
        pass

    @asyncio.coroutine
    @abstractmethod
    def apply(self, msg, **kwargs):
        pass
