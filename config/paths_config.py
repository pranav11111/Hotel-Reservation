import os


################################### Data Ingestion ##############################################

raw_dir = 'artifacts/raw'
raw_file_path = os.path.join(raw_dir, 'raw.csv')
train_file_path = os.path.join(raw_dir, "train.csv")
test_file_path = os.path.join(raw_dir, "test.csv")

config_path = 'config/config.yaml'


################################### Data processing ##############################################


processed_dir = 'artifacts/processed'
processed_train_data_path = os.path.join(processed_dir, 'processed_train.csv')
processed_test_data_path = os.path.join(processed_dir, 'processed_test.csv')



################################### Data training ##############################################

model_output_path = 'artifacts/models/lgbm_model.pkm'
