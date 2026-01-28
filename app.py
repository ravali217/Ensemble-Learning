import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------
# Sample placeholder ML logic
# Replace with your trained stacking model later
# -----------------------------
def predict_base_models(input_df):
    """
    Simulate base model predictions.
    In reality, you would load your trained models and predict here.
    """
    # Simple rules for demonstration
    lr_pred = "Approved" if input_df['ApplicantIncome'][0] > 5000 else "Rejected"
    dt_pred = "Approved" if input_df['CreditHistory'][0] == 1 else "Rejected"
    rf_pred = "Approved" if input_df['LoanAmount'][0] < 200 else "Rejected"
    
    return lr_pred, dt_pred, rf_pred

def stacking_meta_model(lr, dt, rf):
    """
    Simple stacking meta model logic for demo:
    If majority of base models approve → Approved
    """
    approvals = [lr, dt, rf].count("Approved")
    if approvals >= 2:
        final = "Approved"
        confidence = (approvals/3)*100
    else:
        final = "Rejected"
        confidence = ((3-approvals)/3)*100
    return final, confidence

# -----------------------------
# Streamlit App
# -----------------------------

st.set_page_config(page_title="Smart Loan Approval System", page_icon="🎯", layout="centered")

# Title & Description
st.title("🎯 Smart Loan Approval System – Stacking Model")
st.markdown(
    "This system uses a **Stacking Ensemble Machine Learning model** to predict whether a loan will be approved "
    "by combining multiple ML models for better decision making."
)

st.sidebar.header("Applicant Details")

# Sidebar Input Section
applicant_income = st.sidebar.number_input("Applicant Income", min_value=0, step=1000)
coapplicant_income = st.sidebar.number_input("Co-Applicant Income", min_value=0, step=1000)
loan_amount = st.sidebar.number_input("Loan Amount", min_value=0, step=1000)
loan_term = st.sidebar.number_input("Loan Amount Term (in months)", min_value=0, step=12)
credit_history = st.sidebar.radio("Credit History", options=["Yes", "No"])
employment_status = st.sidebar.selectbox("Employment Status", options=["Salaried", "Self-Employed"])
property_area = st.sidebar.selectbox("Property Area", options=["Urban", "Semi-Urban", "Rural"])

# Convert Credit History to numeric
credit_history_val = 1 if credit_history == "Yes" else 0

# Prepare input dataframe
input_data = pd.DataFrame({
    "ApplicantIncome": [applicant_income],
    "CoapplicantIncome": [coapplicant_income],
    "LoanAmount": [loan_amount],
    "Loan_Amount_Term": [loan_term],
    "CreditHistory": [credit_history_val],
    "EmploymentStatus": [employment_status],
    "PropertyArea": [property_area]
})

# -----------------------------
# Model Architecture Display
# -----------------------------
st.subheader("🔧 Stacking Model Architecture")
st.markdown("""
**Base Models Used:**
- Logistic Regression
- Decision Tree
- Random Forest

**Meta Model Used:**
- Logistic Regression

*Stacking combines predictions of base models to improve overall accuracy.*
""")

# -----------------------------
# Prediction Section
# -----------------------------
if st.button("🔘 Check Loan Eligibility (Stacking Model)"):
    # Get base model predictions
    lr_pred, dt_pred, rf_pred = predict_base_models(input_data)
    
    # Get stacking meta model result
    final_pred, confidence = stacking_meta_model(lr_pred, dt_pred, rf_pred)
    
    # -----------------------------
    # Output Section
    # -----------------------------
    st.subheader("📊 Base Model Predictions")
    st.write(f"**Logistic Regression →** {lr_pred}")
    st.write(f"**Decision Tree →** {dt_pred}")
    st.write(f"**Random Forest →** {rf_pred}")
    
    st.subheader("🧠 Final Stacking Decision")
    if final_pred == "Approved":
        st.success(f"✅ Loan Approved (Confidence: {confidence:.1f}%)")
    else:
        st.error(f"❌ Loan Rejected (Confidence: {confidence:.1f}%)")
    
    # -----------------------------
    # Business Explanation
    # -----------------------------
    st.subheader("💡 Business Explanation")
    explanation = (
        f"Based on income, credit history, and combined predictions from multiple models, "
        f"the applicant is **{'likely' if final_pred=='Approved' else 'unlikely'}** to repay the loan. "
        f"Therefore, the stacking model predicts loan **{final_pred}**."
    )
    st.info(explanation)
