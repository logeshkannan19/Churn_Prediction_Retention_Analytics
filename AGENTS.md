# Agent Instructions for Customer Churn Prediction Project

## Project Context
This is a comprehensive data science project for predicting customer churn in the telecom industry. The project includes data generation, EDA, feature engineering, SQL analysis, ML modeling, and business recommendations.

## Directory Structure
```
churn_prediction/
├── main.py                           # Main execution script
├── requirements.txt                  # Dependencies
├── README.md                         # Project documentation
├── AGENTS.md                         # This file
├── src/
│   ├── __init__.py
│   ├── data_generation.py            # Data generation
│   ├── eda_analysis.py               # EDA module
│   ├── feature_engineering.py        # Feature engineering
│   ├── sql_queries.py                # SQL analysis
│   ├── ml_models.py                  # ML models
│   └── insights_recommendations.py   # Business insights
├── data/                            # Data directory
├── results/                         # Results directory
├── sql/                            # SQL directory
└── dashboard/                       # Dashboard specs
```

## Key Components

### 1. Data Generation (src/data_generation.py)
- Generates 7,500 synthetic customer records
- Features: customer_id, tenure_months, contract_type, internet_service, payment_method, monthly_charges, total_charges, services, churn, satisfaction_score, customer_segment, risk_tier
- Churn patterns based on industry research

### 2. EDA (src/eda_analysis.py)
- Class: `ChurnEDA(df, target_col='churn')`
- Key methods:
  - `generate_summary_statistics()`
  - `analyze_churn_by_segment()`
  - `analyze_correlations()`
  - `statistical_tests()`
  - `create_visualizations()`
  - `generate_eda_report()`

### 3. Feature Engineering (src/feature_engineering.py)
- Class: `FeatureEngineer(df)`
- Creates 40+ features including:
  - Tenure segments
  - Charge buckets
  - Service aggregations
  - Risk scores
  - Interaction features

### 4. ML Models (src/ml_models.py)
- Class: `ChurnModelTrainer(df, target_col='churn')`
- Models: Logistic Regression, Decision Tree, Random Forest, Gradient Boosting
- Evaluation: Accuracy, Precision, Recall, F1-Score, ROC-AUC
- Key methods:
  - `prepare_features()`
  - `split_data()`
  - `train_*` methods for each model
  - `compare_models()`
  - `hyperparameter_tuning()`
  - `get_feature_importance()`
  - `plot_*` methods for visualizations

### 5. SQL Queries (src/sql_queries.py)
- Class: `ChurnSQLAnalyzer(db_path)`
- Key methods:
  - `setup_database(df)`
  - `get_churn_rate_by_segment()`
  - `get_high_risk_customers()`
  - `get_revenue_loss_analysis()`
  - `run_all_queries()`

### 6. Insights (src/insights_recommendations.py)
- Class: `ChurnInsights(df)`
- Key methods:
  - `calculate_key_metrics()`
  - `quantify_insights()`
  - `generate_retention_strategies()`
  - `calculate_roi_projections()`
  - `generate_full_report()`

## Running the Project

### Full Pipeline
```bash
cd churn_prediction
python main.py
```

### Individual Modules
```bash
python -c "from src.data_generation import main; main()"
python -c "from src.eda_analysis import ChurnEDA; import pandas as pd; eda = ChurnEDA(pd.read_csv('data/customer_data.csv')); eda.generate_eda_report()"
```

## Output Files
- `data/customer_data.csv` - Raw dataset
- `data/engineered_features.csv` - ML-ready features
- `results/visualizations/*.png` - 15+ visualizations
- `results/model_report.txt` - ML model results
- `results/business_insights_report.txt` - Full business analysis
- `sql/churn_queries.sql` - SQL query reference
- `dashboard/powerbi_dashboard_spec.md` - Dashboard design

## Important Variables
- `target_col`: 'churn' (binary: 0=retained, 1=churned)
- `test_size`: 0.2 (80/20 train-test split)
- `random_state`: 42 (for reproducibility)

## Notes for Agents
1. All modules are designed to run independently after data generation
2. Visualizations are saved to `results/visualizations/`
3. Models can be loaded from `results/models/`
4. SQL database is created at `data/churn_analysis.db`
5. The project demonstrates complete data science workflow from data to deployment-ready insights
