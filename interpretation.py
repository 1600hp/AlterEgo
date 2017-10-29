from abc import ABCMeta, abstractmethod

class Interpretation:
    __metaclass__ = ABCMeta

    @abstractmethod
    def rate(self, msg):
        pass

    @abstractmethod
    def apply(self, msg):
        pass
