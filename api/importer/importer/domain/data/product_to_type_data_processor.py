import pandas as pd
import os


class ProductToTypeDataProcessor():

    def __init__(self, filename, mappings):
        super().__init__()

        self.mappings = mappings 

        self.processed_data = None

        self.load_data(str(filename))
        self.transform_data()
        self.clean_data()

    def load_data(self, filename, skiprows=None, nrows=None):
        if os.path.splitext(filename)[1] in ['.xlsx', '.xls']:
            data = pd.read_excel(filename, skiprows=skiprows, nrows=nrows)
        if os.path.splitext(filename)[1] in ['.csv']:
            data = pd.read_csv(filename, delimiter=';')
        self.processed_data = data

    def transform_data(self):
        cols = self.mappings
        self.processed_data.rename(columns=cols, inplace=True)
        self.processed_data['Date'] = pd.to_datetime(self.processed_data['Date'], dayfirst=True)
    
    def clean_data(self):
        self.processed_data = self.processed_data[['product', 'product type']]
        self.processed_data.drop_duplicates('product', inplace=True)
    
    @property
    def data(self):
        return self.processed_data
        
