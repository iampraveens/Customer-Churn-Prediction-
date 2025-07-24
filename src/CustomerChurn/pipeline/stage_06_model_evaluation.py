from CustomerChurn.config.configuration import ConfigurationManager
from CustomerChurn.components.model_evaluation import ModelEvaluation
from CustomerChurn import logger


STAGE_NAME = "Model Evaluation stage"


class ModelEvaluationTrainingPipeline:
    def __init__(self):
        """
        Initializes an instance of the class.
        This is a special method that Python calls when an object is instantiated from the class.
        """
        pass

    def main(self):
        """
        Executes the main function of the class.
        This function initializes a `ConfigurationManager` object and retrieves the model evaluation
        configuration using the `get_model_evaluation_config` method. It then creates a `ModelEvaluation`
        object with the retrieved configuration. Finally, it calls the `save_results` method of the
        `ModelEvaluation` object.
        Parameters:
            self (ModelEvaluationTrainingPipeline): The instance of the class.
        """
        config = ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()
        model_evaluation_config = ModelEvaluation(config=model_evaluation_config)
        model_evaluation_config.save_results()


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ModelEvaluationTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e