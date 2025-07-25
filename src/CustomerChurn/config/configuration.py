from CustomerChurn.constants import *
from CustomerChurn.utils.common import read_yaml, create_directories
from CustomerChurn.entity.config_entity import DataIngestionConfig
from CustomerChurn.entity.config_entity import DataValidationConfig
from CustomerChurn.entity.config_entity import DataPreprocessingConfig
from CustomerChurn.entity.config_entity import DataTransformationConfig
from CustomerChurn.entity.config_entity import ModelTrainerConfig
from CustomerChurn.entity.config_entity import ModelEvaluationConfig

class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH,
        schema_filepath = SCHEMA_FILE_PATH):
        
        """
        Initializes the ConfigurationManager class with file paths to configuration,
        parameters, and schema files.

        Args:
            config_filepath (str): Path to configuration YAML file.
            params_filepath (str): Path to parameters YAML file.
            schema_filepath (str): Path to schema YAML file.

        Attributes:
            config (dict): Configuration dictionary.
            params (dict): Parameters dictionary.
            schema (dict): Schema dictionary.
        """
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)
        
        create_directories([self.config.artifacts_root])
        
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Retrieves and constructs the data ingestion configuration.

        This method reads the data ingestion part of the configuration file, 
        ensures the necessary directories are created, and returns a 
        DataIngestionConfig object with the relevant settings.

        Returns:
            DataIngestionConfig: An object containing configuration settings 
            such as root directory, source URL, local data file path, and 
            unzip directory for data ingestion.
        """

        config = self.config.data_ingestion
        
        create_directories([config.root_dir])
        
        data_ingestion_config = DataIngestionConfig(
            root_dir = config.root_dir,
            source_URL = config.source_URL,
            local_data_file = config.local_data_file,
            unzip_dir = config.unzip_dir
        )
        
        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        """
        Retrieves and constructs the data validation configuration.

        This method reads the data validation part of the configuration file, 
        ensures the necessary directories are created, and returns a 
        DataValidationConfig object with the relevant settings.

        Returns:
            DataValidationConfig: An object containing configuration settings 
            such as root directory, unzip data directory, status file path, and 
            schema for data validation.
        """
        config = self.config.data_validation
        schema = self.schema.COLUMNS
        
        create_directories([config.root_dir])
        
        data_validation_config = DataValidationConfig(
            root_dir = config.root_dir,
            unzip_data_dir = config.unzip_data_dir,
            STATUS_FILE = config.STATUS_FILE,
            all_schema=schema
        )
        
        return data_validation_config
    
    def get_data_preprocessing_config(self) -> DataPreprocessingConfig:
        """
        Retrieves and constructs the data preprocessing configuration.

        This method reads the data preprocessing part of the configuration file, 
        ensures the necessary directories are created, and returns a 
        DataPreprocessingConfig object with the relevant settings.

        Returns:
            DataPreprocessingConfig: An object containing configuration settings 
            such as root directory and data path for data preprocessing.
        """

        config = self.config.data_preprocessing
        
        create_directories([config.root_dir])
        
        data_preprocessing_config = DataPreprocessingConfig(
            root_dir = config.root_dir,
            data_path = config.data_path
        )
        
        return data_preprocessing_config
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation
        params = self.params.DataTransformation

        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            balancing_method=params.balancing_method
        )

        return data_transformation_config
    
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        """
        Retrieves and constructs the model trainer configuration.

        This method reads the model trainer part of the configuration file, 
        ensures the necessary directories are created, and returns a 
        ModelTrainerConfig object with the relevant settings.

        Returns:
            ModelTrainerConfig: An object containing configuration settings 
            such as root directory, train data path, test data path, model name, 
            target column, and model type for model training.
        """
        config = self.config.model_trainer
        model_type = self.params.ModelTrainer.model  
        model_params = self.params[model_type]             
        schema = self.schema.TARGET_COLUMN

        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir=config.root_dir,
            train_data_path=config.train_data_path,
            test_data_path=config.test_data_path,
            model_name=config.model_name,
            target_column=schema.name,
            model=model_type,
            params=model_params
        )

        return model_trainer_config
    
    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        """
        Retrieves and constructs the model evaluation configuration.

        This method reads the model evaluation part of the configuration file, 
        ensures the necessary directories are created, and returns a 
        ModelEvaluationConfig object with the relevant settings.

        Returns:
            ModelEvaluationConfig: An object containing configuration settings 
            such as root directory, test data path, model path, metric file name, 
            and target column for model evaluation.
        """
        config = self.config.model_evaluation
        schema =  self.schema.TARGET_COLUMN

        create_directories([config.root_dir])

        model_evaluation_config = ModelEvaluationConfig(
            root_dir=config.root_dir,
            test_data_path=config.test_data_path,
            model_path = config.model_path,
            metric_file_name = config.metric_file_name,
            target_column = schema.name
           
        )

        return model_evaluation_config