import datetime
import logging

import pandas as pd
from pandas import to_datetime

logger = logging.getLogger('django.request')


class ImportFromExcel():

    def __init__(self, dbname, file_name=None, since=None, cols=None):

        self.dbname = dbname
        self.file_name = file_name
        self.cols = cols

        self.since = since
        if since is None:
            self.since = datetime.date(1999, 1, 1)

        self.data = None
        self.load_data(filename=file_name, nrows=None)
        self.transform_and_filter()

    def load_data(self, filename, skiprows=None, nrows=None):
        """

        :param filename:
        :param skiprows:
        :param nrows:
        :return:
        """

        try:
            self.data = pd.read_excel(filename, skiprows=skiprows, nrows=nrows)
            logger.info(self.data.columns)
            print(self.data.columns)
        except Exception as e:
            logger.error(e)

    def transform_and_filter(self):
        """

        :return:
        """

        if self.cols is not None:
            self.data.rename(columns=self.cols, inplace=True)

        self.data['Date'] = to_datetime(self.data['Date'])

        if self.since is not None:
            self.data = self.data[self.data['Date'] > self.since]


        self.data['cost'] = self.data['price'] - self.data['margin']

        data = self.data.copy()
        data_accounts = self.data.copy()

        if 'Account id' not in self.data.columns:
            data_accounts.drop_duplicates('Account Name', inplace=True)
            data_accounts['Account id'] = data_accounts.index + 1000

            for n in data_accounts['Account Name'].values:
                data.loc[data['Account Name'] == n, 'Account id'] = \
                    data_accounts[data_accounts['Account Name'] == n]['Account id'].values[0]

        self.data = data


if __name__ == "__main__":
    cols = {
        'PRODUCT FAMILY': 'product class',
        'PRODUCT GROUP': 'product line',
        'PRODUCT SUB GROUP': 'product type',
        'Item nr': 'product',
        'POSITION_BEZ1': 'description',
        'Account': 'Account Name',
        'Invoice Date': 'Date',
        'Customer Name': 'Account Name',
        'Customer No_': 'nn---',
        # 'Customer No_': 'Account id',
        'City': 'city',
        'VORGANG_L_PLZ': 'postcode',
        'External Sales Rep': 'kam',
        'POSITION_SUMB': 'goal',
        'Quantity Sold': 'quantity',
        'VORGANG_NR': 'invoice',
        'Price (EUR)': 'price',
        'Margin (EUR)': 'margin',
        'Cost Price/unit (Ex VAT)': 'cost',
        'YEAR': 'Jahr',
    }

    cols = {
        'Kundennr.': 'Account Name',
        'Auftragsnr.': 'invoice',
        # 'Re-/Gu-Nr.': ,
        'Re-/Gu-Datum': 'Date',
        'Artikelnr.': 'product',
        'Artikelgruppennr.': 'product type',
        # 'ME': ,
        'Umsatz VK': 'price',
        'Marge': 'margin',
        'Warengruppennr.': 'product line',
        'Menge': 'quantity',
        # 'Breite': ,
        # 'Positionswert': ,
        # 'Pos.': ,
        # 'F': ,
        # 'Unterkundennr.': ,
        # 'Auftragsposnr.': ,
        # 'Menge ext.': ,
        # 'DEK-Preis': ,
        # 'LEK-Preis': ,
        # 'VK-Preis': ,
        # 'Umsatz EK': ,
        # 'Auftr.Art': ,
        # 'Auftragsartbez.': ,
        # 'Artikel MC Verkauf': ,
        # 'Benutzer': ,
        # 'Gewicht': ,
        # 'PE': ,
        # 'MPVE-Bez': ,
        # 'Menge/Verp.Einheit': ,
        # 'VE Menge': ,
        # 'MC Kunde': ,
        # 'Vertretername': ,
        # 'Sachbearbeiter': ,
        # 'Landkz.': ,
        'Branchennr.': 'product class',
        # 'Branchenbez.': ,
    }

    database = "data_clarus_de"
    filename = '/Users/martin/Documents/cui/accounts/Clarus/ExcelExport_tblFaktStd_201909020919.xlsx'

    importer = ImportFromExcel(database, file_name=filename, cols=cols)

    print(importer.data.columns)
