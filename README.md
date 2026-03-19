# Customer Churn Prediction & Retention Strategy

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Last Commit](https://img.shields.io/github/last-commit/logeshkannan19/Customer-Churn-Prediction-Retention-Strategy)

> **End-to-End Data Science Project**: Predicting customer churn in the telecom industry using machine learning, statistical analysis, and business intelligence to develop actionable retention strategies.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Results](#key-results)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Methodology](#methodology)
- [Machine Learning Models](#machine-learning-models)
- [Business Insights](#business-insights)
- [Retention Strategies](#retention-strategies)
- [Documentation](#documentation)
- [Contributing](#contributing)

---

## Overview

### Problem Statement

A telecom company faces a **27.39% customer churn rate**, resulting in **$2M+ annual revenue loss**. This project develops a comprehensive solution combining:

- **Exploratory Data Analysis** to understand churn patterns
- **Machine Learning Models** to predict at-risk customers
- **SQL Analytics** for segment analysis
- **Business Intelligence** dashboards for monitoring
- **Actionable Retention Strategies** with ROI projections

### Dataset

| Attribute | Description |
|-----------|-------------|
| Records | 7,500 customers |
| Features | 19 attributes |
| Target | Churn (binary: 0=Retained, 1=Churned) |
| Churn Rate | 27.39% |

---

## Key Results

| Metric | Value |
|--------|-------|
| **Churn Rate** | 27.39% |
| **Annual Revenue at Risk** | $2,003,017 |
| **Best ML Model** | Random Forest |
| **Model F1-Score** | 0.81 |
| **Model ROC-AUC** | 0.90 |
| **Retention ROI** | 200%+ |

### Top Churn Risk Factors

| Factor | Impact | Churn Rate |
|--------|--------|------------|
| New Customers (<12 months) | 2.1x higher | 38.35% |
| Month-to-Month Contracts | 1.8x higher | 32.52% |
| Electronic Check Payment | 1.3x higher | 31.85% |
| High Charges (>$80/mo) | 1.9x higher | 33.70% |

---

## Project Structure

```
Customer-Churn-Prediction-Retention-Strategy/
├── src/
│   ├── __init__.py
│   ├── data_generation.py          # Synthetic data generator
│   ├── eda_analysis.py             # Exploratory Data Analysis
│   ├── feature_engineering.py      # Feature engineering (40+ features)
│   ├── sql_queries.py              # SQL analytics module
│   ├── ml_models.py                # ML model training & evaluation
│   └── insights_recommendations.py # Business insights generator
│
├── data/
│   ├── customer_data.csv           # Raw customer dataset
│   └── customer_data_processed.csv # Processed data
│
├── results/
│   ├── visualizations/             # 11 EDA visualizations
│   ├── models/                     # Trained ML models
│   ├── model_report.txt            # Model performance report
│   └── business_insights_report.txt # Full business analysis
│
├── dashboard/
│   └── powerbi_dashboard_spec.md   # Power BI dashboard design
│
├── sql/
│   └── churn_queries.sql           # SQL query reference
│
├── tests/                          # Unit tests
├── docs/                           # Documentation
│
├── main.py                         # Main execution script
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── LICENSE                         # MIT License
├── CONTRIBUTING.md                 # Contribution guidelines
├── .gitignore                      # Git ignore file
└── pyproject.toml                  # Project configuration
```

---

## Quick Start

### Prerequisites

- Python 3.8+
- pip or conda

### Installation

```bash
# Clone the repository
git clone https://github.com/logeshkannan19/Customer-Churn-Prediction-Retention-Strategy.git
cd Customer-Churn-Prediction-Retention-Strategy

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Complete Pipeline

```bash
# Run all modules
python main.py

# Or run individual modules
python -c "from src.data_generation import main; main()"
python -c "from src.eda_analysis import ChurnEDA; import pandas as pd; eda = ChurnEDA(pd.read_csv('data/customer_data.csv')); eda.generate_eda_report()"
```

### Output Files

After running the pipeline:

```
results/
├── visualizations/
│   ├── 01_churn_distribution.png
│   ├── 02_churn_by_contract.png
│   ├── 03_churn_by_tenure.png
│   ├── 04_churn_by_payment.png
│   ├── 05_charges_distribution.png
│   ├── 06_correlation_heatmap.png
│   ├── 07_tenure_charges.png
│   ├── 08_service_analysis.png
│   ├── 09_risk_analysis.png
│   ├── 10_segment_analysis.png
│   └── 11_revenue_impact.png
├── model_report.txt
└── business_insights_report.txt
```

---

## Methodology

### 1. Data Generation

Synthetic dataset with realistic churn patterns based on industry research:

- **Tenure-weighted churn**: New customers have higher churn probability
- **Contract type patterns**: Month-to-month contracts show highest churn
- **Service engagement**: More services = lower churn
- **Payment method correlation**: Electronic check users churn more

### 2. Exploratory Data Analysis

Comprehensive EDA including:

- Summary statistics and distributions
- Churn rate analysis by segment
- Correlation analysis
- Statistical significance tests (t-tests, chi-square)
- 11 professional visualizations

### 3. Feature Engineering

Created 40+ engineered features:

| Category | Features |
|----------|----------|
| Tenure | `tenure_group`, `is_new_customer`, `is_long_tenure` |
| Charges | `charge_bucket`, `is_high_value`, `avg_monthly_spend` |
| Contract | `contract_risk_score`, `is_monthly_contract` |
| Services | `total_services`, `has_core_services`, `has_streaming` |
| Payment | `is_electronic_check`, `is_auto_pay` |
| Interactions | `high_risk_new`, `risky_contract_payment` |
| Risk | `composite_risk_score`, `risk_tier_calculated` |

### 4. SQL Analytics

12 analytical queries for:

- Churn rate by segment
- High-risk customer identification
- Revenue loss calculation
- Tenure-based analysis
- Service impact analysis
- Retention opportunities

---

## Machine Learning Models

### Models Compared

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|-------|----------|-----------|--------|----------|---------|
| Logistic Regression | 0.78 | 0.72 | 0.75 | 0.73 | 0.85 |
| Decision Tree | 0.80 | 0.76 | 0.78 | 0.77 | 0.84 |
| **Random Forest** | **0.84** | **0.80** | **0.82** | **0.81** | **0.90** |
| Gradient Boosting | 0.83 | 0.78 | 0.81 | 0.79 | 0.89 |

### Best Model: Random Forest

**Why Random Forest?**
- Best F1-Score (balances precision and recall)
- Highest ROC-AUC (strong discriminative ability)
- Handles imbalanced data well
- Provides feature importance

### Top 10 Feature Importance

| Rank | Feature | Importance |
|------|---------|------------|
| 1 | tenure_months | 0.156 |
| 2 | satisfaction_score | 0.142 |
| 3 | monthly_charges | 0.098 |
| 4 | total_charges | 0.087 |
| 5 | contract_type_encoded | 0.076 |
| 6 | is_electronic_check | 0.054 |
| 7 | total_services | 0.048 |
| 8 | is_fiber | 0.035 |
| 9 | payment_risk_score | 0.031 |
| 10 | has_core_services | 0.028 |

---

## Business Insights

### Quantified Findings

#### 1. Tenure Impact [HIGH]
> New customers (<12 months) churn at **38.35%** vs **17.60%** for loyal customers (48+ months)
- **2.1x higher churn risk** for new customers

#### 2. Contract Type Impact [CRITICAL]
> Month-to-month customers churn at **32.52%** vs **18.45%** for two-year contracts
- **1.8x higher churn** without contract commitment

#### 3. Payment Method Impact [HIGH]
> Electronic check users churn at **31.85%** vs **24.11%** for auto-pay customers
- **$166,918 monthly revenue at risk** from payment method

#### 4. Price Sensitivity [MEDIUM]
> High-charge customers ($80+) churn at **33.70%** vs **17.90%** for budget customers
- **1.9x more churn** at higher price points

### Segment Analysis

| Segment | Customers | Churn Rate | Avg Revenue | Revenue at Risk |
|---------|-----------|------------|-------------|-----------------|
| New | 1,875 | 38.35% | $77.60 | $59,421 |
| Developing | 2,574 | 27.20% | $75.71 | $56,173 |
| Established | 1,716 | 23.31% | $75.57 | $32,634 |
| Loyal | 1,335 | 17.60% | $73.67 | $18,690 |

---

## Retention Strategies

### Priority 1: Contract Upgrade Campaign [CRITICAL]

| Aspect | Details |
|--------|---------|
| Target | Month-to-Month customers (4,114) |
| Current Churn | 32.52% |
| Actions | Discounted annual plans, free premium services |
| Expected Impact | 25-30% churn reduction |
| ROI | 200%+ |

### Priority 2: Auto-Pay Migration [HIGH]

| Aspect | Details |
|--------|---------|
| Target | Electronic check users (2,653) |
| Current Churn | 31.85% |
| Actions | $5/mo discount, simplified enrollment |
| Expected Impact | 20-25% churn reduction |
| ROI | 236% |

### Priority 3: Early Engagement Program [HIGH]

| Aspect | Details |
|--------|---------|
| Target | New customers (1,875) |
| Current Churn | 38.35% |
| Actions | Welcome series, dedicated support, price lock |
| Expected Impact | 15-20% churn reduction |
| ROI | 150% |

### Priority 4: Service Bundle Upsell [MEDIUM]

| Aspect | Details |
|--------|---------|
| Target | Customers with <2 services |
| Current Churn | ~28% |
| Actions | Essential bundle discount, free trials |
| Expected Impact | 18-22% churn reduction |
| ROI | 164% |

### ROI Projection

| Scenario | Customers Saved | Annual Savings | Investment | ROI |
|----------|-----------------|----------------|-------------|-----|
| 20% reduction | 411 | $400,603 | $200,302 | 100% |
| 30% reduction | 616 | $600,905 | $200,302 | 200% |
| 40% reduction | 822 | $801,207 | $200,302 | 300% |

---

## Documentation

### Power BI Dashboard

Comprehensive dashboard design with **10+ KPIs**:

| KPI | Description |
|-----|-------------|
| Total Customers | 7,500 |
| Churn Rate | 27.39% |
| Retention Rate | 72.61% |
| Monthly Revenue | $450,234 |
| Annual Revenue at Risk | $1.43M |
| At-Risk Customers | 1,988 |
| Avg Customer Lifetime | 28.4 months |
| Avg CSAT Score | 7.2/10 |
| High-Risk Segments | 3 |
| Critical Actions | 147 |

See [`dashboard/powerbi_dashboard_spec.md`](dashboard/powerbi_dashboard_spec.md) for full specification.

### SQL Queries

Reference implementation in [`sql/churn_queries.sql`](sql/churn_queries.sql) including:

- Churn rate by segment
- High-risk customer identification
- Revenue loss calculation
- Tenure bucket analysis
- Service impact analysis

---

## Technologies Used

| Category | Tools |
|----------|-------|
| **Data Analysis** | Python, Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn |
| **Machine Learning** | Scikit-learn, GradientBoosting |
| **Database** | SQLite |
| **BI Tools** | Power BI |
| **Statistics** | SciPy, StatsModels |

---

## Contributing

Contributions are welcome! Please see [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## License

This project is licensed under the MIT License - see [`LICENSE`](LICENSE) for details.

---

## Author

**Customer Churn Prediction & Retention Strategy (2025)**

Built with Python | Powered by Data Science

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue.svg)](https://linkedin.com)
[![Email](https://img.shields.io/badge/Email-Contact-green.svg)](mailto:contact@example.com)

---

*If you found this project useful, please give it a ⭐*
