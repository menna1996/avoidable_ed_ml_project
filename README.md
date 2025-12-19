Avoidable ED Visit ML Project
Overview
This project develops a machine learning pipeline to predict avoidable emergency department (ED) visits using Medicare claims data. 
The Centers for Medicare and Medicaid Services (CMS) Synthetic Medicare Enrollment, Fee for-Service Claims, and Prescription Drug Event Data Public Use File (Synthetic Medicare Claims PUFs) is a synthetic dataset representing enrollment information and healthcare claims for 8,671 Medicare beneficiaries between the ages of 0 and 110.
1.	Load data
a.	Dataset: CMS Synthetic Medicare Enrollment and Fee for Service Claims data
-	Population: 8,671 synthetic Medicare beneficiaries (ages 0–110)
-	Scope: Enrollment and claims (diagnoses, procedures, revenue center codes, payments)
-	Database and normalization
-	Database: PostgreSQL
-	Normalized tables:
	Diagnosis
	Procedure Code
	Claims
	Revenue
	Beneficiary
-	Connection and environment
	Connection via SQLAlchemy with environment variables: POSTGRES
b.	Visit level reconstruction (SQL)
-	Identified ER claims using:
	Revenue center codes: 0450–0459, 0981
	ED E/M CPT/HCPCS codes: 99281–99285
-	Joined across tables:
	Claims ↔ Beneficiary on BENE_ID and YEAR
	Claims ↔ Diagnosis on CLM_ID
	Diagnosis ↔ ICD10_ChronicIndicator on ICD10
	Diagnosis ↔ ED_Algorithm_ICD10 on ICD10
	Diagnosis ↔ CCSR_ICD10 on ICD10
-	Rolled up to visit level:
	Partition by beneficiary, facility, year, and claim start date
	Visit start = MIN(CLM_FROM_DT), visit end = MAX(CLM_THRU_DT)
	Payment aggregation: SUM(CLM_PMT_AMT)
	Claim count per visit: COUNT(DISTINCT CLM_ID)
-	Body system indicators derived from CCSR Body System
-	Year extracted from visit start timestamp
-	Target variable:
	Probably of avoidable ED Visit
-	Visit level modeling dataset: 
	er_visits_modeling_dataset.parquet
-	Final modeling table columns
o	Numeric features:
	AGE_AT_END_REF_YR
	total_paid_amt
	primary_dx_chronic_flag
	bodysystem_respiratory
	bodysystem_circulatory
	bodysystem_infectious
	bodysystem_digestive
	bodysystem_mentalbehavioral
	bodysystem_musculoskeletal
	bodysystem_neoplasms
	bodysystem_nervoussystem
	bodysystem_injurypoisoning
	bodysystem_skin
	bodysystem_genitourinary
	bodysystem_endocrine
	bodysystem_bloodimmune
	bodysystem_symptoms
	bodysystem_externalcauses
	bodysystem_congenital
	bodysystem_perinatal
	bodysystem_pregnancy
	bodysystem_dental
	bodysystem_eye
	bodysystem_ear
	bodysystem_healthstatus
	bodysystem_unacceptable
o	Categorical features:
	SEX_IDENT_CD
	BENE_RACE_CD
	YEAR
o	Target:
	Avoidable_ED_Visit





2.	Clean, Preprocess, and Explore Data
a.	Data Cleaning
-	Missing values: Minimal due to SQL joins with COALESCE.
-	primary_dx and all BodySystem_* indicators are complete.
-	Categorical casting: Converted SEX_IDENT_CD, BENE_RACE_CD, and YEAR to string.
-	High cardinality removed: primary_dx.
-	Contaminated removed: STATE_CODE.
-	Preprocessing Strategy
-	Numeric features:
-	AGE_AT_END_REF_YR → StandardScaler
-	total_paid_amt → Log1p transform + MinMaxScaler
-	OneHotEncoder for SEX_IDENT_CD, BENE_RACE_CD, YEAR
-	Body system indicators:
-	StandardScaler applied to binary flags
b.	Exploratory Data Analysis
-	Class Balance
-	Target Avoidable_ED_Visit is imbalanced (~9.5% positive).
-	Stratified train/test split required to preserve proportions.
-	Demographics
o	SEX_IDENT_CD: ~56% male, ~44% female.
o	BENE_RACE_CD: Majority White (code 1), followed by Hispanic (5) and Black (2).
o	AGE_AT_END_REF_YR: Skewed toward older adults (expected for Medicare).
-	Numeric Features
o	total_paid_amt: Extremely right skewed with large outliers (> $500k).
o	Log transformation applied.
 
-	Correlation Analysis
o	moderate associations among body system indicators.
o	No single numeric feature strongly predicts avoidable ED visits alone.
 



-	Outliers
o	Boxplots confirm extreme outliers in total_paid_amt.
o	Decision: log transform only, keep outliers.
-	Visualizations included
o	Histograms and Boxplots
 
-	Automated profiling report (ydata-profiling)
-	Cleaned dataset: modeling_dataset_clean.parquet
-	EDA figures: histograms, boxplots, correlation heatmap
-	Profiling report: eda_profile.html (optional, generated with ydata-profiling)
o	Avoidable ED visits are rare (~9.5%).
o	Demographics skew older, majority White.
o	Costs are highly skewed with extreme outliers.
o	Body system indicators provide clinically meaningful predictors.
o	Stratified sampling required for modeling.

3.	Train Models
-	Baseline Algorithm: Logistic Regression (No PCA + With Tuning)
-	Logged in MLflow/Dagshub for reproducibility.
-	Experiment Framework
o	Algorithms tested: 
o	Logistic Regression, Ridge Classifier, Random Forest, XGBoost.
-	Conditions:
o	No PCA + No Tuning
o	No PCA + With Tuning (GridSearchCV)
o	PCA + No Tuning
o	PCA + With Tuning (Optuna)
-	Total: 16 experiments, all tracked in MLflow/Dagshub.
o	Dagshub MLflow Experiments
-	Experiment tracking: Dagshub MLflow Experiments
-	Evaluation Metrics
o	Primary metric: F1 score
-	Logging: All metrics and trained models logged to MLflow.
-	Best Model
o	Experiment: experiment 2 randomforest
o	Test F1: 0.862
 
4.	Deploying final model
a.	Deployment
-	Containerization: Final model + FastAPI packaged in Docker.
-	Hosting: API served on Render; Streamlit UI hosted separately.
-	Artifacts tracked: Image in Docker Hub; API docs exposed via OpenAPI (Swagger).
b.	FastAPI service
-	Docs: https://avoidable-ed-api.onrender.com/docs#/default/predict_predict_post
-	Prediction endpoint: POST /predict
c.	Docker image
-	Docker Hub: https://hub.docker.com/repository/docker/menna1996/avoidable-ed-api/general
-	Pull and run locally:
bash
docker pull menna1996/avoidable-ed-api:latest
docker run -p 8000:8000 menna1996/avoidable-ed-api:latest
d.	Streamlit app
-	Live app: https://avoidableedmlproject-9rjakchaxjnarv3xq5dzhp.streamlit.app/
-	Features:Form input: 
o	Demographics, year, costs, body system indicators.
o	Real time prediction: Calls FastAPI /predict endpoint.
