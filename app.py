import streamlit as st
import requests

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Avoidable ED Visit Prediction",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.title("📘 Project Info")
    st.markdown("""
    This app predicts whether an emergency department (ED) visit is avoidable based on patient demographics and clinical classification.

    **Model:** Trained on synthetic claims data  
    **Backend:** FastAPI deployed on Render  
    **Frontend:** Streamlit deployed on Streamlit Cloud  
    **Experiments:** 16 tracked via Dagshub  
    **Database:** Normalized schema on Render  
    """)
    st.markdown("---")
    st.markdown("🔗 [View GitHub Repo](https://github.com/menna1996/avoidable_ed_ml_project)")
    st.markdown("🔗 [View Dagshub Dashboard](https://dagshub.com/menna1996/avoidable_ed_ml_project)")
    st.markdown("🔗 [View FastAPI Endpoint](https://avoidable-ed-api.onrender.com/docs)")

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.title("🏥 Avoidable ED Visit Prediction")
st.markdown("Use patient demographics and clinical classification to predict whether an ED visit is avoidable.")

st.divider()

# ---------------------------------------------------------
# PATIENT INFO
# ---------------------------------------------------------
with st.expander("👤 Patient Information", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        age = st.slider("Age", 0, 120, 65, help="Patient age at end of reference year")
        sex = st.selectbox("Sex", ["Male", "Female"], help="Biological sex")
        race = st.selectbox("Race", ["White", "Black", "Asian", "Hispanic", "Other", "North American Native", "Unknown"], help="Self-reported race")
    with col2:
        year = st.number_input("Year", min_value=2020, max_value=2100, value=2023, help="Reference year for the visit")
        total_paid_amt = st.number_input("Total Paid Amount ($)", min_value=0.0, value=0.0, help="Total amount paid for the visit")
        chronic = st.selectbox("Chronic Condition", ["No", "Yes"], help="Does the patient have a chronic condition?")

st.divider()

# ---------------------------------------------------------
# CLINICAL CLASSIFICATION
# ---------------------------------------------------------
with st.expander("🧠 Clinical Classification", expanded=True):
    body_system_map = {
        "Blood/Immune": "bodysystem_bloodimmune",
        "Circulatory": "bodysystem_circulatory",
        "Dental": "bodysystem_dental",
        "Digestive": "bodysystem_digestive",
        "Ear": "bodysystem_ear",
        "Endocrine/Metabolic": "bodysystem_endocrine",
        "External Causes": "bodysystem_externalcauses",
        "Eye": "bodysystem_eye",
        "Health Status/Contact": "bodysystem_healthstatus",
        "Genitourinary": "bodysystem_genitourinary",
        "Infectious": "bodysystem_infectious",
        "Injury/Poisoning": "bodysystem_injurypoisoning",
        "Congenital": "bodysystem_congenital",
        "Mental/Behavioral": "bodysystem_mentalbehavioral",
        "Musculoskeletal": "bodysystem_musculoskeletal",
        "Neoplasms": "bodysystem_neoplasms",
        "Nervous System": "bodysystem_nervoussystem",
        "Perinatal": "bodysystem_perinatal",
        "Pregnancy/Childbirth": "bodysystem_pregnancy",
        "Respiratory": "bodysystem_respiratory",
        "Skin/Subcutaneous": "bodysystem_skin",
        "Symptoms/Signs": "bodysystem_symptoms",
        "Unacceptable Diagnosis": "bodysystem_unacceptable"
    }

    selected_body_system = st.selectbox("Primary Body System", list(body_system_map.keys()), help="Clinical classification of the primary diagnosis")

st.divider()

# ---------------------------------------------------------
# MAPPINGS
# ---------------------------------------------------------
sex_map = {"Male": "1", "Female": "2"}
race_map = {
    "Unknown": "0", "White": "1", "Black": "2", "Other": "3",
    "Asian": "4", "Hispanic": "5", "North American Native": "6"
}
chronic_map = {"No": 0, "Yes": 1}

body_system_payload = {v: 0 for v in body_system_map.values()}
body_system_payload[body_system_map[selected_body_system]] = 1

payload = {
    "AGE_AT_END_REF_YR": age,
    "SEX_IDENT_CD": sex_map[sex],
    "BENE_RACE_CD": race_map[race],
    "YEAR": str(year),
    "total_paid_amt": total_paid_amt,
    "primary_dx_chronic_flag": chronic_map[chronic],
}
payload.update(body_system_payload)

# ---------------------------------------------------------
# PREDICTION
# ---------------------------------------------------------
API_URL = "https://avoidable-ed-api.onrender.com/predict"

if st.button("🔍 Predict Avoidable ED Visit"):
    try:
        response = requests.post(API_URL, json=payload)
        result = response.json()
        prob = result.get("probability")
        pred = result.get("prediction")

        if prob is None or pred is None:
            st.error("⚠️ API response missing required fields.")
        else:
            prob_pct = round(prob * 100, 2)
            st.subheader("📊 Prediction Result")
            st.metric(label="Probability of Avoidable ED Visit", value=f"{prob_pct}%")

            if prob >= 0.50:
                st.success("✅ Likely Avoidable ED Visit")
            else:
                st.info("ℹ️ Likely Non‑Avoidable ED Visit")

    except Exception as e:
        st.error("❌ Error contacting prediction service.")