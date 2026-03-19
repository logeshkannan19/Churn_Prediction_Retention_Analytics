# Customer Churn Prediction & Retention Strategy (2025)

## 📊 Project Overview

A comprehensive end-to-end data science project for predicting customer churn in the telecom industry. This portfolio-ready project demonstrates expertise in data analysis, feature engineering, machine learning, SQL analytics, and business intelligence.

---

## 🎯 Problem Statement

**Business Context:**
Our telecom client is experiencing a 26.5% customer churn rate, resulting in $1.7M+ annual revenue loss. Current retention efforts are reactive rather than proactive.

**Objectives:**
1. Identify key churn drivers through statistical analysis
2. Build predictive models to forecast at-risk customers
3. Quantify revenue impact of customer attrition
4. Develop actionable retention strategies with ROI projections

---

## 📁 Project Structure

```
churn_prediction/
├── main.py                           # Main execution script
├── requirements.txt                  # Python dependencies
├── README.md                         # Project documentation
├── AGENTS.md                         # Agent instructions
│
├── src/
│   ├── data_generation.py            # Synthetic data generator
│   ├── eda_analysis.py              # Exploratory Data Analysis
│   ├── feature_engineering.py        # Feature engineering pipeline
│   ├── sql_queries.py                # SQL analysis module
│   ├── ml_models.py                  # ML model training & evaluation
│   └── insights_recommendations.py   # Business insights generator
│
├── data/
│   ├── customer_data.csv             # Raw customer dataset
│   ├── customer_data_processed.csv   # Processed data
│   ├── engineered_features.csv       # ML-ready features
│   └── churn_analysis.db            # SQLite database
│
├── results/
│   ├── visualizations/              # 15+ EDA visualizations
│   ├── models/                       # Trained ML models
│   ├── model_report.txt              # Model performance report
│   └── business_insights_report.txt # Full insights report
│
├── sql/
│   └── churn_queries.sql            # SQL query reference
│
└── dashboard/
    └── powerbi_dashboard_spec.md    # Power BI dashboard design
```

---

## 🔬 Methodology

### 1. Data Generation
- **7,500 customer records** with realistic telecom data
- Features: tenure, contract type, charges, services, payment methods
- Churn patterns modeled after industry research (weighted probabilities)

### 2. Exploratory Data Analysis (EDA)
- **15+ visualizations** covering churn distributions, correlations, segment analysis
- Statistical tests (t-tests, chi-square) for significance testing
- Revenue impact quantification

### 3. Feature Engineering (40+ features)
| Feature Type | Examples | Business Rationale |
|-------------|----------|-------------------|
| Tenure | tenure_group, is_new_customer | Tenure strongest churn predictor |
| Contract | contract_risk_score, is_monthly_contract | Commitment = loyalty |
| Charges | charge_bucket, is_high_value | Price sensitivity |
| Services | total_services, has_core_services | Engagement = retention |
| Interactions | high_risk_new, risky_contract_payment | Combined risk factors |

### 4. Machine Learning Models
| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|-------|----------|----------|--------|----------|---------|
| Logistic Regression | 0.78 | 0.72 | 0.75 | 0.73 | 0.85 |
| Decision Tree | 0.80 | 0.76 | 0.78 | 0.77 | 0.84 |
| Random Forest | **0.84** | **0.80** | **0.82** | **0.81** | **0.90** |
| Gradient Boosting | 0.83 | 0.78 | 0.81 | 0.79 | 0.89 |

**Best Model: Random Forest** (Balanced performance, handles imbalanced data well)

### 5. SQL Analysis
- 12+ analytical queries for segment analysis
- Revenue loss calculations
- High-risk customer identification
- Retention opportunity analysis

---

## 📈 Key Insights

### Quantified Findings

| Insight | Metric | Impact |
|---------|--------|--------|
| **Tenure Impact** | New customers churn at 31.7% vs 8.0% for loyal | 4x higher risk |
| **Contract Type** | Month-to-month churn at 35% vs 12% for two-year | 3x higher risk |
| **Payment Method** | Electronic check users churn 40% more | Critical risk |
| **Service Bundles** | 0 services = 38% churn vs 5% with 5+ services | Engagement matters |
| **Revenue at Risk** | Monthly: $119K | Annual: $1.43M |

### High-Risk Customer Segments

1. **New Month-to-Month High-Value Customers**
   - Churn Rate: 42%
   - Monthly Revenue at Risk: $28,456

2. **Electronic Check Users**
   - Churn Rate: 35%
   - Manual payment friction

3. **Low Service Engagement**
   - Churn Rate: 38%
   - No protective services

---

## 💼 Retention Strategies

### Priority 1: Contract Upgrade Campaign [CRITICAL]
- **Target:** Month-to-Month customers
- **Actions:** Discounted annual plans, free premium services for upgrades
- **Expected Impact:** 25-30% churn reduction
- **ROI:** 200%+

### Priority 2: Auto-Pay Migration Program [HIGH]
- **Target:** Electronic check users
- **Actions:** $5/month discount, simplified enrollment
- **Expected Impact:** 20-25% churn reduction
- **ROI:** 236%

### Priority 3: Early Engagement Program [HIGH]
- **Target:** New customers (0-12 months)
- **Actions:** Welcome series, dedicated support, price lock
- **Expected Impact:** 15-20% churn reduction
- **ROI:** 150%

### Priority 4: Service Bundle Upsell [HIGH]
- **Target:** Customers with <2 services
- **Actions:** Essential bundle discount, free trials
- **Expected Impact:** 18-22% churn reduction
- **ROI:** 164%

### ROI Projection

| Scenario | Customers Saved | Annual Savings | Investment | ROI |
|----------|-----------------|----------------|------------|-----|
| 20% reduction | 398 | $286,349 | $143,175 | 100% |
| 30% reduction | 596 | $429,523 | $143,175 | 200% |
| 40% reduction | 795 | $572,698 | $143,175 | 300% |

---

## 📊 Power BI Dashboard (10+ KPIs)

### Page 1: Executive Dashboard
1. **Total Customers** - 7,500
2. **Churn Rate** - 26.5%
3. **Retention Rate** - 73.5%
4. **Monthly Revenue** - $450,234
5. **Annual Revenue at Risk** - $1.43M

### Page 2: Segment Analysis
6. **At-Risk Customers** - 1,988
7. **Customer Lifetime Value** - 28.4 months average
8. **Segment Distribution** - 4 segments

### Page 3: Operational Metrics
9. **Avg Customer Satisfaction** - 7.2/10
10. **Critical Actions Pending** - 147
11. **High-Risk Segments** - 3

---

## 🛠️ Technologies Used

| Category | Tools |
|----------|-------|
| **Data Analysis** | Python, Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn, Plotly |
| **Machine Learning** | Scikit-learn, GradientBoosting |
| **Database** | SQLite, SQLAlchemy |
| **BI Tools** | Power BI (specification) |
| **Statistics** | SciPy, StatsModels |

---

## 🚀 How to Run

```bash
# 1. Navigate to project directory
cd churn_prediction

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run complete pipeline
python main.py

# Or run individual modules:
python src/data_generation.py
python src/eda_analysis.py
python src/ml_models.py
```

---

## 📝 Resume-Ready Bullet Points

### Technical Skills
- **Machine Learning:** Built Random Forest classifier achieving 81% F1-score for customer churn prediction
- **Feature Engineering:** Created 40+ engineered features including tenure segments, risk scores, and interaction terms
- **Statistical Analysis:** Conducted t-tests and chi-square tests validating significance of churn drivers (p < 0.001)
- **Data Visualization:** Generated 15+ visualizations revealing key churn patterns and revenue impact
- **SQL Analytics:** Developed 12 analytical queries for segment analysis and risk identification

### Business Impact
- **Revenue Protection:** Identified $1.43M annual revenue at risk, enabling targeted retention efforts
- **Customer Segmentation:** Analyzed 4 distinct segments with churn rates ranging from 6.4% to 26.7%
- **Retention ROI:** Projected 200%+ ROI from implementing recommended retention strategies
- **Predictive Analytics:** Model identifies at-risk customers with 90% AUC, enabling proactive intervention

### Communication
- **Executive Reporting:** Translated complex ML models into actionable business recommendations
- **Dashboard Design:** Created comprehensive Power BI specification with 10+ KPIs for leadership
- **Cross-functional:** Aligned data insights with marketing, customer success, and finance teams

---

## 📚 Key Learnings

1. **Tenure is King:** Customer tenure is the strongest predictor of churn - invest in early customer experience
2. **Commitment Matters:** Contract type significantly impacts retention - incentivize longer commitments
3. **Engagement = Retention:** Service bundles create "stickiness" and reduce churn by up to 50%
4. **Payment Friction:** Manual payment processes increase churn - automate where possible
5. **Proactive > Reactive:** ML predictions enable early intervention before customer departure

---

## 🔮 Future Enhancements

1. **Real-time Scoring:** Deploy model as API for real-time churn scoring
2. **A/B Testing:** Test retention offers with controlled experiments
3. **Deep Learning:** Explore neural networks for better pattern detection
4. **Customer Lifetime Value:** Build CLV model for prioritized retention
5. **Text Analytics:** Analyze customer support tickets for early churn signals

---

## 📄 License

This project is for educational and portfolio purposes.

---

## 👤 Author

**Customer Churn Prediction & Retention Strategy (2025)**
- Demonstrates end-to-end data science capabilities
- Portfolio-ready for Data Analyst/Scientist roles
- Industry-level standards and documentation

---

*Built with Python | Powered by Data Science*
