import pytest
from api.importer.importer.application.import_kam_command import ImportKamCommand
import os


def test_command_should_have_fqdn_method():

    filename = os.path.realpath(__file__)
    mappings = {'a': 'b'}

    command = ImportKamCommand(filename, mappings)
    fqdn = {
        "module": "api.importer.importer.application.import_kam_handler",
        "handler_class": "ImportKamHandler"
    }
    assert command.fqdn == fqdn
