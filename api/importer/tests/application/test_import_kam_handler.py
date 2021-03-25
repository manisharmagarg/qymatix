from api.importer.importer.application.import_kam_handler import ImportKamHandler
from api.importer.importer.application.import_kam_command import ImportKamCommand
import pytest
from unittest.mock import patch
import os


def test_handler_initializes():

    filename = os.path.realpath(__file__)
    mappings = {'a': 'b'}
    command = ImportKamCommand(filename, mappings)
    handler = ImportKamHandler(command)

    isinstance(handler.command, ImportKamCommand)

    # with pytest.raises(ValueError, match=r".*Price cannot be negative.*"):
