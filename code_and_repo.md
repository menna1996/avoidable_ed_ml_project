## Repository structure

```text
.
├── .devcontainer/
├── __pycache__/
├── mlruns/                      # MLflow runs
├── app/                         # Streamlit app (deployed)
├── custom_transformers/         # Reusable transformers
├── mlflow/                      # MLflow utilities
├── 0_create_database.ipynb
├── 1_sql_join_to_pandas.ipynb
├── 2_explore_data.ipynb
├── 3_experiments.ipynb
├── 4_final_model.ipynb
├── .env
├── main.py                      # FastAPI entrypoint (local)
├── er_visits_modeling_dataset.parquet
├── modeling_dataset_clean.parquet
├── final_avoidable_ed_model.joblib
├── Dockerfile
├── requirements.txt
├── _config.yml                  # JupyterBook config
├── _toc.yml
├── index.md
├── project_overview.md
├── experiments.md
└── code_and_repo.md
