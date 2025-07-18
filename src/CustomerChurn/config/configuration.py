from CustomerChurn.constants import *
from CustomerChurn.utils.common import read_yaml, create_directories
from CustomerChurn.entity.config_entity import DataIngestionConfig
from CustomerChurn.entity.config_entity import DataValidationConfig

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