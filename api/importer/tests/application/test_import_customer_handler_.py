from api.importer.importer.application.import_customer_handler import ImportCustomerHandler
from api.importer.importer.application.import_customer_command import ImportCustomerCommand
import pytest
from unittest.mock import patch
import os


def test_handler_initializes():

    filename = os.path.realpath(__file__)
    mappings = {'a': 'b'}
    command = ImportCustomerCommand(filename, mappings)
    handler = ImportCustomerHandler(command)

    isinstance(handler.command, ImportCustomerCommand)

    # with pytest.raises(ValueError, match=r".*Price cannot be negative.*"):
