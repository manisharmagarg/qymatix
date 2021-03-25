import datetime

import uploader
from pandas import to_datetime


def upload_products(filename, what=''):
    '''
    '''

    if what == 'class':
        data_cl = uploader.load_data(filename=filename)
        uploader.upload_product_class(dbname=dbname, data=data_cl)

    if what == 'line':
        data_products = uploader.load_data(filename=filename)
        cols = {
            'Invoice Date': 'Date',
            'ARTIKELWG_MASTER': 'product line'
        }
        data_products.rename(columns=cols, inplace=True)

        # data_products['Date'] = to_datetime(data_products['Date'], dayfirst=False, yearfirst=False)
        data_products['Date'] = to_datetime(data_products['Date'])

        # data_products = data_products[data_products['Jahr']==2018]
        # data_products= data_products[(data_products['Jahr']==2018) | (data_products['Jahr']==2017)]
        data_products = data_products[data_products['Date'] > datetime.date(2018, 5, 17)]
        data_products = data_products[data_products['Art'] == 'Verkauf']
        data_products = data_products[data_products['Account id'] < 300000]
        data_products.drop_duplicates('product line', inplace=True)
        uploader.upload_product_line(dbname=dbname, data=data_products)

    if what == 'type':
        data_products = uploader.load_data(filename=filename)
        cols = {
            'Invoice Date': 'Date',
            'Account Id': 'Account id',
            'Item Group': 'product type',
            'ARTIKELWG_MASTER': 'product line'
        }
        data_products.rename(columns=cols, inplace=True)
        # data_products = data_products[data_products['Jahr']==2018]
        # data_products= data_products[(data_products['Jahr']==2018) | (data_products['Jahr']==2017)]

        data_products['Date'] = to_datetime(data_products['Date'])

        # data_products = data_products[data_products['Date']>datetime.date(2018,5,17)]

        # data_products = data_products[data_products['Art']=='Verkauf']
        data_products = data_products[data_products['Account id'] < 300000]
        data_products.drop_duplicates('product type', inplace=True)
        uploader.upload_product_type(dbname=dbname, data=data_products)

    if what == 'products':
        data_products = uploader.load_data(filename=filename)
        cols = {
            'Invoice Date': 'Date',
            'Account Id': 'Account id',
            'Item': 'product',
            'Item Group': 'product type',
            'POSITION_BEZ1': 'description'
        }
        data_products.rename(columns=cols, inplace=True)
        # data_products = data_products[data_products['Jahr']==2018]

        data_products['Date'] = to_datetime(data_products['Date'])
        # data_products = data_products[data_products['Date']>datetime.date(2018,5,17)]

        # data_products = data_products[data_products['Art']=='Verkauf']
        data_products = data_products[data_products['Account id'] < 300000]
        data_products.drop_duplicates('product', inplace=True)

        uploader.upload_products(dbname=dbname, data=data_products)


def upload_customers(filename, what=''):
    '''
    '''
    print("Loading customers from: {}".format(filename))

    data_accounts = uploader.load_data(filename=filename_accounts)

    cols = {
        'ADRESSEN_NAM1': 'Account Name',
        'Account Id': 'Account id',
        'ADRESSEN_ORT': 'city',
        'VORGANG_VERTRETER': 'kam',
        'VORGANG_L_PLZ': 'postcode',
        'Invoice Date': 'Date',
    }

    data_accounts.rename(columns=cols, inplace=True)
    # data_accounts = data_accounts[data_accounts['Jahr']==2018]
    # data_accounts = data_accounts[(data_accounts['Jahr']==2018) | (data_accounts['Jahr']==2017)]

    # data_accounts['Date'] = to_datetime(data_accounts['Date'], dayfirst=False, yearfirst=False)
    data_accounts['Date'] = to_datetime(data_accounts['Date'])
    # data_accounts = data_accounts[data_accounts['Date']>datetime.date(2018,5,17)]

    # data_accounts = data_accounts[data_accounts['Art']=='Verkauf']
    data_accounts = data_accounts[data_accounts['Account id'] < 300000]
    data_accounts.drop_duplicates('Account id', inplace=True)

    uploader.upload_customers(dbname=dbname, data=data_accounts)


def upload_kams(filename, what=''):
    '''
    '''
    print("Loading KAMs from: {}".format(filename))
    data_accounts = uploader.load_data(filename=filename)
    cols = {
        'ADRESSEN_NAM1': 'Account Name',
        'Account Id': 'customer id',
        'ADRESSEN_ORT': 'city',
        'VORGANG_VERTRETER': 'kam',
        'VORGANG_L_PLZ': 'postcode',
        'Invoice Date': 'Date',
    }
    data_accounts.rename(columns=cols, inplace=True)

    data_accounts['Date'] = to_datetime(data_accounts['Date'])
    data_accounts = data_accounts[data_accounts['Date'] > datetime.date(2018, 5, 17)]

    # data_accounts = data_accounts[data_accounts['Jahr']==2018]
    # data_accounts = data_accounts[(data_accounts['Jahr']==2018) | (data_accounts['Jahr']==2017)]

    data_accounts = data_accounts[data_accounts['Art'] == 'Verkauf']
    data_accounts = data_accounts[data_accounts['customer id'] < 300000]
    data_accounts.drop_duplicates('customer id', inplace=True)

    uploader.upload_kam(dbname=dbname, data=data_accounts)


def upload_customers_2(filename, what=''):
    '''
    '''
    print("Loading customers from: {}".format(filename))

    data_accounts = uploader.load_data(filename=filename_accounts)

    cols = {
        'ADRESSEN_NAM1': 'Account Name',
        'Account Id': 'Account id',
        'ADRESSEN_ORT': 'city',
        'VORGANG_VERTRETER': 'kam',
        'VORGANG_L_PLZ': 'postcode',
        'Invoice Date': 'Date',
    }

    data_accounts.rename(columns=cols, inplace=True)

    # data_accounts['Date'] = to_datetime(data_accounts['Date'], dayfirst=False, yearfirst=False)

    data_accounts['Date'] = to_datetime(data_accounts['Date'])
    data_accounts = data_accounts[data_accounts['Date'] > datetime.date(2018, 5, 17)]

    # data_accounts = data_accounts[data_accounts['Jahr']==2018]
    # data_accounts = data_accounts[(data_accounts['Jahr']==2018) | (data_accounts['Jahr']==2017)]
    # data_accounts = data_accounts[data_accounts['Art']=='Verkauf']
    data_accounts = data_accounts[data_accounts['Account id'] < 300000]
    data_accounts.drop_duplicates('Account id', inplace=True)

    uploader.upload_customers(dbname=dbname, data=data_accounts)


def customers(filename, what=''):
    '''
    '''
    print("Loading customers from: {}".format(filename))

    data_accounts = uploader.load_data(filename=filename_accounts)

    cols = {
        'ADRESSEN_NAM1': 'Account Name',
        'Account Id': 'Account id',
        'ADRESSEN_ORT': 'city',
        'VORGANG_VERTRETER': 'kam',
        'VORGANG_L_PLZ': 'postcode',
        'Invoice Date': 'Date',
    }

    data_accounts.rename(columns=cols, inplace=True)

    data_accounts['Date'] = to_datetime(data_accounts['Date'])
    data_accounts = data_accounts[data_accounts['Date'] > datetime.date(2018, 5, 17)]

    # data_accounts = data_accounts[data_accounts['Jahr']==2018]
    # data_accounts = data_accounts[(data_accounts['Jahr']==2018) | (data_accounts['Jahr']==2017)]
    # data_accounts = data_accounts[data_accounts['Art']=='Verkauf']
    data_accounts = data_accounts[data_accounts['Account id'] < 300000]
    data_accounts.drop_duplicates('Account id', inplace=True)

    # uploader.upload_customers(dbname=dbname, data=data_accounts)
    print(data_accounts.columns)

    print(200595 in set(data_accounts['Account id'].values))
    print(201050 in set(data_accounts['Account id'].values))
    print(200885 in set(data_accounts['Account id'].values))
    print(200885 in set(data_accounts['VORGANG_RECHADR'].values))


def upload_sales(filename):
    '''
    '''
    print("Loading sales from: {}".format(filename))
    data_sales = uploader.load_data(filename=filename)
    # print(data_sales)

    cols = {
        'Account Id': 'customer_id',
        'VORGANG_VERTRETER': 'kam',
        'Invoice Date': 'Date',
        'Item': 'product',
        'Price': 'price',
        'Cost': 'cost',
        'Margin': 'margin',
        'VORGANG_MENGE': 'quantity',
        'VORGANG_NR': 'invoice',
        'Invoice Date': 'Date',
    }

    data_sales.rename(columns=cols, inplace=True)
    # print(data_sales[data_sales['Jahr']==2018])
    # data_sales['Date'] = to_datetime(data_sales['Date'], dayfirst=False, yearfirst=True)
    data_sales['Date'] = to_datetime(data_sales['Date'])

    # data_sales = data_sales[data_sales['Date']>=datetime.date(2018,1,1)]
    # data_sales.to_excel(filename.replace('.xlsx', '_2018.xlsx'))

    # data_sales = data_sales[data_sales['Date']>datetime.date(2018,5,17)]
    # data_sales = data_sales[data_sales['Art']=='Verkauf']
    data_sales = data_sales[data_sales['customer_id'] < 300000]

    uploader.upload_sales(dbname=dbname, data=data_sales)


def update_products(filename, skiprows=None):
    '''
    '''

    data = uploader.load_data(filename=filename, skiprows=skiprows)
    cols = {
        'Alte Art.Nr.': 'old_name',
        'AET Art.Nr.': 'new_name',
        'Invoice Date': 'Date',
    }
    data.rename(columns=cols, inplace=True)

    data['Date'] = to_datetime(data['Date'], dayfirst=False, yearfirst=False)

    # data_products = data_products[data_products['Jahr']==2018]
    # data_products= data_products[(data_products['Jahr']==2018) | (data_products['Jahr']==2017)]
    # data_products = data_products[data_products['Art']=='Verkauf']
    # data_products = data_products[data_products['Account id']<300000]
    # data_products.drop_duplicates('product', inplace=True)
    # data['Alte Art.Nr.'] = data['Alte Art.Nr.'].astype(str)

    data['old_name'] = data['old_name'].astype(str)
    data['new_name'] = data['new_name'].astype(str)
    # print(data[:10]['Alte Art.Nr.']=='nan')
    data = data[data['old_name'] != 'nan']
    # data = data[data['old_name'].isin(('894751'))]
    print(data[:10])

    # uploader.update_products(dbname=dbname, data=data)
    uploader.update_products_in_sales(dbname=dbname, data=data)


def upload_plans(dbname, filename, skiprows=None):
    '''
    '''

    data = uploader.load_data(filename=filename, skiprows=skiprows)
    cols = {
        'VORGANG_LIEFADR': 'customer_id',
        # 'VORGANG_RECHADR':'customer_id',
        'VORGANG_VERTRETER': 'kam',
        'Invoice Date': 'Date',
        'Item': 'product',
        'Item Group': 'product type',
        'POSITION_SUMB': 'goal',
        'VORGANG_MENGE': 'quantity',
        'VORGANG_NR': 'invoice',
    }

    data.rename(columns=cols, inplace=True)
    data = data[(data['Jahr'] == 2018)]
    # data = data[(data['Jahr']==2018) | (data['Jahr']==2017)]
    data = data[data['Art'] == 'Verkauf']
    data = data[data['customer_id'] < 300000]
    # data_products.drop_duplicates('product', inplace=True)
    # data['Alte Art.Nr.'] = data['Alte Art.Nr.'].astype(str)
    # print(data.columns)
    # data['old_name'] = data['old_name'].astype(str)
    # data['new_name'] = data['new_name'].astype(str)
    # print(data[:10]['Alte Art.Nr.']=='nan')
    # data = data[data['old_name'] != 'nan']
    # data = data[data['old_name'].isin(('894751'))]
    # print(data[:3])

    uploader.upload_plans(dbname=dbname, data=data)


if __name__ == "__main__":
    dbname = 'qymatix___aet_com'
    dbname = 'qy___test_com'

    local = True
    local = False

    filename = '/home/webuser/users/qy___test_com/data/data_test_2016_1106_2.xlsx'

    # upload_products(filename, what='line')
    # upload_products(filename, what='type')
    # upload_products(filename, what='products')

    filename_accounts = filename
    # upload_customers(filename=filename_accounts)

    # filename_accounts = '/home/webuser/users/aet_at/data/data_AET_QedvUmsatzAdressenPositionenLieferadresse.xls'
    # upload_kams(filename=filename_accounts)

    filename_sales = filename
    upload_sales(filename=filename_sales)

    filename = '/home/webuser/users/aet_at/data/004_AET_ARTIKELSTAMMLISTE_2018-3-19.xlsx'
    # update_products(filename, skiprows=(1))

    # filename = '/home/webuser/users/aet_at/data/data_AET_aedvAngebotAdressenPositionenLieferadresse.xls'
    # upload_plans(dbname, filename)

    # filename_customers = '/home/webuser/users/aet_at/data/data_not_uploaded_AET_Sales_2018-02_A.xlsx'
    # filename_customers = '/home/webuser/users/aet_at/data/data_not_uploaded_AET_Sales_2018-02_A_3.xlsx'
    # data_cust = load_data(filename=filename_customers)
    # id_list = data_cust['customer_id'].drop_duplicates().values
    # print(id_list)
    # upload_customers(dbname=dbname, data=data_accounts, id_list=id_list)
