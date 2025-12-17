import streamlit as st
import requests
import pandas as pd


# ---------------------------------------------------------
# UI SETUP
# ---------------------------------------------------------
st.title("Avoidable ED Visit Prediction")
st.write("Predict whether an emergency department visit is avoidable.")

API_URL = "https://avoidable-ed-api.onrender.com/predict"

# ---------------------------------------------------------
# MAPPINGS
# ---------------------------------------------------------

# Sex mapping
sex_map = {
    "Male": "1",
    "Female": "2"
}

# Race mapping (your exact mapping)
race_display_to_code = {
    "Unknown": "0",
    "White": "1",
    "Black": "2",
    "Other": "3",
    "Asian": "4",
    "Hispanic": "5",
    "North American Native": "6"
}

# Chronic condition mapping
chronic_map = {
    "No": 0,
    "Yes": 1
}

# Body system display → model column mapping (lowercase)
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

# ---------------------------------------------------------
# USER INPUTS
# ---------------------------------------------------------

st.subheader("Patient Information")

age = st.slider("Age", min_value=0, max_value=120, value=65)

sex = st.selectbox("Sex", ["Male", "Female"])

race = st.selectbox(
    "Race",
    ["White", "Black", "Asian", "Hispanic", "Other", "North American Native", "Unknown"]
)

year = st.number_input("Year", min_value=2020, max_value=2100, value=2023)

total_paid_amt = st.number_input("Total Paid Amount ($)", min_value=0.0, value=0.0)

chronic = st.selectbox("Chronic Condition", ["No", "Yes"])

st.subheader("Clinical Classification (Body System)")
selected_body_system = st.selectbox(
    "Primary Body System",
    list(body_system_map.keys())
)

# ---------------------------------------------------------
# BUILD PAYLOAD
# ---------------------------------------------------------

# Start with all body systems = 0
body_system_payload = {v: 0 for v in body_system_map.values()}

# Set selected one to 1
body_system_payload[body_system_map[selected_body_system]] = 1

payload = {
    "AGE_AT_END_REF_YR": age,
    "SEX_IDENT_CD": sex_map[sex],
    "BENE_RACE_CD": race_display_to_code[race],
    "YEAR": str(year),
    "total_paid_amt": total_paid_amt,
    "primary_dx_chronic_flag": chronic_map[chronic],
}

# Add body system flags
payload.update(body_system_payload)

# ---------------------------------------------------------
# PREDICT BUTTON
# ---------------------------------------------------------
if st.button("Predict Avoidable ED Visit"):
    try:
        response = requests.post(API_URL, json=payload)

        # Debug info so the app NEVER goes blank
        st.write("Status code:", response.status_code)
        st.write("Raw response:", response.text)

        # Try to parse JSON safely
        try:
            result = response.json()
        except:
            st.error("API did not return valid JSON.")
            st.stop()

        prob = result.get("probability")
        pred = result.get("prediction")

        if prob is None or pred is None:
            st.error("API response missing 'probability' or 'prediction'. Check FastAPI output.")
            st.stop()

        prob_pct = round(prob * 100, 2)

        st.subheader("Prediction Result")
        st.write(f"**Probability:** {prob_pct}%")

        if prob >= 0.50:
            st.success("✅ Likely Avoidable ED Visit")
        else:
            st.info("ℹ️ Likely Non‑Avoidable ED Visit")

    except Exception as e:
        st.error(f"Error contacting API: {e}")