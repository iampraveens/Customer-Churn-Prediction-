import os
import pandas as pd
from typing import Union
from CustomerChurn import logger
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import ADASYN
from imblearn.combine import SMOTEENN
from CustomerChurn.entity.config_entity import DataTransformationConfig

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
    
    def load_data(self) -> pd.DataFrame:
        try:
            data = pd.read_csv(self.config.data_path)
            logger.info("Data loaded successfully.")
            return data
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise e

    def encode_data(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            binary_columns = ['Partner', 'Dependents', 'PaperlessBilling', 'Churn', 'PhoneService']
            data[binary_columns] = data[binary_columns].map(lambda x: 1 if x == 'Yes' else 0)
            
            data['gender'] = data['gender'].apply(lambda x: 1 if x == 'Female' else 0)

            data['MultipleLines'] = data['MultipleLines'].map({'No phone service': 0, 'No': 0, 'Yes': 1})

            internet_service_columns = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
            data[internet_service_columns] = data[internet_service_columns].replace({'No internet service': 0, 'No': 0, 'Yes': 1})

            categorical_columns = ['InternetService', 'Contract', 'PaymentMethod']
            data = pd.get_dummies(data, columns=categorical_columns, drop_first=True, dtype='int')

            return data

        except Exception as e:
            logger.error(f"Error during data encoding: {str(e)}")
            raise e

    def feature_engineering(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            data['avg_monthly_value'] = data['TotalCharges'] / (data['tenure'] + 1)
            data['tenure_ratio'] = data['tenure'] / (data['TotalCharges'] + 1)
            data['service_density'] = data['OnlineSecurity'] + data['OnlineBackup'] + data['TechSupport']
            data['tenure_MonthlyCharges'] = data['tenure'] * data['MonthlyCharges']
            logger.info("Feature engineering complete.")
            return data
        
        except Exception as e:
            logger.error(f"Error in feature engineering: {str(e)}")
            raise e

    def data_balancing(self, data: pd.DataFrame) -> Union[pd.DataFrame, pd.Series]:
        try:
            X = data.drop('Churn', axis=1)
            y = data['Churn']
            method = self.config.balancing_method
            
            if method == 'SMOTEENN':
                smoteenn = SMOTEENN()
                X_res, y_res = smoteenn.fit_resample(X, y)
                logger.info("Data balanced using SMOTEENN.")
            elif method == 'ADASYN':
                adasyn = ADASYN()
                X_res, y_res = adasyn.fit_resample(X, y)
                logger.info("Data balanced using ADASYN.")
            else:
                raise ValueError(f"Invalid method: {method}. Choose either 'SMOTEENN' or 'ADASYN'.")
            
            logger.info(f"Before balancing: {y.value_counts()}")
            logger.info(f"After balancing: {y_res.value_counts()}")
            
            balanced_data = pd.DataFrame(X_res, columns=X.columns)
            balanced_data['Churn'] = y_res.values
            return balanced_data

        except Exception as e:
            logger.error(f"Error during data balancing: {str(e)}")
            raise e

    def train_test_splitting(self, data: pd.DataFrame):
        
        try:
            train, test = train_test_split(data, test_size=0.2, random_state=42, stratify=data['Churn'])

            if isinstance(train, pd.DataFrame) and isinstance(test, pd.DataFrame):
                train.to_csv(os.path.join(self.config.root_dir, "train.csv"), index=False)
                test.to_csv(os.path.join(self.config.root_dir, "test.csv"), index=False)

                logger.info("Data split into training and test sets.")
                logger.info(f"Train set shape: {train.shape}")
                logger.info(f"Test set shape: {test.shape}")
                logger.info(f"Train CSV saved to: {os.path.join(self.config.root_dir, 'train.csv')}")
                logger.info(f"Test CSV saved to: {os.path.join(self.config.root_dir, 'test.csv')}")
            else:
                raise ValueError("Train-test split did not return DataFrames.")

        except Exception as e:
            logger.error(f"Error during train-test splitting: {str(e)}")
            raise e