
class PPB():

    def __init__(self, data=None, products=None):
        super().__init__()
        self.df = data
        self.prods = products

    def calculate(self):
        try:
            for p in df['product_id'].unique():
                df.loc[df['product_id'] == p,
                       'mean_prod_price'] = prods[prods['product_id'] == p]['mean_price'].values

            df.loc[df['mean_prod_price'] > df['mean_price'] * 1.15, 'ppb'] = 1
            df.loc[df['mean_prod_price'] < df['mean_price'] * 0.85, 'ppb'] = -1
            df.loc[(df['mean_price'] * 0.85 < df['mean_prod_price']) & (
                df['mean_prod_price'] < df['mean_price'] * 1.15), 'ppb'] = 0

            ppbs = df.groupby(['customer_id'])[
                ['prod_qty', 'price', 'margin', 'ppb']].sum().reset_index()
            ppb_count = df.groupby(['customer_id'])[
                'ppb'].count().reset_index()
            ppbs['ppb_value'] = ppbs['ppb'] / ppb_count['ppb']
            ppbs.loc[ppbs['ppb_value'] > 0.1, 'ppb'] = 2
            ppbs.loc[ppbs['ppb_value'] < -0.1, 'ppb'] = 1
            ppbs.loc[(ppbs['ppb_value'] <= 0.1) & (
                ppbs['ppb_value'] >= -0.1), 'ppb'] = 0
            ppbs.loc[ppbs['ppb_value'].isnull(), 'ppb'] = 4

            ppbs['ppb'] = ppbs['ppb'].astype(int)

            ppbs['customer_id'] = ppbs['customer_id'].astype(int)

            try:
                ppbs['size'] = np.log(ppbs['price'])
            except:
                ppbs['size'] = 0

            sys.stdout.write("Calculating ppb...Done\n")
            return ppbs
        except:
            pass

        ppbs = dict()
        ppbs = dict.fromkeys([
            'ppb',
            'max_price',
            'min_price',
            'mean_price',
            'suggested_price',
        ])
        return ppbs
