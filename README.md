Avoidable ED Visit ML Project
Overview
This repository implements a machine learning pipeline to predict avoidable emergency department (ED) visits using the CMS Synthetic Medicare Enrollment and Fee-for-Service Claims dataset. The synthetic dataset represents enrollment and claims for 8,671 beneficiaries and includes diagnoses, procedures, revenue center codes, and payment information.

Data and Database
Dataset
- Source: CMS Synthetic Medicare Enrollment and Fee-for-Service Claims (Synthetic Medicare Claims PUFs)
- Population: 8,671 synthetic beneficiaries (ages 0–110)
- Scope: Enrollment records and claims (diagnoses, procedures, revenue center codes, payments)
Database
- Engine: PostgreSQL
- Connection: SQLAlchemy using environment variables (e.g., POSTGRES)
- Normalized tables: Diagnosis; Procedure Code; Claims; Revenue; Beneficiary

Visit Level Reconstruction
ER claim identification
- Revenue center codes: 0450–0459, 0981
- ED E/M CPT/HCPCS codes: 99281–99285
Joins performed
- Claims ↔ Beneficiary on BENE_ID and YEAR
- Claims ↔ Diagnosis on CLM_ID
- Diagnosis ↔ ICD10_ChronicIndicator on ICD10
- Diagnosis ↔ ED_Algorithm_ICD10 on ICD10
- Diagnosis ↔ CCSR_ICD10 on ICD10
Aggregation to visit level
- Partition by beneficiary, facility, year, and claim start date
- Visit start: MIN(CLM_FROM_DT)
- Visit end: MAX(CLM_THRU_DT)
- Payment aggregation: SUM(CLM_PMT_AMT)
- Claim count per visit: COUNT(DISTINCT CLM_ID)

Features and Modeling Dataset
Target
- Avoidable_ED_Visit (probability of an avoidable ED visit)
Visit-level dataset
- er_visits_modeling_dataset.parquet
Final modeling table columns
Numeric features
- AGE_AT_END_REF_YR
- total_paid_amt
- primary_dx_chronic_flag
- bodysystem_respiratory, bodysystem_circulatory, bodysystem_infectious, bodysystem_digestive, bodysystem_mentalbehavioral, bodysystem_musculoskeletal, bodysystem_neoplasms, bodysystem_nervoussystem, bodysystem_injurypoisoning, bodysystem_skin, bodysystem_genitourinary, bodysystem_endocrine, bodysystem_bloodimmune, bodysystem_symptoms, bodysystem_externalcauses, bodysystem_congenital, bodysystem_perinatal, bodysystem_pregnancy, bodysystem_dental, bodysystem_eye, bodysystem_ear, bodysystem_healthstatus, bodysystem_unacceptable
Categorical features
- SEX_IDENT_CD
- BENE_RACE_CD
- YEAR

Data Cleaning Preprocessing and EDA
Data cleaning
- Missing values are minimal due to SQL joins with COALESCE.
- primary_dx and all BodySystem_* indicators are complete.
- Cast SEX_IDENT_CD, BENE_RACE_CD, and YEAR to string for categorical encoding.
- Removed high-cardinality primary_dx from modeling features.
- Removed contaminated field STATE_CODE.
Preprocessing strategy
- AGE_AT_END_REF_YR → StandardScaler
- total_paid_amt → log1p transform then MinMaxScaler
- One-hot encode SEX_IDENT_CD, BENE_RACE_CD, YEAR
- Apply StandardScaler to binary body system flags
Exploratory Data Analysis highlights
- Class balance: Avoidable_ED_Visit is imbalanced (~9.5% positive) → use stratified train/test split.
- Demographics: ~56% male, ~44% female; majority White (code 1); age distribution skewed to older adults.
- Costs: total_paid_amt is highly right-skewed with extreme outliers (> $500k); log transform applied.
- Correlations: Moderate associations among body system indicators; no single numeric feature dominates predictive power.
- Outliers: Keep outliers after log transform.
- Artifacts produced: modeling_dataset_clean.parquet, histograms, boxplots, correlation heatmap, optional profiling report eda_profile.html (ydata-profiling).

Modeling and Experiments
Experiment framework
- Algorithms tested: Logistic Regression, Ridge Classifier, Random Forest, XGBoost
- Conditions tested:
- No PCA + No Tuning
- No PCA + With Tuning (GridSearchCV)
- PCA + No Tuning
- PCA + With Tuning (Optuna)
- Total experiments: 16 (all tracked in MLflow/Dagshub)
Tracking and metrics
- Experiment tracking: MLflow (Dagshub integration)
- Primary evaluation metric: F1 score
- All metrics and trained models logged to MLflow
Best model
- Best experiment: Random Forest (experiment 2)
- Test F1: 0.862

Deployment
Containerization and hosting
- Final model packaged with FastAPI in Docker
- API hosted on Render; Streamlit UI hosted separately
- Docker image tracked on Docker Hub
FastAPI
- Docs: https://avoidable-ed-api.onrender.com/docs#/default/predict_predict_post
- Prediction endpoint: POST /predict
Docker
- Docker Hub: https://hub.docker.com/repository/docker/menna1996/avoidable-ed-api/general
- Pull and run locally:
docker pull menna1996/avoidable-ed-api:latest
docker run -p 8000:8000 menna1996/avoidable-ed-api:latest


Streamlit app
- Live app: https://avoidableedmlproject-9rjakchaxjnarv3xq5dzhp.streamlit.app/
- Features: form inputs for demographics, year, costs, and body system indicators; real-time predictions via FastAPI /predict endpoint
