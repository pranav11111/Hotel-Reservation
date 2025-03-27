from src.data_preprocessing import DataProcessor
from src.data_ingestion import DataIngestion
from src.model_trainer import ModelTrainer
from utils.common_functions import read_yaml
from config.paths_config import *


if __name__ == '__main__':
    dataingestion = DataIngestion(read_yaml(config_path))
    dataingestion.run()

    processor = DataProcessor(train_file_path, test_file_path,processed_dir,config_path)
    processor.run_processor()

    trainer = ModelTrainer(processed_train_data_path, processed_test_data_path, model_output_path)
    trainer.run_model()
