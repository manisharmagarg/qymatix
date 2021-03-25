import pytest
from api.importer.importer.application.import_product_class_command import ImportProductClassCommand


def test_command_should_have_fqdn_method():

    command = ImportProductClassCommand()
    fqdn = {
        "module": "api.importer.importer.application.import_product_class_handler",
        "handler_class": "ImportProductClassHandler"
    }
    assert command.fqdn == fqdn
