from abc import ABCMeta, abstractmethod


# pylint: disable=too-few-public-methods
class HandlerInterface(metaclass=ABCMeta):

    @abstractmethod
    def handle(self):
        raise NotImplementedError("Method handle should be implemented")
