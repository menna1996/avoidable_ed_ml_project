
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

model = joblib.load("final_avoidable_ed_model.joblib")

class EDVisitInput(BaseModel):
    AGE_AT_END_REF_YR: float
    SEX_IDENT_CD: float
    BENE_RACE_CD: float
    YEAR: float
    total_paid_amt: float
    primary_dx_chronic_flag: float
    bodysystem_respiratory: float
    bodysystem_circulatory: float
    bodysystem_infectious: float
    bodysystem_digestive: float
    bodysystem_mentalbehavioral: float
    bodysystem_musculoskeletal: float
    bodysystem_neoplasms: float
    bodysystem_nervoussystem: float
    bodysystem_injurypoisoning: float
    bodysystem_skin: float
    bodysystem_genitourinary: float
    bodysystem_endocrine: float
    bodysystem_bloodimmune: float
    bodysystem_symptoms: float
    bodysystem_externalcauses: float
    bodysystem_congenital: float
    bodysystem_perinatal: float
    bodysystem_pregnancy: float
    bodysystem_dental: float
    bodysystem_eye: float
    bodysystem_ear: float
    bodysystem_healthstatus: float
    bodysystem_unacceptable: float

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Avoidable ED Prediction API"}

@app.post("/predict")
def predict(data: EDVisitInput):
    try:
        df = pd.DataFrame([data.dict()])
        print("✅ Received input:", df.to_dict(orient="records")[0])

        df.columns = df.columns.str.strip()

        categorical_cols = ["SEX_IDENT_CD", "BENE_RACE_CD", "YEAR"]
        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].astype(str)

        df.fillna("missing", inplace=True)

        pred = model.predict(df)[0]
        prob = model.predict_proba(df)[0][1]

        print("✅ Prediction:", pred, "Probability:", prob)
        return {"prediction": int(pred), "probability": float(prob)}

    except Exception as e:
        print("❌ Prediction error:", str(e))
        raise HTTPException(status_code=500, detail="Prediction failed")
