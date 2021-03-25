import datetime

import uploader
from pandas import to_datetime


def upload_products(filename, what='', since=datetime.date(2000, 1, 1)):
    '''
    '''

    if what == 'class':
        data_cl = uploader.load_data(filename=filename)
        uploader.upload_product_class(dbname=dbname, data=data_cl)

    if what == 'line':
        data_products = uploader.load_data(filename=filename)
        cols = {
            'VORGANG_DATUM': 'Date',
            'ADRESSEN_KEY': 'Account id',
            'ARTIKELWG_MASTER': 'product line'
        }
        data_products.rename(columns=cols, inplace=True)

        # data_products['Date'] = to_datetime(data_products['Date'], dayfirst=False, yearfirst=False)
        data_products['Date'] = to_datetime(data_products['Date'])

        # data_products = data_products[data_products['Jahr']==2018]
        # data_products= data_products[(data_products['Jahr']==2018) | (data_products['Jahr']==2017)]
        data_products = data_products[data_products['Date'] > since]
        data_products = data_products[data_products['Art'] == 'Verkauf']
        data_products = data_products[data_products['Account id'] < 300000]
        data_products.drop_duplicates('product line', inplace=True)
        uploader.upload_product_line(dbname=dbname, data=data_products)

    if what == 'type':
        data_products = uploader.load_data(filename=filename)
        cols = {
            'VORGANG_DATUM': 'Date',
            'ADRESSEN_KEY': 'Account id',
            'ARTIKEL_WG': 'product type',
            'ARTIKELWG_MASTER': 'product line'
        }
        data_products.rename(columns=cols, inplace=True)
        # data_products = data_products[data_products['Jahr']==2018]
        # data_products= data_products[(data_products['Jahr']==2018) | (data_products['Jahr']==2017)]

        data_products['Date'] = to_datetime(data_products['Date'])

        data_products = data_products[data_products['Date'] > since]

        data_products = data_products[data_products['Art'] == 'Verkauf']
        data_products = data_products[data_products['Account id'] < 300000]
        data_products.drop_duplicates('product type', inplace=True)
        uploader.upload_product_type(dbname=dbname, data=data_products)

    if what == 'products':
        data_products = uploader.load_data(filename=filename)
        cols = {
            'VORGANG_DATUM': 'Date',
            'ADRESSEN_KEY': 'Account id',
            'POSITION_ARTNR': 'product',
            'ARTIKEL_WG': 'product type',
            'POSITION_BEZ1': 'description'
        }
        data_products.rename(columns=cols, inplace=True)
        # data_products = data_products[data_products['Jahr']==2018]

        data_products['Date'] = to_datetime(data_products['Date'])
        data_products = data_products[data_products['Date'] > since]

        data_products = data_products[data_products['Art'] == 'Verkauf']
        data_products = data_products[data_products['Account id'] < 300000]
        data_products.drop_duplicates('product', inplace=True)

        uploader.upload_products(dbname=dbname, data=data_products)


def upload_customers(filename, what='', since=datetime.date(2000, 1, 1)):
    '''
    '''
    print("Loading customers from: {}".format(filename))

    data_accounts = uploader.load_data(filename=filename_accounts)

    cols = {
        'ADRESSEN_NAM1': 'Account Name',
        'ADRESSEN_KEY': 'Account id',
        'ADRESSEN_ORT': 'city',
        'VORGANG_VERTRETER': 'kam',
        'VORGANG_L_PLZ': 'postcode',
        'VORGANG_DATUM': 'Date',
    }

    data_accounts.rename(columns=cols, inplace=True)
    # data_accounts = data_accounts[data_accounts['Jahr']==2018]
    # data_accounts = data_accounts[(data_accounts['Jahr']==2018) | (data_accounts['Jahr']==2017)]

    # data_accounts['Date'] = to_datetime(data_accounts['Date'], dayfirst=False, yearfirst=False)
    # data_accounts = data_accounts[data_accounts['Date']>='2018-05-18']
    data_accounts['Date'] = to_datetime(data_accounts['Date'])
    data_accounts = data_accounts[data_accounts['Date'] > since]

    data_accounts = data_accounts[data_accounts['Art'] == 'Verkauf']
    data_accounts = data_accounts[data_accounts['Account id'] < 300000]
    data_accounts.drop_duplicates('Account id', inplace=True)

    data_accounts['Account Name'].apply(lambda x: x.replace("'", "`"))

    uploader.upload_customers(dbname=dbname, data=data_accounts)


def upload_kams(filename, what='', since=datetime.date(2000, 1, 1)):
    '''
    '''
    print("Loading KAMs from: {}".format(filename))
    data_accounts = uploader.load_data(filename=filename)
    cols = {
        'ADRESSEN_NAM1': 'Account Name',
        'ADRESSEN_KEY': 'customer id',
        'ADRESSEN_ORT': 'city',
        'VORGANG_VERTRETER': 'kam',
        'VORGANG_L_PLZ': 'postcode',
        'VORGANG_DATUM': 'Date',
    }
    data_accounts.rename(columns=cols, inplace=True)

    data_accounts['Date'] = to_datetime(data_accounts['Date'])
    data_accounts = data_accounts[data_accounts['Date'] > since]

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
        'ADRESSEN_KEY': 'Account id',
        'ADRESSEN_ORT': 'city',
        'VORGANG_VERTRETER': 'kam',
        'VORGANG_L_PLZ': 'postcode',
        'VORGANG_DATUM': 'Date',
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
        'ADRESSEN_KEY': 'Account id',
        'ADRESSEN_ORT': 'city',
        'VORGANG_VERTRETER': 'kam',
        'VORGANG_L_PLZ': 'postcode',
        'VORGANG_DATUM': 'Date',
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


def upload_sales(filename, since=datetime.date(2000, 1, 1)):
    '''
    '''
    print("Loading sales from: {}".format(filename))
    data_sales = uploader.load_data(filename=filename)
    # print(data_sales)

    cols = {
        'VORGANG_LIEFADR': 'customer_id',
        # 'VORGANG_RECHADR':'customer_id',
        'VORGANG_VERTRETER': 'kam',
        'VORGANG_DATUM': 'Date',
        'POSITION_ARTNR': 'product',
        'POSITION_SUMN': 'price',
        'POSITION_SUME': 'cost',
        'VORGANG_MENGE': 'quantity',
        'VORGANG_NR': 'invoice',
        'VORGANG_DATUM': 'Date',
    }

    data_sales.rename(columns=cols, inplace=True)
    # print(data_sales[data_sales['Jahr']==2018])
    # data_sales['Date'] = to_datetime(data_sales['Date'], dayfirst=False, yearfirst=True)
    data_sales['Date'] = to_datetime(data_sales['Date'])

    # print(data_sales['Date'])

    # print(data_sales[data_sales['Jahr']==2018]['Date'])
    # print(data_sales[data_sales['Jahr']=='2018']['Date'])
    # print(data_sales)
    # print(data_sales)
    # data_sales = data_sales[(data_sales['Jahr']==2018)]
    # data_sales = data_sales[data_sales['Date']>=datetime.date(2018,1,1)]
    # print(data_sales)
    # data_sales.to_excel(filename.replace('.xlsx', '_2018.xlsx'))

    # data_sales = data_sales[(data_sales['Jahr']==2018) | (data_sales['Jahr']==2017)]

    data_sales = data_sales[data_sales['Date'] > since]
    data_sales = data_sales[data_sales['Art'] == 'Verkauf']
    data_sales = data_sales[data_sales['customer_id'] < 300000]

    uploader.upload_sales(dbname=dbname, data=data_sales)


def update_products(filename, skiprows=None):
    '''
    '''

    data = uploader.load_data(filename=filename, skiprows=skiprows)
    cols = {
        'Alte Art.Nr.': 'old_name',
        'AET Art.Nr.': 'new_name',
        'VORGANG_DATUM': 'Date',
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


def upload_plans(dbname, filename, skiprows=None, since=datetime.date(2000, 1, 1)):
    '''
    '''

    data = uploader.load_data(filename=filename, skiprows=skiprows)
    cols = {
        'VORGANG_LIEFADR': 'customer_id',
        # 'VORGANG_RECHADR':'customer_id',
        'VORGANG_TITEL': 'name',
        'VORGANG_VERTRETER': 'kam',
        'VORGANG_DATUM': 'Date',
        'POSITION_ARTNR': 'product',
        'ARTIKEL_WG': 'product type',
        'POSITION_SUMB': 'goal',
        'VORGANG_MENGE': 'quantity',
        'VORGANG_NR': 'invoice',
    }

    data.rename(columns=cols, inplace=True)
    data['Date'] = to_datetime(data['Date'], dayfirst=False, yearfirst=False)

    data = data[data['Date'] > since]

    # data = data[(data['Jahr']==2018)]
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
    dbname = 'aet_at'

    since = datetime.date(2018, 8, 30)

    local = True
    local = False

    # filename = '/home/webuser/users/aet_at/data/AET_Warengruppen.xlsx'
    # filename = '/home/webuser/users/aet_at/data/AET_alle_Artikel.xlsx'

    if True:
        filename = '/home/webuser/users/aet_at/data/data_AET_QedvUmsatzAdressenPositionenLieferadresse.xls'
        filename = '/home/webuser/users/aet_at/data/data_AET_QedvUmsatzAdressenPositionenLieferadresse_0506.xlsx'
        filename = '/home/webuser/users/aet_at/data/data_AET_QedvUmsatzAdressenPositionenLieferadresse_0506_EXTRA.xls'
        filename = '/home/webuser/users/aet_at/data/Umsatz_062018.xlsx'
        filename = '/home/webuser/users/aet_at/data/Umsatz_072018.xlsx'
        filename = '/home/webuser/users/aet_at/data/Umsatz_082018.xlsx'
        filename = '/home/webuser/users/aet_at/data/Umsatz_092018.xlsx'
        filename = '/home/webuser/users/aet_at/data/Umsatz_102018.xlsx'
        filename = '/home/webuser/users/aet_at/data/Umsatz_112018.xlsx'
        filename = '/home/webuser/users/aet_at/data/Umsatz_122018.xlsx'

        upload_products(filename, what='line', since=since)
        upload_products(filename, what='type', since=since)
        upload_products(filename, what='products', since=since)

        # filename_accounts = '/home/webuser/users/aet_at/data/data_AET_qwAdressenAsp.xls'
        # upload_customers_2(filename=filename_accounts)
        # filename_accounts = '/home/webuser/users/aet_at/data/data_AET_QedvUmsatzAdressenPositionenLieferadresse.xls'
        # customers(filename=filename_accounts)

        # filename_accounts = '/home/webuser/users/aet_at/data/data_AET_QedvUmsatzAdressenPositionenLieferadresse.xls'
        # filename_accounts = '/home/webuser/users/aet_at/data/data_AET_QedvUmsatzAdressenPositionenLieferadresse_0506.xlsx'
        # filename_accounts = '/home/webuser/users/aet_at/data/data_AET_QedvUmsatzAdressenPositionenLieferadresse_0506_EXTRA.xls'
        filename_accounts = filename

        upload_customers(filename=filename_accounts, since=since)

        # filename_accounts = '/home/webuser/users/aet_at/data/data_AET_QedvUmsatzAdressenPositionenLieferadresse.xls'
        upload_kams(filename=filename_accounts, since=since)

        # filename_sales = '/home/webuser/users/aet_at/data/data_AET_QedvUmsatzAdressenPositionenLieferadresse.xls'
        # filename_sales = '/home/webuser/users/aet_at/data/data_AET_QedvUmsatzAdressenPositionenLieferadresse_0506.xlsx'
        # filename_sales = '/home/webuser/users/aet_at/data/data_AET_QedvUmsatzAdressenPositionenLieferadresse_0506_2018.xlsx'
        # filename_sales = '/home/webuser/users/aet_at/data/data_AET_QedvUmsatzAdressenPositionenLieferadresse_0506_EXTRA.xls'
        filename_sales = filename
        upload_sales(filename=filename_sales, since=since)

        # filename = '/home/webuser/users/aet_at/data/004_AET_ARTIKELSTAMMLISTE_2018-3-19.xlsx'
        # update_products(filename, skiprows=(1))

    # FOR PLANS
    if True:
        # filename = '/home/webuser/users/aet_at/data/data_AET_aedvAngebotAdressenPositionenLieferadresse.xls'
        # filename = '/home/webuser/users/aet_at/data/Angebote_062018.xlsx'
        # filename = '/home/webuser/users/aet_at/data/Angebote_072018.xlsx'
        # filename = '/home/webuser/users/aet_at/data/Angebote_082018.xlsx'
        # filename = '/home/webuser/users/aet_at/data/Angebote_092018.xlsx'
        # filename = '/home/webuser/users/aet_at/data/Angebote_102018.xlsx'
        filename = '/home/webuser/users/aet_at/data/Angebote_112018.xlsx'
        filename = '/home/webuser/users/aet_at/data/Angebote_122018.xlsx'

        upload_plans(dbname, filename, since=since)

    # filename_customers = '/home/webuser/users/aet_at/data/data_not_uploaded_AET_Sales_2018-02_A.xlsx'
    # filename_customers = '/home/webuser/users/aet_at/data/data_not_uploaded_AET_Sales_2018-02_A_3.xlsx'
    # data_cust = load_data(filename=filename_customers)
    # id_list = data_cust['customer_id'].drop_duplicates().values
    # print(id_list)
    # upload_customers(dbname=dbname, data=data_accounts, id_list=id_list)
