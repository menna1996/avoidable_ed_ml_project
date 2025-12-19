# Experiments and tracking

All experiments are logged to **MLflow** and **Dagshub**.

## MLflow / DagsHub links

- **Dagshub project:**  
  https://dagshub.com/menna1996/avoidable_ed_ml_project

- **MLflow experiment:**  
  https://dagshub.com/menna1996/avoidable_ed_ml_project/experiments  

## Experiment matrix

| Exp # | Algorithm           | PCA | Tuning      | MLflow Run Name                       |
|------:|---------------------|-----|------------|----------------------------------------|
| 1     | Logistic Regression | No  | GridSearch | `Experiment_1_LogReg`                  |
| 2     | Logistic Regression | No  | GridSearch | `Exp2_LogReg`                          |
| 3     | Ridge Classifier    | No  | GridSearch | `Exp2_Ridge`                           |
| 4     | Random Forest       | No  | GridSearch | `Exp2_RandomForest`                    |
| 5     | XGBoost             | No  | GridSearch | `Exp2_XGB`                             |
| 6     | Logistic Regression | No  | None       | `Exp5_LogReg_NoPCA_NoTuning`          |
| 7     | Ridge Classifier    | No  | None       | `Exp6_Ridge_NoPCA_NoTuning`           |
| 8     | Random Forest       | No  | None       | `Exp7_RF_NoPCA_NoTuning`              |
| 9     | XGBoost             | No  | None       | `Exp8_XGB_NoPCA_NoTuning`             |
| 10    | Logistic Regression | Yes | None       | `Exp9_LogReg_PCA_NoTuning`            |
| 11    | Ridge Classifier    | Yes | None       | `Exp10_Ridge_PCA_NoTuning`            |
| 12    | Random Forest       | Yes | None       | `Exp11_RF_PCA_NoTuning`               |
| 13    | XGBoost             | Yes | None       | `Exp12_XGB_PCA_NoTuning`              |
| 14    | Logistic Regression | Yes | Optuna     | `Exp13_LogReg_PCA_Optuna`             |
| 15    | Ridge Classifier    | Yes | Optuna     | `Exp14_Ridge_PCA_Optuna`              |
| 16    | Random Forest       | Yes | Optuna     | `Exp15_RF_PCA_Optuna`                 |
| 17    | XGBoost             | Yes | Optuna     | `Exp16_XGB_PCA_Optuna`                |


## Key findings

- RandomForest (Exp2) achieved the highest test F1-score
 