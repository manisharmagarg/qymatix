from api.importer.importer.application.bus import Bus
from api.importer.importer.application.import_product_class_command import ImportProductClassCommand
import pytest
from unittest.mock import patch


# @pytest.fixture(autouse=True)
def test_bus_finds_handler():

    command = ImportProductClassCommand(1)
    bus = Bus(command)

    class_to_mock = 'api.importer.importer.application.import_product_class_handler.ImportProductClassHandler'
    with patch(class_to_mock) as mocked_handler:
        bus.dispatch()
        mocked_handler.assert_called_once()
