from flask import Flask, render_template, request
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load the trained model
MODEL_PATH = os.path.join("saved_models", "model.joblib")
model = joblib.load(MODEL_PATH)


def preprocess_input(form):
    """
    Preprocess form input to match training features.
    """
    # Numeric
    tenure = float(form.get("tenure"))
    MonthlyCharges = float(form.get("MonthlyCharges"))
    TotalCharges = float(form.get("TotalCharges"))
    SeniorCitizen = int(form.get("SeniorCitizen"))

    # Binary mappings
    Partner = 1 if form.get("Partner") == "Yes" else 0
    Dependents = 1 if form.get("Dependents") == "Yes" else 0
    PhoneService = 1 if form.get("PhoneService") == "Yes" else 0
    PaperlessBilling = 1 if form.get("PaperlessBilling") == "Yes" else 0
    gender = 1 if form.get("gender") == "Female" else 0

    # MultipleLines
    MultipleLines = 1 if form.get("MultipleLines") == "Yes" else 0

    # Internet-related services
    OnlineSecurity = 1 if form.get("OnlineSecurity") == "Yes" else 0
    OnlineBackup = 1 if form.get("OnlineBackup") == "Yes" else 0
    DeviceProtection = 1 if form.get("DeviceProtection") == "Yes" else 0
    TechSupport = 1 if form.get("TechSupport") == "Yes" else 0
    StreamingTV = 1 if form.get("StreamingTV") == "Yes" else 0
    StreamingMovies = 1 if form.get("StreamingMovies") == "Yes" else 0

    # One-hot encoding for InternetService
    InternetService = form.get("InternetService")
    InternetService_Fiber_optic = 1 if InternetService == "Fiber optic" else 0
    InternetService_No = 1 if InternetService == "No" else 0
    # Baseline (DSL) is dropped

    # One-hot encoding for Contract
    Contract = form.get("Contract")
    Contract_One_year = 1 if Contract == "One year" else 0
    Contract_Two_year = 1 if Contract == "Two year" else 0
    # Baseline (Month-to-month) is dropped

    # One-hot encoding for PaymentMethod
    PaymentMethod = form.get("PaymentMethod")
    PaymentMethod_Credit_card = 1 if PaymentMethod == "Credit card (automatic)" else 0
    PaymentMethod_Electronic_check = 1 if PaymentMethod == "Electronic check" else 0
    PaymentMethod_Mailed_check = 1 if PaymentMethod == "Mailed check" else 0
    # Baseline (Bank transfer (automatic)) is dropped

    # Feature engineering
    avg_monthly_value = TotalCharges / (tenure + 1)
    tenure_ratio = tenure / (TotalCharges + 1)
    service_density = OnlineSecurity + OnlineBackup + TechSupport
    tenure_MonthlyCharges = tenure * MonthlyCharges

    # Final feature vector
    features = [
        tenure, MonthlyCharges, TotalCharges,
        SeniorCitizen, Partner, Dependents, PhoneService, PaperlessBilling,
        gender, MultipleLines, OnlineSecurity, OnlineBackup,
        DeviceProtection, TechSupport, StreamingTV, StreamingMovies,
        InternetService_Fiber_optic, InternetService_No,
        Contract_One_year, Contract_Two_year,
        PaymentMethod_Credit_card, PaymentMethod_Electronic_check, PaymentMethod_Mailed_check,
        avg_monthly_value, tenure_ratio, service_density, tenure_MonthlyCharges
    ]

    return np.array(features).reshape(1, -1)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        features = preprocess_input(request.form)
        prediction = model.predict(features)[0]
        probability = (
            model.predict_proba(features)[0][1]
            if hasattr(model, "predict_proba")
            else None
        )

        result_text = (
            "Customer is likely to churn."
            if prediction == 1
            else "Customer is not likely to churn."
        )

        return render_template(
            "result.html",
            prediction=result_text,
            probability=f"{probability:.2f}" if probability is not None else "N/A",
        )
    except Exception as e:
        return render_template("result.html", prediction=f"Error: {str(e)}", probability="N/A")


if __name__ == "__main__":
    app.run(debug=True)
