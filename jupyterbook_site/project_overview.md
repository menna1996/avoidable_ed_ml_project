# Project overview

Avoidable ED visits contribute to unnecessary cost and strain on healthcare systems.  
Goal: **predict which patients are at risk of an avoidable ED visit** using claims data.

## Data

- Target: `Avoidable_ED_Visit` (binary)
- Inputs:
  - Demographics (age, sex, race, year)
  - Cost signals (total paid amounts)
  - Clinical Body system indicators

Stratified 80/20 train-test split to preserve class balance.

## Modeling approach

- Preprocessing with `ColumnTransformer`:
  - StandardScaler (continuous)
  - Log1p + MinMaxScaler (cost)
  - OneHotEncoder (categorical)
  - StandardScaler (body systems)
- PCA applied **after** preprocessing for PCA experiments:
  - `PCA(n_components=0.95)`
- Four algorithms:
  - Logistic Regression
  - Ridge Classifier
  - Random Forest
  - XGBoost

## Experiment design

16 experiments = 4 algorithms × 4 conditions:

1. **No PCA + No Tuning**
2. **No PCA + With Tuning (GridSearchCV)**
3. **PCA + No Tuning**
4. **PCA + With Tuning (Optuna)**

All experiments tracked with MLflow / DagsHub.
