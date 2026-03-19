"""
Insights & Business Recommendations Module
============================================
Transforms data analysis into actionable business insights and retention strategies.
"""

import pandas as pd
import numpy as np


class ChurnInsights:
    """
    Generate business insights and actionable recommendations.
    """
    
    def __init__(self, df):
        self.df = df
        self.target_col = 'churn'
        
    def calculate_key_metrics(self):
        """Calculate key business metrics."""
        total_customers = len(self.df)
        churned = self.df[self.target_col].sum()
        retained = total_customers - churned
        churn_rate = self.df[self.target_col].mean() * 100
        
        monthly_revenue = self.df['monthly_charges'].sum()
        churned_revenue = self.df[self.df[self.target_col] == 1]['monthly_charges'].sum()
        annual_churned_revenue = churned_revenue * 12
        
        metrics = {
            'total_customers': total_customers,
            'churned_customers': int(churned),
            'retained_customers': int(retained),
            'churn_rate_pct': round(churn_rate, 2),
            'retention_rate_pct': round(100 - churn_rate, 2),
            'monthly_revenue': round(monthly_revenue, 2),
            'monthly_revenue_lost': round(churned_revenue, 2),
            'annual_revenue_lost': round(annual_churned_revenue, 2),
            'avg_monthly_charges': round(self.df['monthly_charges'].mean(), 2),
            'avg_tenure': round(self.df['tenure_months'].mean(), 1)
        }
        
        return metrics
    
    def get_segment_analysis(self):
        """Analyze churn by customer segment."""
        segments = ['New', 'Developing', 'Established', 'Loyal']
        
        analysis = {}
        for segment in segments:
            subset = self.df[self.df['customer_segment'] == segment]
            analysis[segment] = {
                'count': len(subset),
                'churn_rate': round(subset[self.target_col].mean() * 100, 2),
                'avg_tenure': round(subset['tenure_months'].mean(), 1),
                'avg_monthly_charges': round(subset['monthly_charges'].mean(), 2),
                'revenue_at_risk': round(subset[subset[self.target_col] == 1]['monthly_charges'].sum(), 2)
            }
        
        return analysis
    
    def get_high_risk_segments(self):
        """Identify highest risk customer segments."""
        high_risk = []
        
        month_to_month = self.df[self.df['contract_type'] == 'Month-to-Month']
        high_risk.append({
            'segment': 'Month-to-Month Contract Holders',
            'size': len(month_to_month),
            'churn_rate': round(month_to_month[self.target_col].mean() * 100, 2),
            'reason': 'No commitment barrier to leaving'
        })
        
        new_high_charge = self.df[(self.df['tenure_months'] <= 12) & 
                                   (self.df['monthly_charges'] > 70)]
        high_risk.append({
            'segment': 'New High-Paying Customers',
            'size': len(new_high_charge),
            'churn_rate': round(new_high_charge[self.target_col].mean() * 100, 2),
            'reason': 'Price-sensitive at onboarding with high expectations'
        })
        
        electronic = self.df[self.df['payment_method'] == 'Electronic Check']
        high_risk.append({
            'segment': 'Electronic Check Users',
            'size': len(electronic),
            'churn_rate': round(electronic[self.target_col].mean() * 100, 2),
            'reason': 'Manual payment process creates friction'
        })
        
        low_services = self.df[self.df['total_services'] if 'total_services' in self.df.columns 
                              else self.df[['Online_Security', 'Online_Backup', 'Device_Protection',
                                           'Tech_Support', 'Streaming_TV', 'Streaming_Movies']].sum(axis=1) < 2]
        
        return high_risk
    
    def quantify_insights(self):
        """Quantify key insights with specific numbers."""
        insights = []
        
        # Insight 1: Tenure-Churn Relationship
        new_churn = self.df[self.df['tenure_months'] <= 12][self.target_col].mean() * 100
        old_churn = self.df[self.df['tenure_months'] >= 48][self.target_col].mean() * 100
        insights.append({
            'category': 'Tenure Impact',
            'insight': f'New customers (<12 months) churn at {new_churn:.1f}% vs {old_churn:.1f}% for long-tenure customers (48+ months)',
            'quantified': f'{new_churn/old_churn:.1f}x higher churn risk for new customers',
            'impact': 'HIGH'
        })
        
        # Insight 2: Contract Type Impact
        mtom_churn = self.df[self.df['contract_type'] == 'Month-to-Month'][self.target_col].mean() * 100
        two_year_churn = self.df[self.df['contract_type'] == 'Two Year'][self.target_col].mean() * 100
        insights.append({
            'category': 'Contract Impact',
            'insight': f'Month-to-month customers churn at {mtom_churn:.1f}% vs only {two_year_churn:.1f}% for two-year contracts',
            'quantified': f'{mtom_churn/two_year_churn:.1f}x higher churn without contract commitment',
            'impact': 'CRITICAL'
        })
        
        # Insight 3: Payment Method Impact
        echeck_churn = self.df[self.df['payment_method'] == 'Electronic Check'][self.target_col].mean() * 100
        auto_churn = self.df[self.df['payment_method'].str.contains('Automatic')][self.target_col].mean() * 100
        insights.append({
            'category': 'Payment Method Impact',
            'insight': f'Electronic check users churn at {echeck_churn:.1f}% vs {auto_churn:.1f}% for auto-pay customers',
            'quantified': f'${self.df[self.df[self.target_col]==1]["monthly_charges"].sum():,.0f} monthly revenue at risk from payment method',
            'impact': 'HIGH'
        })
        
        # Insight 4: Service Bundle Impact
        service_cols = ['Online_Security', 'Online_Backup', 'Device_Protection',
                       'Tech_Support', 'Streaming_TV', 'Streaming_Movies']
        self.df['total_services_calc'] = self.df[service_cols].sum(axis=1)
        
        no_service_churn = self.df[self.df['total_services_calc'] == 0][self.target_col].mean() * 100
        high_service_churn = self.df[self.df['total_services_calc'] >= 4][self.target_col].mean() * 100
        insights.append({
            'category': 'Service Bundle Impact',
            'insight': f'Customers with no add-on services churn at {no_service_churn:.1f}% vs {high_service_churn:.1f}% for engaged customers (4+ services)',
            'quantified': f'Service adoption reduces churn by {no_service_churn - high_service_churn:.1f} percentage points',
            'impact': 'HIGH'
        })
        
        # Insight 5: Monthly Charge Impact
        high_charge_churn = self.df[self.df['monthly_charges'] > 80][self.target_col].mean() * 100
        low_charge_churn = self.df[self.df['monthly_charges'] <= 50][self.target_col].mean() * 100
        insights.append({
            'category': 'Price Sensitivity',
            'insight': f'High-charge customers ($80+) churn at {high_charge_churn:.1f}% vs {low_charge_churn:.1f}% for budget customers ($50 or less)',
            'quantified': f'Higher prices correlate with {high_charge_churn/low_charge_churn:.1f}x more churn',
            'impact': 'MEDIUM'
        })
        
        return insights
    
    def generate_retention_strategies(self):
        """
        Generate actionable retention strategies.
        """
        strategies = [
            {
                'name': 'Early Engagement Program',
                'target_segment': 'New Customers (0-12 months)',
                'current_churn_rate': f"{self.df[self.df['tenure_months'] <= 12][self.target_col].mean()*100:.1f}%",
                'actions': [
                    'Onboarding welcome series with service education',
                    'Dedicated support hotline for first 90 days',
                    'Personal check-in calls at 30/60/90 day marks',
                    'Special "new customer" pricing lock for 6 months'
                ],
                'expected_impact': '15-20% reduction in new customer churn',
                'cost_estimate': 'Medium (Staff time + reduced pricing)',
                'priority': 'HIGH'
            },
            {
                'name': 'Contract Upgrade Campaign',
                'target_segment': 'Month-to-Month Contract Holders',
                'current_churn_rate': f"{self.df[self.df['contract_type'] == 'Month-to-Month'][self.target_col].mean()*100:.1f}%",
                'actions': [
                    'Offer 3-month contract at discounted rate',
                    'Highlight benefits of annual commitment',
                    'Provide free month of premium service for upgrade',
                    'Create urgency with "loyalty pricing" expiring'
                ],
                'expected_impact': '25-30% reduction in month-to-month churn',
                'cost_estimate': 'Low-Medium (Revenue discount + free services)',
                'priority': 'CRITICAL'
            },
            {
                'name': 'Auto-Pay Migration Program',
                'target_segment': 'Electronic Check Users',
                'current_churn_rate': f"{self.df[self.df['payment_method'] == 'Electronic Check'][self.target_col].mean()*100:.1f}%",
                'actions': [
                    'Offer $5/month discount for auto-pay enrollment',
                    'Simplify enrollment process',
                    'Send personalized outreach explaining benefits',
                    'Offer one-time $25 bill credit after 3 months auto-pay'
                ],
                'expected_impact': '20-25% reduction in electronic check churn',
                'cost_estimate': 'Low (Discount cost offset by reduced churn)',
                'priority': 'HIGH'
            },
            {
                'name': 'Service Bundle Upsell',
                'target_segment': 'Customers with <2 Additional Services',
                'current_churn_rate': f"{self.df[self.df['total_services_calc'] < 2][self.target_col].mean()*100:.1f}%",
                'actions': [
                    'Create "Essential Bundle" with Security + Support at 20% discount',
                    'Personalized recommendations based on usage',
                    'Free trial periods for premium services',
                    'Cross-sell training for customer service team'
                ],
                'expected_impact': '18-22% reduction in low-engagement churn',
                'cost_estimate': 'Medium (Bundle pricing + training)',
                'priority': 'HIGH'
            },
            {
                'name': 'Price Optimization & Retention Offers',
                'target_segment': 'High-Value, High-Churn Risk Customers',
                'current_churn_rate': f"{self.df[(self.df['monthly_charges'] > 80) & (self.df['tenure_months'] < 24)][self.target_col].mean()*100:.1f}%",
                'actions': [
                    'Implement price freeze for 12 months',
                    'Offer "loyalty discount" for customers approaching renewal',
                    'Create "price protection" guarantee',
                    'Develop competitor price matching program'
                ],
                'expected_impact': '20-25% reduction in price-sensitive churn',
                'cost_estimate': 'Medium-High (Revenue impact)',
                'priority': 'HIGH'
            },
            {
                'name': 'Customer Appreciation & Loyalty Program',
                'target_segment': 'All At-Risk Segments',
                'current_churn_rate': 'Variable by segment',
                'actions': [
                    'Launch tiered loyalty rewards program',
                    'Celebrate customer milestones (anniversaries)',
                    'Provide exclusive access to new features',
                    'Create customer community/events'
                ],
                'expected_impact': '10-15% overall churn reduction',
                'cost_estimate': 'Medium (Program development + rewards)',
                'priority': 'MEDIUM'
            }
        ]
        
        return strategies
    
    def calculate_roi_projections(self):
        """
        Calculate ROI projections for retention strategies.
        """
        total_churned = self.df[self.target_col].sum()
        avg_monthly_revenue = self.df['monthly_charges'].mean()
        annual_revenue_lost = self.df[self.df[self.target_col] == 1]['monthly_charges'].sum() * 12
        
        projections = {
            'baseline_annual_loss': round(annual_revenue_lost, 2),
            'retention_investment_estimate': round(annual_revenue_lost * 0.10),
            'projections': {
                '20%_churn_reduction': {
                    'customers_retained': int(total_churned * 0.20),
                    'annual_savings': round(annual_revenue_lost * 0.20, 2),
                    'roi_pct': 100
                },
                '30%_churn_reduction': {
                    'customers_retained': int(total_churned * 0.30),
                    'annual_savings': round(annual_revenue_lost * 0.30, 2),
                    'roi_pct': 200
                },
                '40%_churn_reduction': {
                    'customers_retained': int(total_churned * 0.40),
                    'annual_savings': round(annual_revenue_lost * 0.40, 2),
                    'roi_pct': 300
                }
            }
        }
        
        return projections
    
    def generate_full_report(self):
        """Generate comprehensive insights and recommendations report."""
        metrics = self.calculate_key_metrics()
        segments = self.get_segment_analysis()
        insights = self.quantify_insights()
        strategies = self.generate_retention_strategies()
        roi = self.calculate_roi_projections()
        
        report = f"""
{'='*100}
CUSTOMER CHURN PREDICTION & RETENTION STRATEGY REPORT
{'='*100}

================================================================================
EXECUTIVE SUMMARY
================================================================================

Total Customers Analyzed: {metrics['total_customers']:,}
Current Churn Rate: {metrics['churn_rate_pct']}%
Monthly Revenue at Risk: ${metrics['monthly_revenue_lost']:,.2f}
Annual Revenue at Risk: ${metrics['annual_revenue_lost']:,.2f}

KEY FINDING: {(metrics['churn_rate_pct'] * metrics['total_customers'] / 100):,.0f} customers churn monthly, 
costing the business ${metrics['annual_revenue_lost']:,.0f} in annual recurring revenue.

================================================================================
QUANTIFIED INSIGHTS
================================================================================
"""
        
        for i, insight in enumerate(insights, 1):
            report += f"""
{i}. {insight['category']} [{insight['impact']} IMPACT]
   Finding: {insight['insight']}
   Quantified: {insight['quantified']}
"""
        
        report += """
================================================================================
SEGMENT ANALYSIS
================================================================================
"""
        
        for segment, data in segments.items():
            report += f"""
{segment} Customers:
  - Count: {data['count']:,}
  - Churn Rate: {data['churn_rate']}%
  - Avg Tenure: {data['avg_tenure']} months
  - Avg Monthly Charges: ${data['avg_monthly_charges']:.2f}
  - Revenue at Risk: ${data['revenue_at_risk']:,.2f}
"""
        
        report += """
================================================================================
RETENTION STRATEGY RECOMMENDATIONS
================================================================================
"""
        
        for i, strategy in enumerate(strategies, 1):
            report += f"""
{i}. {strategy['name']}
    Target: {strategy['target_segment']}
    Current Churn Rate: {strategy['current_churn_rate']}
    
    Actions:
"""
            for action in strategy['actions']:
                report += f"      - {action}\n"
            
            report += f"""
    Expected Impact: {strategy['expected_impact']}
    Cost Estimate: {strategy['cost_estimate']}
    Priority: {strategy['priority']}
"""
        
        report += f"""
================================================================================
ROI PROJECTIONS
================================================================================

Current Annual Revenue Loss from Churn: ${roi['baseline_annual_loss']:,.2f}
Estimated Retention Program Investment: ${roi['retention_investment_estimate']:,.2f}

Scenario Analysis:
"""
        
        for scenario, data in roi['projections'].items():
            report += f"""
{scenario}:
  - Customers Retained: {data['customers_retained']:,}
  - Annual Savings: ${data['annual_savings']:,.2f}
  - ROI: {data['roi_pct']}%
"""
        
        report += """
================================================================================
IMPLEMENTATION PRIORITIES
================================================================================

IMMEDIATE (Next 30 Days):
1. Launch auto-pay migration program for electronic check users
2. Begin contract upgrade outreach for month-to-month customers
3. Deploy early engagement program for new customer onboarding

SHORT-TERM (30-90 Days):
1. Create and promote service bundles
2. Implement price protection offers for high-value customers
3. Launch loyalty rewards pilot program

LONG-TERM (90+ Days):
1. Full loyalty program rollout
2. Customer appreciation events
3. Continuous monitoring and optimization

================================================================================
KEY SUCCESS METRICS (KPIs)
================================================================================

Primary Metrics:
- Churn Rate: Current {metrics['churn_rate_pct']}% → Target <{metrics['churn_rate_pct'] * 0.7:.1f}%
- Customer Retention Rate: Current {metrics['retention_rate_pct']}% → Target >{min(100, metrics['retention_rate_pct'] + 10):.1f}%
- Monthly Recurring Revenue (MRR) Growth: Target 5% increase

Secondary Metrics:
- Contract Upgrade Rate: Target 15% of month-to-month customers
- Auto-Pay Enrollment: Target 80% of eligible customers
- Service Bundle Adoption: Target 60% of customers with 2+ services
- Customer Satisfaction Score: Target 8.0+ average

================================================================================
CONCLUSION
================================================================================

This analysis identifies clear patterns in customer churn and provides
actionable strategies to reduce customer attrition. The combination of
targeted retention offers, improved onboarding, and loyalty programs can
potentially save ${roi['projections']['30%_churn_reduction']['annual_savings']:,.0f} annually.

Priority should be given to:
1. Converting month-to-month customers to longer contracts
2. Migrating customers to auto-pay methods
3. Increasing service adoption among at-risk segments
4. Improving the new customer experience

Regular monitoring and A/B testing of retention offers will be critical
to optimizing ROI and achieving target churn reduction.

================================================================================
Report Generated: Churn Prediction Analysis 2025
================================================================================
"""
        
        return report


def main():
    """Generate insights report."""
    df = pd.read_csv('data/customer_data.csv')
    
    analyzer = ChurnInsights(df)
    report = analyzer.generate_full_report()
    
    with open('results/business_insights_report.txt', 'w') as f:
        f.write(report)
    
    print(report)
    print("\nReport saved to results/business_insights_report.txt")
    
    return report


if __name__ == "__main__":
    main()
