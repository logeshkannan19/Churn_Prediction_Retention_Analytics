"""
SQL Integration Module
=======================
SQL queries for churn analysis, including:
- Churn rate by segment
- High-risk customer identification
- Revenue loss calculation
- Customer lifetime analysis
"""

import sqlite3
import pandas as pd


class ChurnSQLAnalyzer:
    """
    SQL-based analysis for churn prediction.
    Demonstrates SQL proficiency for business analytics.
    """
    
    def __init__(self, db_path='data/churn_analysis.db'):
        self.db_path = db_path
        self.conn = None
        
    def setup_database(self, df):
        """
        Create SQLite database and load customer data.
        """
        self.conn = sqlite3.connect(self.db_path)
        df.to_sql('customers', self.conn, if_exists='replace', index=False)
        print(f"Database created: {self.db_path}")
        print(f"Table 'customers' loaded with {len(df):,} records")
        
    def execute_query(self, query):
        """Execute SQL query and return results."""
        return pd.read_sql_query(query, self.conn)
    
    def get_churn_rate_by_segment(self):
        """
        Query 1: Calculate churn rate by customer segment.
        
        Business Question: Which customer segments have the highest churn?
        """
        query = """
        SELECT 
            customer_segment,
            COUNT(*) AS total_customers,
            SUM(churn) AS churned_customers,
            ROUND(CAST(SUM(churn) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct,
            ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges,
            ROUND(SUM(CASE WHEN churn = 1 THEN monthly_charges ELSE 0 END), 2) AS revenue_lost_monthly
        FROM customers
        GROUP BY customer_segment
        ORDER BY churn_rate_pct DESC;
        """
        return self.execute_query(query)
    
    def get_churn_rate_by_contract(self):
        """
        Query 2: Calculate churn rate by contract type.
        
        Business Question: How does contract type affect churn?
        """
        query = """
        SELECT 
            contract_type,
            COUNT(*) AS total_customers,
            SUM(churn) AS churned_customers,
            ROUND(CAST(SUM(churn) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct,
            ROUND(AVG(tenure_months), 1) AS avg_tenure_months,
            ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges
        FROM customers
        GROUP BY contract_type
        ORDER BY churn_rate_pct DESC;
        """
        return self.execute_query(query)
    
    def get_churn_rate_by_payment(self):
        """
        Query 3: Calculate churn rate by payment method.
        
        Business Question: Which payment methods correlate with higher churn?
        """
        query = """
        SELECT 
            payment_method,
            COUNT(*) AS total_customers,
            SUM(churn) AS churned_customers,
            ROUND(CAST(SUM(churn) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct,
            ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges
        FROM customers
        GROUP BY payment_method
        ORDER BY churn_rate_pct DESC;
        """
        return self.execute_query(query)
    
    def get_churn_by_internet_service(self):
        """
        Query 4: Calculate churn rate by internet service type.
        """
        query = """
        SELECT 
            internet_service,
            COUNT(*) AS total_customers,
            SUM(churn) AS churned_customers,
            ROUND(CAST(SUM(churn) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct,
            ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges
        FROM customers
        GROUP BY internet_service
        ORDER BY churn_rate_pct DESC;
        """
        return self.execute_query(query)
    
    def get_high_risk_customers(self):
        """
        Query 5: Identify high-risk customers for immediate retention focus.
        
        Risk Criteria:
        - New customers (tenure <= 12 months)
        - Month-to-month contract
        - Monthly charges > $70
        - Electronic check payment
        - No additional services
        """
        query = """
        SELECT 
            customer_id,
            tenure_months,
            contract_type,
            internet_service,
            payment_method,
            monthly_charges,
            satisfaction_score,
            risk_tier,
            Online_Security + Online_Backup + Device_Protection + 
                Tech_Support + Streaming_TV + Streaming_Movies AS total_services
        FROM customers
        WHERE risk_tier IN ('High', 'Critical')
           OR (tenure_months <= 12 
               AND contract_type = 'Month-to-Month' 
               AND monthly_charges > 70)
        ORDER BY 
            CASE risk_tier 
                WHEN 'Critical' THEN 1 
                WHEN 'High' THEN 2 
                ELSE 3 
            END,
            monthly_charges DESC
        LIMIT 100;
        """
        return self.execute_query(query)
    
    def get_revenue_loss_analysis(self):
        """
        Query 6: Calculate revenue loss due to customer churn.
        """
        query = """
        WITH churn_metrics AS (
            SELECT 
                customer_segment,
                COUNT(*) AS total_customers,
                SUM(churn) AS churned_customers,
                SUM(CASE WHEN churn = 1 THEN monthly_charges ELSE 0 END) AS monthly_revenue_lost,
                SUM(CASE WHEN churn = 0 THEN monthly_charges ELSE 0 END) AS monthly_revenue_retained,
                SUM(monthly_charges) AS total_monthly_revenue
            FROM customers
            GROUP BY customer_segment
        )
        SELECT 
            customer_segment,
            total_customers,
            churned_customers,
            ROUND(CAST(churned_customers AS FLOAT) / total_customers * 100, 2) AS churn_rate_pct,
            ROUND(monthly_revenue_lost, 2) AS monthly_revenue_lost,
            ROUND(monthly_revenue_retained, 2) AS monthly_revenue_retained,
            ROUND(monthly_revenue_lost * 12, 2) AS annual_revenue_lost,
            ROUND(monthly_revenue_lost / total_monthly_revenue * 100, 2) AS revenue_loss_pct
        FROM churn_metrics
        ORDER BY monthly_revenue_lost DESC;
        """
        return self.execute_query(query)
    
    def get_tenure_churn_analysis(self):
        """
        Query 7: Analyze churn patterns by tenure buckets.
        """
        query = """
        SELECT 
            CASE 
                WHEN tenure_months <= 6 THEN '0-6 months (Very New)'
                WHEN tenure_months <= 12 THEN '7-12 months (New)'
                WHEN tenure_months <= 24 THEN '13-24 months (Early)'
                WHEN tenure_months <= 48 THEN '25-48 months (Mid-term)'
                WHEN tenure_months <= 72 THEN '49-72 months (Long-term)'
                ELSE '73+ months (Very Long-term)'
            END AS tenure_bucket,
            COUNT(*) AS customer_count,
            SUM(churn) AS churned_count,
            ROUND(CAST(SUM(churn) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct,
            ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges
        FROM customers
        GROUP BY tenure_bucket
        ORDER BY 
            CASE tenure_bucket
                WHEN '0-6 months (Very New)' THEN 1
                WHEN '7-12 months (New)' THEN 2
                WHEN '13-24 months (Early)' THEN 3
                WHEN '25-48 months (Mid-term)' THEN 4
                WHEN '49-72 months (Long-term)' THEN 5
                ELSE 6
            END;
        """
        return self.execute_query(query)
    
    def get_monthly_charge_buckets(self):
        """
        Query 8: Analyze churn by monthly charge ranges.
        """
        query = """
        SELECT 
            CASE 
                WHEN monthly_charges < 35 THEN 'Budget (<$35)'
                WHEN monthly_charges < 55 THEN 'Standard ($35-55)'
                WHEN monthly_charges < 75 THEN 'Premium ($55-75)'
                WHEN monthly_charges < 100 THEN 'High ($75-100)'
                ELSE 'Premium+ ($100+)'
            END AS charge_range,
            COUNT(*) AS customer_count,
            SUM(churn) AS churned_count,
            ROUND(CAST(SUM(churn) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct,
            ROUND(AVG(tenure_months), 1) AS avg_tenure_months
        FROM customers
        GROUP BY charge_range
        ORDER BY 
            CASE charge_range
                WHEN 'Budget (<$35)' THEN 1
                WHEN 'Standard ($35-55)' THEN 2
                WHEN 'Premium ($55-75)' THEN 3
                WHEN 'High ($75-100)' THEN 4
                ELSE 5
            END;
        """
        return self.execute_query(query)
    
    def get_service_impact_analysis(self):
        """
        Query 9: Analyze how additional services affect churn.
        """
        query = """
        SELECT 
            total_services,
            COUNT(*) AS customer_count,
            SUM(churn) AS churned_count,
            ROUND(CAST(SUM(churn) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct,
            ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges
        FROM (
            SELECT 
                customer_id,
                churn,
                monthly_charges,
                Online_Security + Online_Backup + Device_Protection + 
                    Tech_Support + Streaming_TV + Streaming_Movies AS total_services
            FROM customers
        )
        GROUP BY total_services
        ORDER BY total_services;
        """
        return self.execute_query(query)
    
    def get_customer_value_segments(self):
        """
        Query 10: Segment customers by value (CLV perspective).
        """
        query = """
        SELECT 
            value_segment,
            COUNT(*) AS customer_count,
            SUM(churn) AS churned_count,
            ROUND(CAST(SUM(churn) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct,
            ROUND(AVG(monthly_charges), 2) AS avg_monthly_revenue,
            ROUND(SUM(monthly_charges), 2) AS total_monthly_revenue,
            ROUND(SUM(monthly_charges) * 12, 2) AS annual_revenue
        FROM (
            SELECT 
                customer_id,
                churn,
                monthly_charges,
                tenure_months,
                CASE 
                    WHEN monthly_charges >= 80 AND tenure_months >= 36 THEN 'Premium Champions'
                    WHEN monthly_charges >= 80 AND tenure_months < 36 THEN 'Premium At-Risk'
                    WHEN monthly_charges >= 50 AND tenure_months >= 24 THEN 'Valuable Loyalists'
                    WHEN monthly_charges >= 50 AND tenure_months < 24 THEN 'Valuable Newcomers'
                    WHEN monthly_charges < 50 AND tenure_months >= 36 THEN 'Budget Loyalists'
                    ELSE 'Budget Newcomers'
                END AS value_segment
            FROM customers
        )
        GROUP BY value_segment
        ORDER BY avg_monthly_revenue DESC;
        """
        return self.execute_query(query)
    
    def get_retention_opportunities(self):
        """
        Query 11: Identify specific retention opportunities.
        """
        query = """
        SELECT 
            customer_segment,
            contract_type,
            COUNT(*) AS customer_count,
            ROUND(AVG(monthly_charges), 2) AS avg_monthly_revenue,
            SUM(churn) AS churned_count,
            ROUND(CAST(SUM(churn) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct,
            ROUND(SUM(CASE WHEN churn = 1 THEN monthly_charges ELSE 0 END) * 12, 2) AS annual_revenue_at_risk
        FROM customers
        WHERE contract_type = 'Month-to-Month'
          AND tenure_months BETWEEN 6 AND 24
        GROUP BY customer_segment, contract_type
        HAVING COUNT(*) > 50
        ORDER BY churn_rate_pct DESC;
        """
        return self.execute_query(query)
    
    def get_summary_metrics(self):
        """
        Query 12: Get overall summary metrics for executive dashboard.
        """
        query = """
        SELECT 
            COUNT(*) AS total_customers,
            SUM(churn) AS total_churned,
            ROUND(CAST(SUM(churn) AS FLOAT) / COUNT(*) * 100, 2) AS overall_churn_rate,
            ROUND(SUM(monthly_charges), 2) AS total_monthly_revenue,
            ROUND(SUM(CASE WHEN churn = 1 THEN monthly_charges ELSE 0 END), 2) AS monthly_revenue_lost,
            ROUND(SUM(CASE WHEN churn = 1 THEN monthly_charges ELSE 0 END) * 12, 2) AS annual_revenue_lost,
            ROUND(AVG(tenure_months), 1) AS avg_tenure_months,
            ROUND(AVG(satisfaction_score), 1) AS avg_satisfaction_score
        FROM customers;
        """
        return self.execute_query(query)
    
    def close_connection(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
    
    def run_all_queries(self):
        """Execute all SQL queries and return results."""
        print("=" * 80)
        print("SQL ANALYSIS RESULTS")
        print("=" * 80)
        
        results = {
            'summary_metrics': self.get_summary_metrics(),
            'churn_by_segment': self.get_churn_rate_by_segment(),
            'churn_by_contract': self.get_churn_rate_by_contract(),
            'churn_by_payment': self.get_churn_rate_by_payment(),
            'churn_by_internet': self.get_churn_by_internet_service(),
            'high_risk_customers': self.get_high_risk_customers(),
            'revenue_loss': self.get_revenue_loss_analysis(),
            'tenure_churn': self.get_tenure_churn_analysis(),
            'charge_buckets': self.get_monthly_charge_buckets(),
            'service_impact': self.get_service_impact_analysis(),
            'value_segments': self.get_customer_value_segments(),
            'retention_opportunities': self.get_retention_opportunities()
        }
        
        for name, df in results.items():
            print(f"\n{name.upper().replace('_', ' ')}")
            print("-" * 60)
            print(df.to_string(index=False))
        
        return results


def save_sql_queries():
    """Save SQL queries to file for reference."""
    queries = """
-- ================================================
-- CUSTOMER CHURN PREDICTION - SQL QUERIES
-- ================================================

-- 1. CHURN RATE BY CUSTOMER SEGMENT
SELECT 
    customer_segment,
    COUNT(*) AS total_customers,
    SUM(churn) AS churned_customers,
    ROUND(CAST(SUM(churn) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN churn = 1 THEN monthly_charges ELSE 0 END), 2) AS revenue_lost_monthly
FROM customers
GROUP BY customer_segment
ORDER BY churn_rate_pct DESC;

-- 2. HIGH-RISK CUSTOMERS IDENTIFICATION
SELECT 
    customer_id,
    tenure_months,
    contract_type,
    monthly_charges,
    satisfaction_score,
    risk_tier
FROM customers
WHERE tenure_months <= 12 
   AND contract_type = 'Month-to-Month' 
   AND monthly_charges > 70
ORDER BY monthly_charges DESC
LIMIT 100;

-- 3. REVENUE LOSS CALCULATION BY SEGMENT
WITH revenue_analysis AS (
    SELECT 
        customer_segment,
        SUM(CASE WHEN churn = 1 THEN monthly_charges ELSE 0 END) AS monthly_loss,
        SUM(CASE WHEN churn = 1 THEN monthly_charges ELSE 0 END) * 12 AS annual_loss
    FROM customers
    GROUP BY customer_segment
)
SELECT 
    customer_segment,
    ROUND(monthly_loss, 2) AS monthly_revenue_lost,
    ROUND(annual_loss, 2) AS annual_revenue_lost
FROM revenue_analysis
ORDER BY annual_loss DESC;

-- 4. CHURN RATE BY TENURE BUCKETS
SELECT 
    CASE 
        WHEN tenure_months <= 12 THEN 'New (0-12)'
        WHEN tenure_months <= 24 THEN 'Early (13-24)'
        WHEN tenure_months <= 48 THEN 'Mid (25-48)'
        ELSE 'Long (49+)'
    END AS tenure_group,
    COUNT(*) AS customer_count,
    ROUND(CAST(SUM(churn) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct
FROM customers
GROUP BY tenure_group;

-- 5. SERVICE IMPACT ON RETENTION
SELECT 
    Online_Security + Online_Backup + Device_Protection + 
        Tech_Support + Streaming_TV + Streaming_Movies AS services_count,
    COUNT(*) AS customer_count,
    ROUND(CAST(SUM(churn) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct
FROM customers
GROUP BY services_count
ORDER BY services_count;
"""
    
    with open('sql/churn_queries.sql', 'w') as f:
        f.write(queries)
    
    print("SQL queries saved to sql/churn_queries.sql")


def main():
    """Run SQL analysis on customer data."""
    df = pd.read_csv('data/customer_data.csv')
    
    analyzer = ChurnSQLAnalyzer()
    analyzer.setup_database(df)
    
    results = analyzer.run_all_queries()
    
    analyzer.close_connection()
    
    save_sql_queries()
    
    return results


if __name__ == "__main__":
    main()
