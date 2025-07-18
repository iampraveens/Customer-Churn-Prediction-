from CustomerChurn.config.configuration import ConfigurationManager
from CustomerChurn.components.data_transformation import DataTransformation
from CustomerChurn import logger
from pathlib import Path



STAGE_NAME = "Data Transformation stage"

class DataTransformationTrainingPipeline:
    def __init__(self):
        """
        Initializes an instance of the DataTransformationTrainingPipeline class.
        
        This is a special method that Python calls when an object is instantiated from the class.
        """
        pass

    def main(self):
        
        """
        This is the main method of the DataTransformationTrainingPipeline class.

        It is responsible for orchestrating the data transformation process by creating a ConfigurationManager object, retrieving the data transformation configuration, creating a DataTransformation object, loading data, encoding data, performing feature engineering, data balancing, and doing train-test splitting.

        :return: None
        """

        try:
            config = ConfigurationManager()
            data_transformation_config = config.get_data_transformation_config()
            data_transformation = DataTransformation(config=data_transformation_config)
            data = data_transformation.load_data()
            data = data_transformation.encode_data(data=data)
            data = data_transformation.feature_engineering(data=data)
            balanced_data = data_transformation.data_balancing(data=data)
            data_transformation.train_test_splitting(data=balanced_data)

        except Exception as e:
            print(e)
            
if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataTransformationTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e