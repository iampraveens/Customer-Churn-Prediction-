import pandas as pd 
import os
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from CustomerChurn import logger
from CustomerChurn.entity.config_entity import ModelTrainerConfig
from CustomerChurn.utils.common import read_yaml

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config
        
    def train(self):
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)

        X_train = train_data.drop([self.config.target_column], axis=1)
        X_test = test_data.drop([self.config.target_column], axis=1)
        y_train = train_data[self.config.target_column]
        y_test = test_data[self.config.target_column]

        model_name = self.config.model
        params = self.config.params

        if model_name == 'LogisticRegression':
            model = LogisticRegression(max_iter=params['max_iter'])
        elif model_name == 'RandomForestClassifier':
            model = RandomForestClassifier(
                n_estimators=params['n_estimators'],
                max_depth=params['max_depth'],
                min_samples_split=params['min_samples_split'],
                min_samples_leaf=params['min_samples_leaf'],
                max_features=params['max_features'],
                criterion=params['criterion']
            )
        elif model_name == 'XGBClassifier':
            model = XGBClassifier(
                max_depth=params['max_depth'],
                learning_rate=params['learning_rate'],
                n_estimators=params['n_estimators'],
                subsample=params['subsample'],
                colsample_bytree=params['colsample_bytree']
            )
        else:
            raise ValueError(f"Invalid model name: {model_name}")

        logger.info(f"Training {model_name} model with parameters: {params}")   
        model.fit(X_train, y_train)
        joblib.dump(model, os.path.join(self.config.root_dir, self.config.model_name))
        logger.info(f"{model_name} model trained and saved successfully.")