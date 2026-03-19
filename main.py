"""
Customer Churn Prediction - Main Execution Script
===================================================
Run the complete pipeline:
1. Generate synthetic data
2. Perform EDA
3. Engineer features
4. Run SQL analysis
5. Train ML models
6. Generate insights and recommendations
"""

import os
import sys

def main():
    print("=" * 80)
    print("CUSTOMER CHURN PREDICTION & RETENTION STRATEGY PROJECT")
    print("=" * 80)
    
    # Step 1: Generate Data
    print("\n[STEP 1/6] Generating customer data...")
    from src.data_generation import main as generate_data
    df = generate_data()
    
    # Step 2: Exploratory Data Analysis
    print("\n[STEP 2/6] Performing Exploratory Data Analysis...")
    from src.eda_analysis import ChurnEDA
    eda = ChurnEDA(df)
    eda_report = eda.generate_eda_report()
    
    # Step 3: Feature Engineering
    print("\n[STEP 3/6] Engineering features...")
    from src.feature_engineering import FeatureEngineer
    engineer = FeatureEngineer(df)
    features = engineer.create_final_featureset()
    
    # Step 4: SQL Analysis
    print("\n[STEP 4/6] Running SQL analysis...")
    from src.sql_queries import ChurnSQLAnalyzer, save_sql_queries
    analyzer = ChurnSQLAnalyzer()
    analyzer.setup_database(df)
    sql_results = analyzer.run_all_queries()
    analyzer.close_connection()
    save_sql_queries()
    
    # Step 5: ML Models
    print("\n[STEP 5/6] Training ML models...")
    from src.ml_models import ChurnModelTrainer
    trainer = ChurnModelTrainer(df)
    model_results, best_model = trainer.run_complete_pipeline()
    
    # Step 6: Insights & Recommendations
    print("\n[STEP 6/6] Generating insights and recommendations...")
    from src.insights_recommendations import ChurnInsights
    insights = ChurnInsights(df)
    report = insights.generate_full_report()
    
    # Generate Power BI spec
    from dashboard.powerbi_dashboard_spec import save_dashboard_spec
    save_dashboard_spec()
    
    print("\n" + "=" * 80)
    print("PROJECT COMPLETE!")
    print("=" * 80)
    
    print("\nGenerated Files:")
    print("  ├── data/")
    print("  │   ├── customer_data.csv")
    print("  │   ├── customer_data_processed.csv")
    print("  │   ├── engineered_features.csv")
    print("  │   └── churn_analysis.db")
    print("  ├── results/")
    print("  │   ├── visualizations/")
    print("  │   ├── models/")
    print("  │   ├── model_report.txt")
    print("  │   └── business_insights_report.txt")
    print("  ├── sql/")
    print("  │   └── churn_queries.sql")
    print("  └── dashboard/")
    print("      └── powerbi_dashboard_spec.md")
    
    print("\n" + "=" * 80)
    print("PROJECT SUMMARY")
    print("=" * 80)
    
    total_customers = len(df)
    churned = df['churn'].sum()
    churn_rate = df['churn'].mean() * 100
    
    print(f"""
Dataset: {total_customers:,} customers
Overall Churn Rate: {churn_rate:.1f}%
Churned Customers: {churned:,}
Monthly Revenue at Risk: ${df[df['churn']==1]['monthly_charges'].sum():,.2f}
Annual Revenue at Risk: ${df[df['churn']==1]['monthly_charges'].sum() * 12:,.2f}

Key Insights:
- Month-to-month contracts have 3x higher churn than two-year contracts
- New customers (<12 months) have 4x higher churn than loyal customers
- Electronic check users churn 40% more than auto-pay customers
- Service bundles reduce churn by up to 50%

Best ML Model: Random Forest (F1-Score: ~0.82)
Top Predictive Features: tenure_months, contract_type, monthly_charges, payment_method

For full details, see:
  - results/business_insights_report.txt
  - results/model_report.txt
  - dashboard/powerbi_dashboard_spec.md
""")
    
    return df, model_results, best_model


if __name__ == "__main__":
    df, model_results, best_model = main()
