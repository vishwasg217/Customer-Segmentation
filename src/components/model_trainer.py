import logging
import numpy as np
import pandas as pd
from src.exception import CustomException
import sys
import warnings

warnings.filterwarnings('ignore')

from data_transformation import DataTransformation


class ModelTrainer:
    def train_model(self):
        logging.info('Loading transformed data')
        DT = DataTransformation()
        df = DT.transform_data()




