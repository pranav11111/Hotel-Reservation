import os
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_functions import read_yaml, load_data
from scipy.stats import randint
import mlflow
import mlflow.sklearn

logger = get_logger(__name__)

class ModelTrainer:

    def __init__(self, train_path, test_path, model_output_path):
        self.trainpath = train_path
        self.testpath = test_path
        self.model_output_path = model_output_path


        self.params_dist = light_params
        self.randomsearch_params = random_search_params

    def load_split_data(self):
        try:
            logger.info(f'Loading data from {self.trainpath}')
            train_df = load_data(self.trainpath)
            
            logger.info(f'Loading data from {self.testpath}')
            test_df = load_data(self.testpath)


            x_train = train_df.drop('booking_status', axis= 1)
            y_train = train_df['booking_status']

            x_test = test_df.drop('booking_status', axis= 1)
            y_test = test_df['booking_status']

            logger.info('Data spliting done for model training')

            return x_train, x_test, y_train, y_test
        except Exception as e:
            logger.error(f'Error while loading data {e}')
            raise CustomException('Failed to load data', e)
    

    def train(self, x_train, y_train):
        try:
            logger.info('Initializing model')

            model = lgb.LGBMClassifier(random_state= self.randomsearch_params['random_state'])

            logger.info('starting hyper parameter tuning')

            random_search = RandomizedSearchCV(
                estimator= model,
                param_distributions= self.params_dist,
                n_iter= self.randomsearch_params['n_iter'],
                cv= self.randomsearch_params['cv'],
                verbose= self.randomsearch_params['verbose'],
                random_state= self.randomsearch_params['random_state'],
                scoring= self.randomsearch_params['scoring']
            )

            logger.info('Fitting random search cv')

            random_search.fit(x_train, y_train)

            logger.info("Hyperparameter tuning done")

            best_param = random_search.best_params_

            best_lgbm = random_search.best_estimator_

            logger.info(f'Best params are {best_param}')

            return best_lgbm
        
        except Exception as e:
            logger.error(f'Error while hyperparamter tuning {e}')
            raise CustomException('Failed to find best hyper parameter', e)
        
    def eval_model(self, model, x_test, y_test):
        try:
            logger.info('Evaluating our model')

            pred = model.predict(x_test)
            accuray = accuracy_score(y_test, pred)
            precision = precision_score(y_test, pred)
            recall = recall_score(y_test, pred)
            f1 = f1_score(y_test, pred)

            logger.info(f'Accuracy: {accuray}, precision : {precision}, recall : {recall}, f1 : {f1}')

            return {
                'accuracy': accuray,
                'precision': precision,
                'recall': recall,
                'f1': f1,
            }
        except Exception as e:
            logger.error(f'Error while evaluation {e}')
            raise CustomException('Failed evaluate the model', e)
    
    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok= True)

            logger.info('Made model directory')

            joblib.dump(model, self.model_output_path)

            logger.info(f'model saved to {self.model_output_path}')

        except Exception as e:
            logger.error(f'Error while saving{e}')
            raise CustomException('Failed save the model', e)
        
    def run_model(self):
        try:
            with mlflow.start_run():
                logger.info('starting training pipeline')

                logger.info("Starting ML flow experimentation")

                logger.info('Logging the training and testing data to mlflow')
                mlflow.log_artifact(self.trainpath, artifact_path= 'Datasets')
                mlflow.log_artifact(self.testpath, artifact_path= 'Datasets')

                x_train, x_test, y_train, y_test = self.load_split_data()
                model = self.train(x_train, y_train)
                metrics = self.eval_model(model, x_test, y_test)
                self.save_model(model)

                logger.info('Logging the model, params and metrics to mlflow')
                mlflow.log_artifact(self.model_output_path)
                mlflow.log_params(model.get_params())
                mlflow.log_metrics(metrics)

                logger.info("model training succesfully completed")
        except Exception as e:
            logger.error(f'Error while in pipeline{e}')
            raise CustomException('Failed during pipeline', e)
            
if __name__ == '__main__':
    trainer = ModelTrainer(processed_train_data_path, processed_test_data_path, model_output_path)
    trainer.run_model()
