"""
Script to get the customer deep details
"""
# pylint: disable=import-error
# pylint: disable=broad-except
# pylint: disable=line-too-long
import json
import logging
import traceback
import pandas as pd

logger = logging.getLogger(__name__)


class CustomersDetails:
    """
    Class read the deep details of customers
    """
    def __init__(self, customers_df, sales_df=None,
                 customer_id=None, page_number=None):
        super()
        self.customer_df = customers_df
        self.sale_df = sales_df
        self.customer_id = customer_id
        self.page_number = page_number

    def get_customers_details(self):
        """
        function: get customers details
        """

        customers = self.get_customers_metrics()

        for key in customers:
            scales = list()
            for metric in ('sales', 'margin'):
                try:
                    s_sales_margin_val = round(
                        customers[key]['s' + metric], 2
                    )
                    sales_margin_val = round(customers[key][metric])
                except KeyError as exception:
                    logger.info("%s", exception)
                    s_sales_margin_val = 0
                    sales_margin_val = 0
                scales.append(
                    {
                        'y': s_sales_margin_val,
                        'value': sales_margin_val,
                        'label': sales_margin_val
                    }
                )

            risk_scale = self.get_risk(customers, key)
            scales.append(risk_scale)

            ppb_scale = self.get_ppb(customers, key)
            scales.append(ppb_scale)

            ccbm_scale = self.get_ccbm(customers, key)
            scales.append(ccbm_scale)

            customers[key]['scales'] = scales
        return customers

    def get_customers_metrics(self):
        """
        function: get customers metrics
        """
        customers = dict()

        try:
            for data_keys in ('sales', 'margin', 'risk', 'ppb', 'ccbm'):

                self.customer_df[data_keys] = self.customer_df[
                    data_keys].apply(pd.to_numeric)

                if self.customer_id:
                    self.sale_df[data_keys] = self.sale_df[data_keys].apply(pd.to_numeric)

                    self.customer_df[
                        's' + data_keys] = self.customer_df[data_keys] / self.sale_df[data_keys].max()
                elif self.page_number:
                    self.sale_df[data_keys] = self.sale_df[data_keys].apply(pd.to_numeric)

                    self.customer_df['s' + data_keys] = \
                        self.customer_df[data_keys] / self.sale_df[data_keys].max()
                else:
                    self.customer_df['s' + data_keys] = \
                        self.customer_df[data_keys] / self.customer_df[data_keys].max()

            grouped = self.customer_df.groupby('id')
            for name, group in grouped:
                customers[str(name)] = json.loads(
                    group.to_json(orient='records'))[0]
        except Exception as exception:
            logger.error(
                "message %s, error %s",
                exception,
                traceback.format_exc(),
                extra={'type': 'Login'}
            )

        return customers

    @staticmethod
    def get_risk(customers, key):
        """
        Static method to get the risk value of a customer
        """
        count_risk_high = 0
        count_risk_some = 0
        count_risk_low = 0
        count_risk_unknown = 0

        metric = 'risk'
        try:
            s_risk_val = round(customers[key]['s' + metric], 2)
            risk_val = customers[key][metric]
        except KeyError as exception:
            logger.info("%s", exception)
            s_risk_val = 0
            risk_val = 0

        if 1.3 < risk_val <= 2:
            label = 'low'
            count_risk_high += 1
        elif 0.7 < risk_val <= 1.3:
            label = 'some'
            count_risk_some += 1
        elif 0.0 < risk_val <= 0.7:
            label = 'high'
            count_risk_low += 1
        else:
            label = 'unknown'
            count_risk_unknown += 1

        return {
            'y': s_risk_val,
            'value': risk_val,
            'label': label
        }

    @staticmethod
    def get_ppb(customers, key):
        """
        Static method to get the ppb value of a customer
        """
        metric = 'ppb'

        count_ppb_good = 0
        count_ppb_normal = 0
        count_ppb_bad = 0
        count_ppb_unknown = 0

        try:
            s_ppb_val = round(customers[key]['s' + metric], 2)
        except KeyError as exception:
            logger.info("%s", exception)
            s_ppb_val = 0

        ppb_val = customers[key][metric]

        if ppb_val == 2:
            label = 'good'
            count_ppb_good += 1
        elif ppb_val == 1:
            label = 'normal'
            count_ppb_normal += 1
        elif ppb_val == 0:
            label = 'bad'
            count_ppb_bad += 1
        else:
            label = 'unknown'
            count_ppb_unknown += 1

        return {
            'y': s_ppb_val,
            'value': ppb_val,
            'label': label
        }

    @staticmethod
    def get_ccbm(customers, key):
        """
        Static method to get the ccbm value of customer
        """
        metric = 'ccbm'
        try:
            s_ccbm = round(customers[key]['s' + metric], 2)
        except KeyError as exception:
            logger.info("%s", exception)
            s_ccbm = 0

        return {
            'y': s_ccbm,
            'value': s_ccbm,
            'label': s_ccbm
        }
