from CustomerChurn.config.configuration import ConfigurationManager
from CustomerChurn.components.model_trainer import ModelTrainer
from CustomerChurn import logger

STAGE_NAME = "Model Trainer stage"

class ModelTrainerTrainingPipeline:
    def __init__(self):
        """
        Initializes an instance of the class.
        This is a special method that Python calls when an object is instantiated from the class.
        """
        pass

    def main(self):
        """
        This function is the main entry point of the ModelTrainerTrainingPipeline class.
        It is responsible for initializing the ConfigurationManager, retrieving the model trainer configuration,
        creating an instance of the ModelTrainer class, and triggering the model training process.
        
        Parameters:
            self (ModelTrainerTrainingPipeline): The instance of the class.
        """
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer_config = ModelTrainer(config=model_trainer_config)
        model_trainer_config.train()


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ModelTrainerTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e