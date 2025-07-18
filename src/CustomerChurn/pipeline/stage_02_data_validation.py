from CustomerChurn.config.configuration import ConfigurationManager
from CustomerChurn.components.data_validation import DataValidation
from CustomerChurn import logger


STAGE_NAME = "Data Validation stage"

class DataValidationTrainingPipeline:
    """
        Initializes an instance of the DataValidationTrainingPipeline class.
        
        This is a special method that Python calls when an object is instantiated from the class.
        """
    def __init__(self):
        """
        Initializes an instance of the class.
        This is a special method that Python calls when an object is instantiated from the class.
        """
        pass

    def main(self):
        """
        This is the main method of the DataValidationTrainingPipeline class.
        
        It is responsible for initializing the ConfigurationManager, 
        retrieving the data validation configuration, 
        creating an instance of the DataValidation class, 
        and validating all columns based on the configuration.
        """
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(config=data_validation_config)
        data_validation.validate_all_columns()


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataValidationTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e