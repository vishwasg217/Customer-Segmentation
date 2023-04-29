import numpy as np
import pandas as pd

from src.exception import CustomException
from src.logger import logging
import sys
# drop missing values
# convert transaction date and customer birth date to datetime
# create new column for age and remove ages below 0 and above 100
# regex on location to extract city
# month year column

class DataPreprocessor:

    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def drop_missing_values(self):
        try: 
            self.df = self.df.dropna()
        except Exception as e:
            logging.error('Error while dropping null values')
         

    def drop_feature(self, feature: list):
        try: 
            self.df = self.df.drop(feature, axis=1)
        except Exception as e:
            logging.error('Error while dropping a feature')
             
    def convert_to_datetime(self):
        try: 
            self.df['TransactionDate'] = pd.to_datetime(self.df['TransactionDate'])
            self.df['CustomerDOB'] = pd.to_datetime(self.df['CustomerDOB'])
        except Exception as e:
            logging.error('Error while converting to datetime datatype')
         
    def create_age_column(self):
        try:
            self.df['age'] = self.df['TransactionDate'].dt.year - self.df['CustomerDOB'].dt.year
            self.df = self.df[(self.df['age'] >= 0) & (self.df['age'] <= 100)]
        except Exception as e:
            logging.error('Error while creating age column')
         
    def regex_city(self):
        try:
            self.df.replace(r'(.*HYDERABAD.*)','HYDERABAD',regex=True, inplace = True)
            self.df.replace(r'(.*PUNE.*)','PUNE',regex=True, inplace = True)
            self.df.replace(r'(.*AHMEDABAD.*)','AHMEDABAD',regex=True, inplace = True)
            self.df.replace(r'(.*MUMBAI.*)','MUMBAI',regex=True, inplace = True)
            self.df.replace(r'(.*BANGALORE.*)','BANGALORE',regex=True, inplace = True)
            self.df.replace(r'(.*DELHI.*)','DELHI',regex=True, inplace = True)
            self.df.replace(r'(.*RAJKOT.*)','RAJKOT',regex=True, inplace = True)
            self.df.replace(r'(.*THANE.*)','THANE',regex=True, inplace = True)
            self.df.replace(r'(.*CHENNAI.*)','CHENNAI',regex=True, inplace = True)
            self.df.replace(r'(.*COIMBATORE.*)','COIMBATORE',regex=True, inplace = True)
            self.df.replace(r'(.*JAIPUR.*)','JAIPUR',regex=True, inplace = True)
            self.df.replace(r'(.*KOLKATA.*)','KOLKATA',regex=True, inplace = True)
        except Exception as e:
            logging.error('Error cwhile performing regex')
         
    
    def create_month_year_column(self):
        try:
            self.df['month_year'] = self.df['TransactionDate'].dt.strftime('%b %Y')
            self.df['month_year'] = pd.to_datetime(self.df['month_year'])
        except Exception as e:
            logging.error('Error while creating month year column')

    def preprocess(self):
        self.drop_missing_values()
        self.drop_feature(['TransactionTime'])
        self.convert_to_datetime()
        self.create_age_column()
        self.regex_city()
        self.create_month_year_column()
        return self.df


# TransactionID,CustomerID,CustomerDOB,CustGender,CustLocation,CustAccountBalance,TransactionDate,TransactionTime,TransactionAmount (INR)

    

