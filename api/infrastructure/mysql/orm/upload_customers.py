import sqlalchemy
import autogen_entities
import pandas as pd
import os
from numpy import nan


database = 'data_qy___test_com'
database = 'data_clarus___films_com'

url = "mysql+mysqlconnector://root:dev@0.0.0.0:3306/{}".format(database)
engine = sqlalchemy.create_engine(
                url,
                connect_args={'use_pure': True}
            )

Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

# customers = session.query(autogen_entities.Customer).all()
# for c in customers:
    # print(c.name)

customer_name = 'BRAHMS DIAGNOSTIKA'
customer_industry = 'Medizin-Pharma'

def load_data(filename, skiprows=None, nrows=None):
    '''
    '''
    if os.path.splitext(filename)[1] in ['.xlsx', '.xls']:
        data = pd.read_excel(filename, skiprows=skiprows, nrows=nrows)
    if os.path.splitext(filename)[1] in ['.csv']:
        data = pd.read_csv(filename, delimiter=';')

    return data

def transform_data(data):

        cols = {
            'Auftragsnr.': 'invoice',
            'Re-/Gu-Datum': 'Date',
            'Artikelnr.': 'product',
            'Artikelgruppennr.': 'product type',
            'Umsatz VK': 'price',
            'Marge': 'margin',
            'Warengruppennr.': 'product line',
            'Menge': 'quantity',
            'MC Kunde': 'account name',
            'Branchennr.': 'product class',
            'Branchenbez.': 'industry',
        }

        data.rename(columns=cols, inplace=True)

        data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)

        return data

raw_data = load_data('/Users/martin/Documents/cui/accounts/Clarus/ExcelExport_tblFaktStd_201909020919.xlsx')

data = transform_data(raw_data)

data = data[['account name', 'industry']]

data.drop_duplicates('account name', inplace=True)

for index, row in data.iterrows():
    customer_name = row['account name']
    customer_industry =  row['industry']

    if customer_name is not nan and customer_industry is not nan:
        customer = session.query(autogen_entities.Customer)\
                                .filter_by(name=customer_name)\
                                .first()

        if customer != None:
            customer.industry = customer_industry

            session.commit()

            print(">>>>")
            print(customer.industry)


