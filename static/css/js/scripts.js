document.addEventListener("DOMContentLoaded", () => {
    console.log("Churn Prediction App Loaded ✅");

    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", (e) => {
            const tenure = document.querySelector("input[name='tenure']").value;
            if (tenure < 0) {
                e.preventDefault();
                alert("Tenure cannot be negative!");
            }
        });
    }

    // Add focus effect to result card if present
    const resultCard = document.querySelector(".result-card");
    if (resultCard) {
        resultCard.classList.add("fade-in");
    }
});