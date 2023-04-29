import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from src.exception import CustomException
from src.logger import logging
import sys

#  convert transaction date to datetime
# groupby customer id and aggregate by {'TransactionDate':'max', 'TransactionID':'count', 'TransactionAmount (INR)':'sum'}
# create recency feature by subtracting max transaction date from today and converting to days

class DataTransformation:
    def __init__(self, df):
        self.df = df
        self.rfm = pd.DataFrame() 
    
    def convert_to_datetime(self):
        try:
            self.df['TransactionDate'] = pd.to_datetime(self.df['TransactionDate'])
        except Exception as e:
            logging.error('Error converting to datetime datatype')
            raise CustomException(e, sys)

    def groupby_customer_id(self):
        try:
            self.rfm = self.df.groupby('CustomerID').agg({'TransactionDate':'max', 'TransactionID':'count', 'TransactionAmount (INR)':'sum'}).reset_index()
        except Exception as e:
            logging.error('Error while grouping by customer id')
            raise CustomException(e, sys)

    def create_recency_feature(self):
        try:
            self.rfm['Recency'] = self.df['TransactionDate'].max() - self.rfm['TransactionDate']
            self.rfm['Recency'] = self.rfm['Recency'].dt.days
        except Exception as e:
            logging.error('Error while creating recency feature')
            raise CustomException(e, sys)

    def drop_customer_id(self):
        try:
            self.rfm = self.rfm.drop('CustomerID', axis=1)
        except Exception as e:
            logging.error('Error while dropping customer id')
            raise CustomException(e, sys)

    def rename_columns(self):
        try:
            self.rfm.columns = ['Frequency', 'Monetary', 'Recency']
        except Exception as e:
            logging.error('Error while renaming columns')
            raise CustomException(e, sys)


    def create_rfm_df(self):
        self.convert_to_datetime()
        self.groupby_customer_id()
        self.create_recency_feature()
        self.drop_customer_id()
        self.rename_columns()
        return self.rfm
        