from api.importer.importer.application.import_product_class_handler import ImportProductClassHandler
from api.importer.importer.application.import_product_class_command import ImportProductClassCommand
import pytest
from unittest.mock import patch


def test_handler_initializes():

    command = ImportProductClassCommand()
    handler = ImportProductClassHandler(command)

    isinstance(handler.command, ImportProductClassCommand)
    # assert handler.query.product_id == 1


@pytest.mark.skip(reason="no way of currently testing this")
def test_handler_handle():

    command = ImportProductClassCommand()
    handler = ImportProductClassHandler(command)

    class_to_mock = 'api.importer.importer.domain.ppb.ppb.PPB.calculate'
    with patch(class_to_mock) as mocked_ppb:
        handler.handle()
        mocked_ppb.assert_called_once()
