import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import  *
from utils.common_functions import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config['bucket_name']
        self.bucket_file_name = self.config['bucket_file_name']
        self.train_ratio =self.config['train_ratio']


        os.makedirs(raw_dir, exist_ok= True)

        logger.info(f'Data Ingestion started with bucket {self.bucket_name} and file {self.bucket_file_name}') 

    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.bucket_file_name)

            blob.download_to_filename(raw_file_path) 

            logger.info("Downloaded as csv") 
        except Exception as e:
            logger.error('error while downloading data')
            raise CustomException('File not downloaded',e)


    def split_data(self):
        try:
            logger.info('Spliting started')
            
            df= pd.read_csv(raw_file_path)

            train_data, test_data = train_test_split(df, test_size= 1- self.train_ratio, random_state= 1)

            train_data.to_csv(train_file_path)
            test_data.to_csv(test_file_path)

            logger.info(f"Train data saved to {train_file_path} and test data saved to {test_file_path}")
        
        except Exception as e:
            logger.error('error while spltiing data')
            raise CustomException('File not split into train and test data',e)
        
    def run(self):
        try:
            logger.info("starting data ingestion")
            self.download_csv_from_gcp()
            self.split_data()

            logger.info("Data ingestion complete")
        except Exception as e:
            logger.error('error while data ingestion')
            raise CustomException('File not ingested',e)
        finally:
            logger.info("completed ingestion")

if __name__ == '__main__':
    dataingestion = DataIngestion(read_yaml(config_path))
    dataingestion.run()