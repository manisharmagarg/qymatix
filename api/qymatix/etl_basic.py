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

        if 'pfisterer' in self.dbname:
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
        else:
            cols = {
                'ARTIKELWG_MASTER': 'product line',
                'Item': 'product',
                'Item Group': 'product type',
                'POSITION_BEZ1': 'description',
                'Account': 'Account Name',
                'Invoice Date': 'Date',
                'ADRESSEN_NAM1': 'Account Name',
                'ADRESSEN_KEY': 'customer id',
                'ADRESSEN_ORT': 'city',
                'VORGANG_L_PLZ': 'postcode',
                'VORGANG_LIEFADR': 'customer_id',
                'VORGANG_VERTRETER': 'kam',
                'VORGANG_DATUM': 'Date',
                'POSITION_ARTNR': 'product',
                'ARTIKEL_WG': 'product type',
                'POSITION_SUMB': 'goal',
                'VORGANG_MENGE': 'quantity',
                'VORGANG_NR': 'invoice',
                'Account id': 'customer_id',
                'VORGANG_RECHADR':'customer_id',
                'POSITION_SUMN': 'price',
                'POSITION_SUME': 'cost',
                'YEAR': 'Jahr',
            }

        import datetime
        if 'Date' not in self.data.columns:
            self.data['Date'] = self.data.apply(lambda x: datetime.date(x['Sales Year'], x['Sales Month'], x['Sales Day of Month']), axis=1)
        else:
            self.data['Date'] = to_datetime(self.data['Date'])

        if self.since is not None:
            self.data = self.data[self.data['Date'] > self.since]

        self.data.rename(columns=cols, inplace=True)
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

file_name = '/var/www/qyapp/pfisterer_000001.xlsx'

database_name = 'pfisterer_de'

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



