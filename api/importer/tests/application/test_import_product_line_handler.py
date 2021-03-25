from api.importer.importer.application.import_product_line_handler import ImportProductLineHandler
from api.importer.importer.application.import_product_line_command import ImportProductLineCommand
import pytest
from unittest.mock import patch


def test_handler_initializes():

    command = ImportProductLineCommand()
    handler = ImportProductLineHandler(command)

    isinstance(handler.command, ImportProductLineCommand)
    # assert handler.query.product_id == 1
