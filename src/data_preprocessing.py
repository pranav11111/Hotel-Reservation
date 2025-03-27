import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE


logger = get_logger(__name__)


class DataProcessor:

    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir

        self.config = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    def preprocess_data(self, df):
        try:
            logger.info("Starting data preprocssing")

            logger.info("Dropping unnamed and unnecessary columns")
            
            df.drop(['Unnamed: 0', 'Booking_ID'], axis= 1, inplace= True)
            
            logger.info("Dropped unnamed and unnecessary columns")
            
            logger.info("Removing duplicates")
            
            df.drop_duplicates(inplace= True)
            
            logger.info("Removed duplicates")

            cat_cols = self.config['data_processing']['categorical_columns']
            num_cols = self.config['data_processing']['numerical_columns']


            logger.info(" Starting label encoding")
            lb = LabelEncoder()

            mappings= {}

            for column in cat_cols:
                df[column] = lb.fit_transform(df[column])

                mappings[column] = {label:code for label, code in zip(lb.classes_, lb.transform(lb.classes_))}    

            logger.info("Label mappings are:")    

            for col,mappings in mappings.items():
                logger.info(f"{col}, {mappings}")  

            logger.info("Handling skewness")

            skewness_threshold = self.config['data_processing']['skewness_threshold']
            skewness = df[num_cols].apply( lambda x: x.skew())

            for column in skewness[skewness > skewness_threshold].index:
                df[column] = np.log1p(df[column])

            return df
        
        except Exception as e:
            logger.error('Error during preprocess step',e)
            raise CustomException('Error while prerpocessing', e)
        
    def balance_data(self, df):
        try:
            logger.info('Handling imblanced data')
            x = df.drop('booking_status', axis =1)
            y = df['booking_status']
            
            
            smote = SMOTE(random_state= 42)
            x_resampled, y_resampled = smote.fit_resample(x,y)

            balanced_df = pd.DataFrame(x_resampled, columns= x.columns)
            balanced_df['booking_status'] = y_resampled

            logger.info('Data balanced succesfully')

            return balanced_df
        
        except Exception as e:
            logger.error('Error during balancing data',e)
            raise CustomException('Error while balancing data', e)
        
    def select_features(self, df):
        try:
            logger.info("Starting feature selection")

            x = df.drop('booking_status', axis =1)
            y = df['booking_status']

            model = RandomForestClassifier(random_state= 42)
            model.fit(x,y)

            feature_imporatnce = model.feature_importances_

            feature_imporatnce_df = pd.DataFrame({"features": x.columns, "importance": feature_imporatnce })

            top_important_feature = feature_imporatnce_df.sort_values(by= 'importance', ascending= False)

            no_features = self.config['data_processing']['no_of_features']

            top_10_features = top_important_feature['features'].head(no_features).values

            logger.info(f'Select total of {no_features} which are {top_10_features}')

            top_10_df = df[top_10_features.tolist() + ['booking_status']]

            logger.info("Feature selection completed succesfully!")

            return top_10_df
        except Exception as e:
            logger.error('Error during feature selection',e)
            raise CustomException('Error while selection', e)


    def save_data(self, df, path):
        try:
            logger.info("saving data in processed folder")
            df.to_csv(path, index = False)

            logger.info(f'Data saved succesfully to {path}')

        except Exception as e:
            logger.error('Error during saving data',e)
            raise CustomException('Error while saving', e)
        
    def run_processor(self):
        try:
            logger.info("loading data")

            train_df = load_data(self.train_path)
            test_df = load_data(self.train_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.balance_data(train_df)

            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]


            self.save_data(train_df, processed_train_data_path)
            self.save_data(test_df, processed_test_data_path)

            logger.info("data proccessing completed")
        except Exception as e:
            logger.error('Error during full preprocessing',e)
            raise CustomException('Error full preprocessing', e)
        
if __name__ == "__main__":
    processor = DataProcessor(train_file_path, test_file_path,processed_dir,config_path)
    processor.run_processor()