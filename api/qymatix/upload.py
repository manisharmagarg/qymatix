import os
import sys

# import datetime
import config
import customers
import kam
import pandas as pd
import products
import sales


def delete_databases(dbname, username, local=False):
    '''
    '''
    # if config.checkDatabaseExists(dbname='data_' + dbname):

    print("Deleting old database...")
    try:
        config.dropDatabase(dbname='data_' + dbname, local=local)
    except Exception as e:
        print(e)

    try:
        config.dropDatabase(dbname='results_' + dbname, local=local)
    except Exception as e:
        print(e)

    try:
        config.dropDatabase(dbname='data_' + dbname, local=local)
    except Exception as e:
        print(e)


def init_databases(dbname, username, local=False):
    # if not config.checkDatabaseExists(dbname='data_' + dbname):
    try:
        config.createDatabase(dbname='data_' + dbname, local=local)
    except Exception as e:
        print(e)
        # raise

    try:
        config.createDatabase(dbname='results_' + dbname, local=local)
    except Exception as e:
        print(e)

    try:
        config.createDatabase(dbname="data_" + dbname, local=local)
    except Exception as e:
        print(e)

    try:
        config.createDataTables(dbname='data_' + dbname, local=local)
    except Exception as e:
        print(e)

    try:
        config.createTasksTables(dbname="data_" + dbname, local=local)
    except Exception as e:
        print(e)

    try:
        config.initTasksTables(dbname="data_" + dbname, name=username, local=local)
    except Exception as e:
        print(e)

    try:
        config.createUsersCustomersTable(dbname="data_" + dbname, local=local)
    except Exception as e:
        print(e)


def upload_data(dbname, username, filename):
    '''
    '''
    name, ext = os.path.splitext(filename)
    name = os.path.split(name)[-1] + "_" + ext[1:]
    name = name.replace("-", "_")
    name = name.replace(".", "_")

    # if os.path.splitext(filename)[1] == '.csv':
    # csv2mysql(data=filename, dbname=dbname)
    if os.path.splitext(filename)[1] in ['.xlsx', '.xls']:
        try:
            print("Uploading data...")
            xls2mysql(data=filename, dbname=dbname)
        except Exception as e:
            print("Not posible to upload data. Check your file.")
            print(e)
            # return None
            raise

        # dbname = "data_" + username + "_{}".format(name)
        dbname = "data_" + dbname
        config.createUsersCustomersTable(dbname)

        try:
            kam.insertKamFromFile(dbname, filename=filename)
        except:
            print("Not posible to insert KAM.")
            # return None
            raise


def xls2mysql(data, dbname='data_userID_username', from_line=None, to_line=None, local=False):
    '''
    '''
    filename = data

    # data = pd.read_excel(filename, 'Sheet1')
    data = pd.read_excel(filename, encoding='latin1')

    for c in data.columns:
        if c in ('Date', 'date', 'Invoice Date'):
            data.rename(columns={c: 'Date'}, inplace=True)

    data['Date'] = pd.to_datetime(data['Date'], dayfirst=False, yearfirst=False)
    data.drop_duplicates(inplace=True)

    if from_line == None:
        from_line = 0
    if to_line == None:
        to_line = len(data.index)

    for i in data.index.tolist()[from_line:to_line]:
        # if lines != None:
        # if i > lines:
        # return
        # sys.stdout.write("\r")
        # sys.stdout.write("{} form {}".format(i, to_line))
        sys.stdout.write("{} form {}\r".format(i, max(data.index.tolist())))
        sys.stdout.flush()

        cust_address = ""
        cust_postcode = ""
        cust_city = ""
        cust_country = ""
        sales_date = ""
        sales_kam = ""
        cust_revenue = -1
        cust_employees = -1
        cust_industry = ""
        cust_classification = ""
        cust_website = ""
        cust_comment = ""
        cust_favorite = 0

        sales_data = {}

        for name in data.columns:
            if name in ('Kunde', 'Clients', 'Customer', 'Client', 'Customer Name', 'Account'):
                cust_name = data.ix[i][name]
                # cust_name = cust_name.replace(" ", "_")
                # print(cust_name.encode('utf-8'))
                # print(cust_name)
            if name in (u'Address', u'Adresse'):
                cust_address = data.ix[i][name]
            if name in (u'PLZ', u'Post', u'Postcode', u'Zipcod', u'Zip', u'ZipCode'):
                cust_postcode = data.ix[i][name]
            if name in ('city', 'City', u'stadt', u'Stadt'):
                cust_city = data.ix[i][name]
            if name in (u'Country', u'Land'):
                cust_country = data.ix[i][name]
            if name in (u'revenue', u'Revenue'):
                cust_revenue = data.ix[i][name]
            if name in (u'employees', u'Employees'):
                cust_employees = data.ix[i][name]
            if name in (u'industry', u'Industry'):
                cust_industry = data.ix[i][name]
            if name in (u'classification', u'Classification'):
                cust_classification = data.ix[i][name]
            if name in (u'website', u'Website', u'Webpage', u'webpage', u'Site', u'site'):
                cust_website = data.ix[i][name]
            if name in (u'comment', u'comment'):
                cust_comment = data.ix[i][name]
            if name in (u'favorite', u'Favorite'):
                cust_favorite = data.ix[i][name]

            if name in (u'Product', u'Material', u'Article', u'Artikel', 'Item'):
                prod_name = str(data.ix[i][name])
                # prod_name = prod_name.replace(" ", "_")
            if name in (u'Product description', u'Item Description', u'Article Description'):
                prod_description = str(data.ix[i][name])
            if name in (u'Product Group', u'Item Group', u'Article Group', 'Product Type', 'Type'):
                prod_type = str(data.ix[i][name])
            if name in ('Price', 'Pay', 'Preis', 'price'):
                sales_data['prod_price'] = float(str(data.ix[i][name]).replace(',', '.'))
            if name in ('Margin', 'margin', 'Marge'):
                sales_data['prod_margin'] = float(str(data.ix[i][name]).replace(",", "."))
            if name in ('Cost', 'Costs', 'Fabrication Cost'):
                sales_data['prod_cost'] = float(str(data.ix[i][name]).replace(',', '.'))
            if name in ('Unit Cost'):
                sales_data['prod_unit_cost'] = float(str(data.ix[i][name]).replace(',', '.'))
            if name in ('Unit Price'):
                sales_data['prod_unit_price'] = float(str(data.ix[i][name]).replace(',', '.'))
            if name in ('Unit Margin'):
                sales_data['prod_unit_margin'] = float(str(data.ix[i][name]).replace(',', '.'))
            if name in ('Quantity', 'Qty'):
                sales_data['prod_quantity'] = int(str(data.ix[i][name]).replace(',', '.'))
            if name in ('Year', 'YY', 'Jahr'):
                sales_year = data.ix[i][name]
            if name in ('Month', 'MM', 'Monat'):
                sales_month = data.ix[i][name]
            if name in ('Date', 'date', 'Invoice Date'):
                sales_date = data.ix[i][name]
            if name in ('Invoice', 'Invoice No.'):
                sales_invoice = data.ix[i][name]
            if name in ('KAM', 'kam', 'Account Manager', 'AccountManager', 'Account manager', 'account manager'):
                sales_kam = data.ix[i][name]

        if 'prod_quantity' not in sales_data.keys():
            sales_data['prod_quantity'] = 1

        if 'prod_unit_price' in sales_data.keys() and 'prod_price' not in sales_data.keys():
            sales_data['prod_price'] = sales_data['prod_unit_price'] * sales_data['prod_quantity']

        if 'prod_unit_price' not in sales_data.keys() and 'prod_price' in sales_data.keys():
            sales_data['prod_unit_price'] = sales_data['prod_price'] / sales_data['prod_quantity']

        if 'prod_unit_cost' in sales_data.keys() and 'prod_cost' not in sales_data.keys():
            sales_data['prod_cost'] = sales_data['prod_unit_cost'] * sales_data['prod_quantity']

        if 'prod_unit_cost' not in sales_data.keys() and 'prod_cost' in sales_data.keys():
            sales_data['prod_unit_cost'] = sales_data['prod_cost'] / sales_data['prod_quantity']

        if 'prod_unit_margin' not in sales_data.keys() and 'prod_unit_cost' in sales_data.keys():
            sales_data['prod_unit_margin'] = sales_data['prod_unit_price'] - sales_data['prod_unit_cost']
        if 'prod_unit_margin' in sales_data.keys() and 'prod_cost' not in sales_data.keys():
            sales_data['prod_unit_cost'] = sales_data['prod_unit_price'] - sales_data['prod_unit_margin']

        if 'prod_margin' not in sales_data.keys() and 'prod_cost' in sales_data.keys():
            sales_data['prod_margin'] = sales_data['prod_price'] - sales_data['prod_cost']
        if 'prod_margin' in sales_data.keys() and 'prod_cost' not in sales_data.keys():
            sales_data['prod_cost'] = sales_data['prod_price'] - sales_data['prod_margin']

        try:
            sales_invoice
        except:
            sales_invoice = 'NULL'

        try:
            prod_description
        except:
            prod_description = ""

        try:
            prod_type
        except:
            prod_type = ""

        try:
            prod_type_description
        except:
            prod_type_description = ""

        try:
            try:
                _data = {
                    'name': cust_name, \
                    'address': cust_address, \
                    'postcode': cust_postcode, \
                    'city': cust_city, \
                    'country': cust_country, \
                    'revenue': cust_revenue, \
                    'employees': cust_employees, \
                    'industry': cust_industry, \
                    'classification': cust_classification, \
                    'website': cust_website, \
                    'comment': cust_comment, \
                    'favorite': cust_favorite
                }

                customer_id = customers.insertCustomer(_data, dbname, local=local)

            except Exception as e:
                # print(e)
                # raise
                pass

            try:
                if prod_type == "":
                    prod_type = "Product Type not specified"

                try:
                    _data = {
                        'name': prod_type, \
                        'description': prod_type_description \
                        }
                    product_type_id = products.insertProductType(data=_data, dbname=dbname, local=local)
                except:
                    product_type_id = 1
                    raise

                _data = {
                    'name': prod_name, \
                    'product_type_id': product_type_id, \
                    'description': prod_description \
                    }
                product_id = products.insertProduct(_data, dbname, local=local)

            except Exception as e:
                print(e)
                raise
                # pass

            try:

                _data = { \
                    'customer_id': customer_id, \
                    'product_id': product_id, \
                    'quantity': sales_data['prod_quantity'], \
                    'price': sales_data['prod_price'], \
                    'cost': sales_data['prod_cost'], \
                    'margin': sales_data['prod_margin'], \
                    'year': sales_date.year, \
                    'month': sales_date.month, \
                    'date': sales_date.isoformat().replace("T", " "), \
                    'invoice': sales_invoice, \
                    'kam': sales_kam, \
                    }

                sales.insertSalesRecord(_data, dbname, local=local)

            except Exception as e:
                print(e)
                raise
                # pass
        except:
            raise


if __name__ == "__main__":
    # dbname = 'ftest'
    # username = 'ftest'
    dbname = 'martinmasip_data_test_2015_2016_copy_super_reduced_xlsx'
    username = 'martinmasip'
    dbname = 'martinmasip'
    dbname = 'martin_masip'
    dbname = 'qymatix_best'
    dbname = 'coldjet_qy'
    local = True
    local = False

    # delete_databases(dbname, username, local=local)
    # init_databases(dbname, username, local=local)

    # config.clear_table('data_' + dbname + '.sales')
    ##xls2mysql(data='/home/webuser/users/martinmasip/data/data_test_few_records.xlsx', dbname=dbname)
    # xls2mysql(data='/home/webuser/users/martinmasip/data/Sales_analytics_520_Oli_modified_2_short.xlsx', dbname=dbname, local=local)
    # xls2mysql(data='/home/webuser/users/martin_masip/data/20170622_Orbus_January_2016-June_2017.xlsx', dbname=dbname, local=local)
    # xls2mysql(data='/home/webuser/users/martin_masip/data/20170622_Orbus_January_2016-June_2017_reduced.xlsx', dbname=dbname, local=local)
    xls2mysql(data='/home/webuser/users/coldjet_qy/data/sales_coldjet.xlsx', dbname=dbname, local=local)
