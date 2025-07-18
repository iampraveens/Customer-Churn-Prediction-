from CustomerChurn.config.configuration import ConfigurationManager
from CustomerChurn.components.data_ingestion import DataIngestion
from CustomerChurn import logger

STAGE_NAME = "Data Ingestion stage"

class DataIngestionTrainingPipeline:
    """
        Initializes the DataIngestionTrainingPipeline class.
        
        This is a class constructor method that is automatically called when an object 
        of the class is created.
        """
    def __init__(self):
        pass
    
    def main(self):
        """
        This is the main method of the DataIngestionTrainingPipeline class.
        
        It is responsible for orchestrating the data ingestion process by creating 
        a ConfigurationManager object, retrieving the data ingestion configuration, 
        creating a DataIngestion object, and calling its download_file and 
        extract_zip_file methods.
        """
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.extract_zip_file()
        

if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e