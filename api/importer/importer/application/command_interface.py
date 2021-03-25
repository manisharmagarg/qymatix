from abc import ABCMeta, abstractmethod

class CommandInterface(metaclass=ABCMeta):

    @abstractmethod
    def fqdn(self):
        raise NotImplementedError("Method fqdn should be implemented")