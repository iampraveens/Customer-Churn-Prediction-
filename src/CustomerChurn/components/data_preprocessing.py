import os
import pandas as pd
from CustomerChurn import logger
from CustomerChurn.entity.config_entity import DataPreprocessingConfig

class DataPreprocessing:
    def __init__(self, config: DataPreprocessingConfig):
        """
        Initializes the DataPreprocessing class with a DataPreprocessingConfig object.
        
        Args:
            config (DataPreprocessingConfig): The configuration object for data preprocessing.
        """
        
        self.config = config
        
    def data_cleaning(self) -> pd.DataFrame:
        """
        Reads the data from the specified path, removes rows with missing values of TotalCharges, 
        converts the TotalCharges column to float, and removes the customerID column.
        
        Args:
            None
        
        Returns:
            pd.DataFrame: The cleaned data.
        """
        try:
            data = pd.read_csv(self.config.data_path)
            data.drop(data[data['TotalCharges'] == " "].index, axis=0, inplace=True)
            data['TotalCharges'] = data['TotalCharges'].astype('float')
            data.drop(columns=['customerID'], axis=1, inplace=True)
            
            cleaned_data_path = os.path.join(self.config.root_dir, "cleaned_data.csv")
            data.to_csv(cleaned_data_path, index=False)
            logger.info(f"Cleaned data saved at {cleaned_data_path}")
            
            return data
        
        except Exception as e:
            logger.exception(e)
            raise e