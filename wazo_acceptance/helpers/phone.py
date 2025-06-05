from abc import ABC, abstractmethod

class Phone(ABC):

    @abstractmethod
    def call(self, exten):
        pass

    @abstractmethod
    def hangup(self):
        pass