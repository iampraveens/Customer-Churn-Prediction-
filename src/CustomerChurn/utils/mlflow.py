import dagshub
import mlflow.sklearn

def setup_mlflow():
    # Initialize MLflow with DagsHub
    dagshub.init(
        repo_owner="iampraveens",
        repo_name="Customer-Churn-Prediction-",
        mlflow=True,
        dvc=True
    )
    # Enable automatic logging
    mlflow.sklearn.autolog()
