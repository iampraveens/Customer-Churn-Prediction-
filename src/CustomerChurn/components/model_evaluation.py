from pathlib import Path 
import os
import pandas as pd 
from sklearn.metrics import accuracy_score, f1_score, recall_score, roc_auc_score, confusion_matrix, ConfusionMatrixDisplay, RocCurveDisplay
import joblib
import mlflow
import matplotlib.pyplot as plt
from CustomerChurn.entity.config_entity import ModelEvaluationConfig
from CustomerChurn.utils.common import save_json
from CustomerChurn import logger
from CustomerChurn.utils.mlflow import setup_mlflow

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        """
        Constructor for ModelEvaluation class

        Parameters
        ----------
        config : ModelEvaluationConfig
            Configuration for model evaluation
        """
        
        self.config = config
        setup_mlflow()

    def eval_metrics(self, actual, pred, proba):
        """
        Evaluate performance metrics for model predictions.

        Parameters
        ----------
        actual : array-like
            True labels of the test data.
        pred : array-like
            Predicted labels by the model.
        proba : array-like
            Predicted probabilities for the positive class.

        Returns
        -------
        accuracy : float
            Ratio of correctly predicted labels to total labels.
        f1 : float
            F1 score, the harmonic mean of precision and recall.
        recall : float
            Recall score, the ratio of true positives to actual positives.
        auc : float
            Area Under the Receiver Operating Characteristic Curve (ROC AUC).
        """

        accuracy = accuracy_score(actual, pred)
        f1 = f1_score(actual, pred)
        recall = recall_score(actual, pred)
        auc = roc_auc_score(actual, proba)
        return accuracy, f1, recall, auc
    
    def save_results(self):
        """
        Evaluate model on test data, save metrics and visualizations.

        This method reads test data and model from the specified paths in the 
        configuration, evaluates the model's performance on the test data by 
        calculating various metrics such as accuracy, F1 score, recall, and AUC. 
        It saves these metrics to a JSON file. Additionally, it generates and 
        saves a confusion matrix and ROC curve plot as visualizations.

        Exceptions:
            AttributeError: If the model does not support probability predictions, 
            fall back to using predicted labels.

        Logs:
            Information about successful saving of evaluation metrics and visualizations.
        """

        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        X_test = test_data.drop([self.config.target_column], axis=1)
        y_test = test_data[self.config.target_column]  

        y_pred = model.predict(X_test)

        # Handle probability output
        try:
            y_proba = model.predict_proba(X_test)[:, 1]
        except AttributeError:
            y_proba = y_pred  # Fallback if model has no predict_proba

        # Calculate metrics
        accuracy, f1, recall, auc = self.eval_metrics(y_test, y_pred, y_proba)

        # Save metrics to JSON
        scores = {
            "accuracy": accuracy,
            "f1_score": f1,
            "recall_score": recall,
            "auc_score": auc
        }
        save_json(path=Path(self.config.metric_file_name), data=scores)
        
        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot(cmap=plt.cm.Blues)
        cm_path = os.path.join(self.config.root_dir, "confusion_matrix.png")
        plt.title("Confusion Matrix")
        plt.savefig(cm_path)
        plt.close()

        # ROC Curve
        RocCurveDisplay.from_predictions(y_test, y_proba)
        roc_path = os.path.join(self.config.root_dir, "roc_curve.png")
        plt.title("ROC Curve")
        plt.savefig(roc_path)
        plt.close()

        logger.info("Evaluation metrics and visualizations saved successfully.")

        with mlflow.start_run(run_name="model_evaluation"):
            mlflow.log_metrics(scores)
            mlflow.log_artifact(self.config.metric_file_name)
            mlflow.log_artifact(cm_path)
            mlflow.log_artifact(roc_path)
            mlflow.log_param("target_column", self.config.target_column)
            mlflow.log_param("test_data_rows", len(X_test))