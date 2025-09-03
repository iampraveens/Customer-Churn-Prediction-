# 📊 Customer Churn Prediction

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/) [![scikit-learn](https://img.shields.io/badge/scikitLearn-1.5.1-green.svg)](https://opensource.org/licenses/MIT) [![MLflow](https://img.shields.io/badge/MLflow-3.3.2-blueviolet.svg)](https://mlflow.org/) [![DVC](https://img.shields.io/badge/DVC-3.62.0-orange.svg)](https://dvc.org/) [![DagsHub](https://img.shields.io/badge/DagsHub-0.6.3-red.svg)](https://dvc.org/)

A complete **end-to-end machine learning project** that predicts customer churn for a telecom company. The project includes **data pipelines with DVC**, **experiment tracking with MLflow/DagsHub**, and a **Flask web application** for real-time churn prediction.

## 🚀 Project Overview

Customer churn is one of the most critical problems in the telecom industry. This project leverages machine learning techniques to predict whether a customer is likely to churn, helping businesses take proactive measures to retain them.

# 🚀 Key Features

- End-to-End ML Pipeline with stages:
  - Data ingestion
  - Data validation
  - Data preprocessing & transformation
  - Model training (Logistic Regression, Random Forest, XGBoost)
  - Model evaluation (Accuracy, F1, Recall, AUC, Confusion Matrix, ROC Curve)
- Data Version Control (DVC) for pipeline reproducibility
- MLflow + Dagshub integration for experiment tracking and model registry
- Class imbalance handling with SMOTEENN / ADASYN
- Feature engineering for improved model performance
- Flask Web App for real-time churn prediction
- Deployment Ready on Render/Heroku with gunicorn

## 🛠️ Installation & Setup

### 1. Clone the repository

```bash
https://github.com/iampraveens/Customer-Churn-Prediction-.git
cd Customer-Churn-Prediction-
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run ML pipeline (DVC)

```bash
dvc repro
```

### 5. Run Flask app locally

```bash
flask run --host=0.0.0.0 --port=8000
```

---

## ☁️ DVC Remote on DagsHub (Step‑by‑Step)

> Use these exact commands to connect your DVC pipeline to DagsHub and push artifacts.

```bash
# Initialize DVC in this repository
dvc init

# Add DagsHub as your DVC remote (replace with your username/repo)
dvc remote add origin https://dagshub.com/<username>/<repo>.dvc

# Make it the default remote
dvc remote default origin
```

**Create a DagsHub Personal Access Token**

1. Open: [https://dagshub.com/settings/tokens](https://dagshub.com/settings/tokens)
2. **Generate New Token** → name it e.g. `dvc_token`
3. Copy the token (you’ll use it as password below)

```bash
# Configure auth for the DVC remote (stored only locally)
dvc remote modify origin --local auth basic
# Use your DagsHub username
dvc remote modify origin --local user your-username
# Paste the personal access token as the password
dvc remote modify origin --local password <YOUR_TOKEN>

# Run the full pipeline and push artifacts to DagsHub
dvc repro
dvc push

# Commit & push code + DVC metadata to GitHub/DagsHub
git add .
git commit -m "Run pipeline and push DVC artifacts"
git push origin main
```

> **Tip:** If a stage is skipped by `dvc repro`, make a minimal change (e.g., bump a param in `params.yaml`) or remove the stage outputs to force re‑run.

---

## 🧪 MLflow + DagsHub Tracking

Track experiments to DagsHub’s MLflow server either **in‑code** (recommended) or via **environment variables**.

### Option A — In‑code initialization (recommended)

```python
# src/CustomerChurn/utils/mlflow.py
import dagshub
import mlflow.sklearn

def setup_mlflow():
    dagshub.init(
        repo_owner="iampraveens",
        repo_name="Customer-Churn-Prediction-",
        mlflow=True,
        dvc=True,
    )
    mlflow.sklearn.autolog()
```

Use inside training/evaluation:

```python
with mlflow.start_run():
    # your fit / predict / log code
    ...
```

### Option B — Environment variables (CI/servers, no interactive login)

```bash
# Point MLflow to DagsHub’s tracking server
export MLFLOW_TRACKING_URI="https://dagshub.com/iampraveens/Customer-Churn-Prediction-.mlflow"

# Basic auth with your DagsHub username + token
export MLFLOW_TRACKING_USERNAME="iampraveens"
export MLFLOW_TRACKING_PASSWORD="<YOUR_TOKEN>"
```

Then, in code, you can use MLflow normally:

```python
import mlflow
with mlflow.start_run():
    mlflow.log_param("chosen_model", model_name)
    mlflow.log_metric("accuracy", acc)
```

> **Where to see runs?**\
> Your runs and metrics will be visible at:\
> `https://dagshub.com/iampraveens/Customer-Churn-Prediction-.mlflow`

---

## 💻 Usage Example

1. Open the Flask app in browser: `http://127.0.0.1:8000`
2. Fill in customer details in the form
3. Get churn prediction result with probability score:

```text
⚠️ Customer is likely to churn.
Churn Probability: 0.75

✅ Customer is not likely to churn.
Churn Probability: 0.20
```

---

## 📂 Project Structure

```
iampraveens-customer-churn-prediction-/
├── README.md                  # Project documentation
├── app.py                     # Flask web application
├── dvc.lock                   # DVC lock file for reproducibility
├── dvc.yaml                   # DVC pipeline stages
├── LICENSE                    # MIT License
├── main.py                    # Main pipeline orchestrator
├── params.yaml                # Model hyperparameters and configs
├── Procfile                   # For Heroku deployment
├── requirements.txt           # Python dependencies
├── schema.yaml                # Data schema for validation
├── setup.py                   # Package setup
├── template.py                # Project scaffolding script
├── .dvcignore                 # DVC ignore patterns
├── artifacts/                 # Pipeline outputs (data, models, metrics)
│   ├── data_ingestion/        # Ingested raw data
│   ├── data_preprocessing/    # Cleaned data
│   ├── data_transformation/   # Transformed train/test sets
│   ├── data_validation/       # Validation status
│   ├── model_evaluation/      # Metrics and plots
│   └── model_trainer/         # Trained models
├── config/                    # Configuration files
│   └── config.yaml
├── research/                  # Jupyter notebooks for experiments
│   ├── 01_data_ingestion.ipynb
│   ├── 02_data_validation.ipynb
│   ├── 03_data_preprocessing.ipynb
│   ├── 04_data_transformation.ipynb
│   ├── 05_model_training.ipynb
│   ├── 06_model_evaluation.ipynb
│   ├── experiments.ipynb
│   └── trials.ipynb
├── saved_models/              # Persisted models for app
│   └── model.joblib
├── src/                       # Source code
│   └── CustomerChurn/
│       ├── components/        # Pipeline components (ingestion, validation, etc.)
│       ├── config/            # Config management
│       ├── constants/         # Constants like file paths
│       ├── entity/            # Data classes for configs
│       ├── pipeline/          # Pipeline stage scripts
│       └── utils/             # Utilities (YAML reading, MLflow setup)
├── static/                    # Web app static files
│   └── css/
│       ├── style.css
│       └── js/
│           └── scripts.js
├── templates/                 # Flask HTML templates
│   ├── index.html             # Input form
│   └── result.html            # Prediction result
└── .dvc/                      # DVC configuration
    ├── config
    └── .gitignore
```

---

## 📦 Dependencies

- Python 3.10+
- Flask
- Scikit-learn
- XGBoost
- Pandas, NumPy
- Matplotlib, Seaborn
- Imbalanced-learn
- DVC
- MLflow
- Dagshub

Install via:

```bash
pip install -r requirements.txt
```

---

## 🤝 Contribution Guidelines

Contributions are welcome! To contribute:

1. Fork the repo
2. Create a new branch (`feature-xyz`)
3. Commit your changes
4. Push the branch
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

Developed with ❤️ by **Praveen S** ([GitHub](https://github.com/iampraveens))
