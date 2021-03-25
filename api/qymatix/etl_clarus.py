import datetime

from api.qymatix import uploader
# from . import file_uploader


class EtlBase():

    def __init__(self, dbname, file_name=None, since=None):
        import datetime
        from api.qymatix import uploader

        self.dbname = dbname
        self.file_name = file_name

        self.since = since
        if since is None:
            self.since = datetime.date(1999, 1, 1)

        self.data = uploader.load_data(filename=file_name, nrows=None)
        self.transform_and_filter()

    def transform_and_filter(self, data=None):
        """

        :return:
        """

        from pandas import to_datetime

        cols = {
            # 'Kundennr.': 'Account Name',
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
            'MC Kunde': 'Account Name',
            # 'Vertretername': ,
            # 'Sachbearbeiter': ,
            # 'Landkz.': ,
            'Branchennr.': 'product class',
            # 'Branchenbez.': ,
        }

        self.data.rename(columns=cols, inplace=True)

        self.data['Date'] = to_datetime(self.data['Date'], dayfirst=True)

        if self.since is not None:
            self.data = self.data[self.data['Date'] > self.since]

        # data = data[(data['Jahr'] == 2018)]
        # data = data[data['Art'] == 'Verkauf']
        # data = data[data['customer_id'] < 300000]

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

    def upload_products_class(self, file_name_product_class=None):
        """
        """
        from api.qymatix import uploader
        if file_name_product_class is not None:
            data = uploader.load_data(filename=file_name_product_class)
        else:
            data = self.data

        data.drop_duplicates('product class', inplace=True)
        uploader.upload_product_class(dbname=self.dbname, data=data)

    def upload_products_line(self, file_name_product_line=None):
        """
        """
        from api.qymatix import uploader
        if file_name_product_line is not None:
            data = uploader.load_data(filename=file_name_product_line)
            self.transform_and_filter()
        else:
            data = self.data

        data.drop_duplicates('product line', inplace=True)
        uploader.upload_product_line(dbname=self.dbname, data=data)

    def upload_products_type(self, file_name_product_type=None):
        """
        """
        from api.qymatix import uploader
        if file_name_product_type is not None:
            data = uploader.load_data(filename=file_name_product_type)
            self.transform_and_filter()
        else:
            data = self.data

        data.drop_duplicates('product type', inplace=True)
        uploader.upload_product_type(dbname=self.dbname, data=data)

    def upload_products(self, file_name_products=None):
        """
        """
        from api.qymatix import uploader
        if file_name_products is not None:
            data = uploader.load_data(filename=file_name_products)
            self.transform_and_filter(data)
        else:
            data = self.data

        data.drop_duplicates('product', inplace=True)
        uploader.upload_products(dbname=self.dbname, data=data)

    def upload_customers(self, file_name_customers=None):
        """
        """
        from api.qymatix import uploader
        if file_name_customers is not None:
            data = uploader.load_data(filename=file_name_customers)
        else:
            data = self.data

        if 'Account id' in data.keys():
            data.drop_duplicates('Account id', inplace=True)
        else:
            data.drop_duplicates('Account Name', inplace=True)

        uploader.upload_customers(dbname=self.dbname, data=data)

    def upload_kams(self, file_name_kams=None):
        """

        :param what:
        :return:
        """
        from api.qymatix import uploader
        if file_name_kams is not None:
            data = uploader.load_data(filename=file_name_kams)
        else:
            data = self.data

        data.drop_duplicates('kam', inplace=True)
        uploader.upload_kam(dbname=self.dbname, data=data)

    def upload_sales(self, file_name_sales=None):
        """

        :param file_name_sales:
        :return:
        """
        from api.qymatix import uploader

        if file_name_sales is not None:
            data_sales = uploader.load_data(filename=file_name)
        else:
            data_sales = self.data

        uploader.upload_sales(dbname=self.dbname, data=data_sales)

    def upload_plans(self, file_name_plans=None, skiprows=None):
        """

        :param file_name_plans:
        :param skiprows:
        :return:
        """
        from api.qymatix import uploader

        if file_name_plans is not None:
            data = uploader.load_data(filename=file_name_plans, skiprows=skiprows)
        else:
            data = self.data

        data.drop_duplicates('plan name', inplace=True)
        uploader.upload_plans(dbname=self.dbname, data=data)

file_name = '/var/www/qyapp/ExcelExport_tblFaktStd_201909020919.xlsx'

database_name = 'clarus_de'

etl = EtlBase(database_name, file_name)

# print("Importing product classes...")
# etl.upload_products_class()
#
# print('\n')
# print('\n')
# print("Importing product lines...")
# etl.upload_products_line()
#
# print('\n')
# print('\n')
# print("Importing product types...")
# etl.upload_products_type()
#
# print('\n')
# print('\n')
# print("Importing products...")
# etl.upload_products()

# print("uploading customers....")
# etl.upload_customers()
# etl.upload_kams()

print("uploading sales....")
etl.upload_sales()


# if __name__ == "__main__":
#
#     file_name = '/var/www/qyapp/pfisterer_file_000001.xlsx'
#
#     database_name = 'data_pfisterer_de'
#
#     etl = EtlBase(database_name, file_name)
#
#     print("Importing product classes...")
#     etl.upload_products_class()

    # etl.upload_products_line()
    # print("uploading product types....")
    # etl.upload_products_type()
    # print("uploading products....")
    # etl.upload_products()

    # print("uploading customers....")
    # etl.upload_customers()
    # etl.upload_kams()
    # print("uploading sales....")
    # etl.upload_sales()



