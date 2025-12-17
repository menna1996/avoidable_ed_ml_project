from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

# Load model
model = joblib.load("final_avoidable_ed_model.joblib")

# ✅ Pydantic schema with defaults
class EDVisitInput(BaseModel):
    # Core demographics
    AGE_AT_END_REF_YR: float = 65
    SEX_IDENT_CD: str = "1"
    BENE_RACE_CD: str = "1"
    YEAR: str = "2023"

    # Financial / chronic
    total_paid_amt: float = 0.0
    primary_dx_chronic_flag: float = 0

    # ✅ First half = 1
    bodysystem_respiratory: float = 1
    bodysystem_circulatory: float = 1
    bodysystem_infectious: float = 1
    bodysystem_digestive: float = 1
    bodysystem_mentalbehavioral: float = 1
    bodysystem_musculoskeletal: float = 1
    bodysystem_neoplasms: float = 1
    bodysystem_nervoussystem: float = 1
    bodysystem_injurypoisoning: float = 1
    bodysystem_skin: float = 1
    bodysystem_genitourinary: float = 1
    bodysystem_endocrine: float = 1

    # ✅ Second half = 0
    bodysystem_bloodimmune: float = 0
    bodysystem_symptoms: float = 0
    bodysystem_externalcauses: float = 0
    bodysystem_congenital: float = 0
    bodysystem_perinatal: float = 0
    bodysystem_pregnancy: float = 0
    bodysystem_dental: float = 0
    bodysystem_eye: float = 0
    bodysystem_ear: float = 0
    bodysystem_healthstatus: float = 0
    bodysystem_unacceptable: float = 0


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Avoidable ED Prediction API"}


@app.post("/predict")
def predict(data: EDVisitInput):
    try:
        # Convert input to DataFrame
        df = pd.DataFrame([data.dict()])
        print("✅ Received input:", df.to_dict(orient="records")[0])

        # ✅ Ensure categorical columns are strings
        categorical_cols = ["SEX_IDENT_CD", "BENE_RACE_CD", "YEAR"]
        for col in categorical_cols:
            df[col] = df[col].astype(str)

        # ✅ Rename body system columns to match training pipeline
        rename_map = {
            "bodysystem_respiratory": "BodySystem_Respiratory",
            "bodysystem_circulatory": "BodySystem_Circulatory",
            "bodysystem_infectious": "BodySystem_Infectious",
            "bodysystem_digestive": "BodySystem_Digestive",
            "bodysystem_mentalbehavioral": "BodySystem_MentalBehavioral",
            "bodysystem_musculoskeletal": "BodySystem_Musculoskeletal",
            "bodysystem_neoplasms": "BodySystem_Neoplasms",
            "bodysystem_nervoussystem": "BodySystem_NervousSystem",
            "bodysystem_injurypoisoning": "BodySystem_InjuryPoisoning",
            "bodysystem_skin": "BodySystem_Skin",
            "bodysystem_genitourinary": "BodySystem_Genitourinary",
            "bodysystem_endocrine": "BodySystem_Endocrine",
            "bodysystem_bloodimmune": "BodySystem_BloodImmune",
            "bodysystem_symptoms": "BodySystem_Symptoms",
            "bodysystem_externalcauses": "BodySystem_ExternalCauses",
            "bodysystem_congenital": "BodySystem_Congenital",
            "bodysystem_perinatal": "BodySystem_Perinatal",
            "bodysystem_pregnancy": "BodySystem_Pregnancy",
            "bodysystem_dental": "BodySystem_Dental",
            "bodysystem_eye": "BodySystem_Eye",
            "bodysystem_ear": "BodySystem_Ear",
            "bodysystem_healthstatus": "BodySystem_HealthStatus",
            "bodysystem_unacceptable": "BodySystem_Unacceptable",
        }

        df = df.rename(columns=rename_map)

        # ✅ Fill missing values safely
        df = df.fillna("missing")

        # ✅ Predict
        pred = model.predict(df)[0]
        prob = model.predict_proba(df)[0][1]

        print("✅ Prediction:", pred, "Probability:", prob)

        return {
            "prediction": int(pred),
            "probability": float(prob)
        }

    except Exception as e:
        print("❌ Prediction error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))