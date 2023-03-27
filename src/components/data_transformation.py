from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin

import logging
import numpy as np
import pandas as pd
from src.exception import CustomException
import sys
import warnings
warnings.filterwarnings('ignore')



# Load the data into a pandas dataframe
df = pd.read_csv('../../artifacts/train.csv')


class DropNullTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns=None):
        self.columns = columns

    def fit(self, df, y=None):
        return self

    def transform(self, df):
        if self.columns:
            df = df.dropna(subset=self.columns)
        else:
            df = df.dropna()
        return df


class CalculateAge(BaseEstimator, TransformerMixin):
    def __init__(self, columns=None):
        self.columns = columns

    def fit(self, df, y=None):
        return self

    def transform(self, df):
        df['CustomerDOB'] = pd.to_datetime(df['CustomerDOB'])
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        df['CustomerAge'] = df['TransactionDate'].dt.year - df['CustomerDOB'].dt.year
        return df


class LocationRegex(BaseEstimator, TransformerMixin):
    def __init__(self, columns=None):
        self.columns = columns

    def fit(self, df, y=None):
        return self

    def transform(self, df):
        df.drop(columns=['TransactionID', 'TransactionTime'], inplace=True)
        df.replace(r'(.*HYDERABAD.*)', 'HYDERABAD', regex=True, inplace=True)
        df.replace(r'(.*PUNE.*)', 'PUNE', regex=True, inplace=True)
        df.replace(r'(.*AHMEDABAD.*)', 'AHMEDABAD', regex=True, inplace=True)
        df.replace(r'(.*MUMBAI.*)', 'MUMBAI', regex=True, inplace=True)
        df.replace(r'(.*BANGALORE.*)', 'BANGALORE', regex=True, inplace=True)
        df.replace(r'(.*DELHI.*)', 'DELHI', regex=True, inplace=True)
        df.replace(r'(.*RAJKOT.*)', 'RAJKOT', regex=True, inplace=True)
        df.replace(r'(.*THANE.*)', 'THANE', regex=True, inplace=True)
        df.replace(r'(.*CHENNAI.*)', 'CHENNAI', regex=True, inplace=True)
        df.replace(r'(.*COIMBATORE.*)', 'COIMBATORE', regex=True, inplace=True)
        df.replace(r'(.*JAIPUR.*)', 'JAIPUR', regex=True, inplace=True)
        df.replace(r'(.*KOLKATA.*)', 'KOLKATA', regex=True, inplace=True)
        return df


class RemoveOutliers(BaseEstimator, TransformerMixin):
    def __init__(self, columns=None):
        self.columns = columns

    def fit(self, df, y=None):
        return self

    def transform(self, df):
        num_cols = df.select_dtypes(include=[np.float64, np.int64])
        isof = IsolationForest(n_estimators=100, contamination=0.1)
        isof.fit(num_cols)
        outliers = isof.predict(num_cols)
        df['is_inliner'] = outliers
        df = df[df['is_inliner'] == 1]
        df.head()
        df.drop('is_inliner', axis=1, inplace=True)
        return df


class OrdinalEncoding(BaseEstimator, TransformerMixin):
    def __init__(self, columns=None):
        self.columns = columns

    def fit(self, df, y=None):
        return self

    def transform(self, df):
        encoder = OrdinalEncoder()
        df.drop(columns=['TransactionDate', 'CustomerDOB'], inplace=True)
        columns = df.select_dtypes(include=['object']).columns
        df[columns] = encoder.fit_transform(df[columns])
        return df


class DataTransformation:

    def transform_data(self):
        try:
            pipeline = Pipeline(steps=[
                ('drop_missing', DropNullTransformer()),
                ('calculate_age', CalculateAge()),
                ('location_regex', LocationRegex()),
                ('remove_outliers', RemoveOutliers()),
                ('ordinal_encoding', OrdinalEncoding()),
                ('standard_scaling', StandardScaler())
            ])
            return pipeline
        except Exception as e:
            raise CustomException(e, sys)
    def initiate_data_transformation(self):
        try:
            train_df = pd.read_csv('artifacts/train.csv')
            test_df = pd.read_csv('artifacts/test.csv')
            logging.info('Data has been read')
            train_df = train_df.sample(n=100000)
            test_df = test_df.sample(n=100000)
            pipeline = self.transform_data()
            df_transformed = pipeline.fit_transform(df)
            df_transformed = pd.DataFrame(df_transformed)
            df_transformed.columns = ['CustomerID', 'CustomerGender', 'CustomerLocation', 'CustAccountBalance', 'TransactionAmount',
                                      'CustomerAge']
            logging.info('Data has been transformed')
            return df_transformed
        except Exception as e:
            raise CustomException(e, sys)




