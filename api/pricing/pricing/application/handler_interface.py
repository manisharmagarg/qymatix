from abc import ABCMeta, abstractmethod

class HandlerInterface(metaclass=ABCMeta):

    @abstractmethod
    def handle(self):
        pass