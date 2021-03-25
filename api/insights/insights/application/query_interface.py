from abc import ABCMeta, abstractmethod


# pylint: disable=too-few-public-methods
class QueryInterface(metaclass=ABCMeta):

    @abstractmethod
    def get_path_and_class_name(self):
        raise NotImplementedError("Method get_path_and_class_name should be implemented")
