"""
Exploratory Data Analysis Module
=================================
Comprehensive EDA for customer churn prediction including:
- Univariate analysis
- Bivariate analysis
- Correlation analysis
- Statistical tests
- Visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import chi2_contingency, ttest_ind
import warnings
import os

warnings.filterwarnings('ignore')

# Set visualization style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Create output directory for visualizations
os.makedirs('results/visualizations', exist_ok=True)


class ChurnEDA:
    """
    Comprehensive Exploratory Data Analysis for Telecom Churn Prediction.
    """
    
    def __init__(self, df, target_col='churn'):
        self.df = df
        self.target_col = target_col
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
    def generate_summary_statistics(self):
        """Generate comprehensive summary statistics."""
        print("=" * 80)
        print("EXPLORATORY DATA ANALYSIS - CUSTOMER CHURN PREDICTION")
        print("=" * 80)
        
        print("\n1. DATASET OVERVIEW")
        print("-" * 40)
        print(f"Total Records: {len(self.df):,}")
        print(f"Total Features: {len(self.df.columns)}")
        print(f"Target Variable: {self.target_col}")
        print(f"Churn Distribution:")
        print(f"  - Churned: {self.df[self.target_col].sum():,} ({self.df[self.target_col].mean()*100:.2f}%)")
        print(f"  - Retained: {(1-self.df[self.target_col]).sum():,} ({(1-self.df[self.target_col].mean())*100:.2f}%)")
        
        print("\n2. NUMERIC FEATURES SUMMARY")
        print("-" * 40)
        numeric_summary = self.df[self.numeric_cols].describe()
        print(numeric_summary.round(2).to_string())
        
        print("\n3. CATEGORICAL FEATURES SUMMARY")
        print("-" * 40)
        for col in self.categorical_cols:
            if col not in ['customer_id', 'account_creation_date', 'last_activity_date']:
                print(f"\n{col}:")
                print(self.df[col].value_counts())
                
        return {
            'total_records': len(self.df),
            'churn_rate': self.df[self.target_col].mean(),
            'numeric_summary': numeric_summary
        }
    
    def analyze_churn_by_segment(self):
        """Analyze churn rates across different customer segments."""
        print("\n4. CHURN ANALYSIS BY SEGMENT")
        print("-" * 40)
        
        churn_analysis = {}
        
        # By Contract Type
        contract_churn = self.df.groupby('contract_type')[self.target_col].agg(['mean', 'count'])
        contract_churn.columns = ['churn_rate', 'count']
        contract_churn['churn_rate'] = contract_churn['churn_rate'] * 100
        print("\nChurn by Contract Type:")
        print(contract_churn.round(2).to_string())
        churn_analysis['contract'] = contract_churn
        
        # By Internet Service
        internet_churn = self.df.groupby('internet_service')[self.target_col].agg(['mean', 'count'])
        internet_churn.columns = ['churn_rate', 'count']
        internet_churn['churn_rate'] = internet_churn['churn_rate'] * 100
        print("\nChurn by Internet Service:")
        print(internet_churn.round(2).to_string())
        churn_analysis['internet'] = internet_churn
        
        # By Payment Method
        payment_churn = self.df.groupby('payment_method')[self.target_col].agg(['mean', 'count'])
        payment_churn.columns = ['churn_rate', 'count']
        payment_churn['churn_rate'] = payment_churn['churn_rate'] * 100
        print("\nChurn by Payment Method:")
        print(payment_churn.round(2).to_string())
        churn_analysis['payment'] = payment_churn
        
        # By Customer Segment
        segment_churn = self.df.groupby('customer_segment')[self.target_col].agg(['mean', 'count'])
        segment_churn.columns = ['churn_rate', 'count']
        segment_churn['churn_rate'] = segment_churn['churn_rate'] * 100
        print("\nChurn by Customer Segment:")
        print(segment_churn.round(2).to_string())
        churn_analysis['segment'] = segment_churn
        
        # By Risk Tier
        risk_churn = self.df.groupby('risk_tier')[self.target_col].agg(['mean', 'count'])
        risk_churn.columns = ['churn_rate', 'count']
        risk_churn['churn_rate'] = risk_churn['churn_rate'] * 100
        print("\nChurn by Risk Tier:")
        print(risk_churn.round(2).to_string())
        churn_analysis['risk'] = risk_churn
        
        return churn_analysis
    
    def analyze_correlations(self):
        """Analyze correlations between features and churn."""
        print("\n5. CORRELATION ANALYSIS")
        print("-" * 40)
        
        # Select numeric columns for correlation
        corr_cols = ['tenure_months', 'monthly_charges', 'total_charges', 
                     'Online_Security', 'Online_Backup', 'Device_Protection',
                     'Tech_Support', 'Streaming_TV', 'Streaming_Movies',
                     'satisfaction_score', self.target_col]
        
        corr_matrix = self.df[corr_cols].corr()
        
        print("\nCorrelation with Churn:")
        churn_corr = corr_matrix[self.target_col].sort_values(ascending=False)
        print(churn_corr.round(3).to_string())
        
        return corr_matrix, churn_corr
    
    def statistical_tests(self):
        """Perform statistical tests for churn significance."""
        print("\n6. STATISTICAL SIGNIFICANCE TESTS")
        print("-" * 40)
        
        churned = self.df[self.df[self.target_col] == 1]
        retained = self.df[self.df[self.target_col] == 0]
        
        test_results = {}
        
        # T-tests for continuous variables
        continuous_vars = ['tenure_months', 'monthly_charges', 'total_charges', 'satisfaction_score']
        
        print("\nT-Test Results (Churned vs Retained):")
        for var in continuous_vars:
            t_stat, p_value = ttest_ind(churned[var], retained[var])
            significance = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else ""
            print(f"  {var}: t={t_stat:.3f}, p={p_value:.6f} {significance}")
            test_results[var] = {'t_stat': t_stat, 'p_value': p_value}
        
        # Chi-square tests for categorical variables
        categorical_vars = ['contract_type', 'internet_service', 'payment_method', 'customer_segment']
        
        print("\nChi-Square Test Results:")
        for var in categorical_vars:
            contingency_table = pd.crosstab(self.df[var], self.df[self.target_col])
            chi2, p_value, dof, expected = chi2_contingency(contingency_table)
            significance = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else ""
            print(f"  {var}: chi2={chi2:.3f}, p={p_value:.6f} {significance}")
            test_results[var] = {'chi2': chi2, 'p_value': p_value}
        
        return test_results
    
    def create_visualizations(self):
        """Generate all visualizations."""
        print("\n7. GENERATING VISUALIZATIONS")
        print("-" * 40)
        
        # Figure 1: Churn Distribution Overview
        self._plot_churn_distribution()
        
        # Figure 2: Churn by Contract Type
        self._plot_churn_by_contract()
        
        # Figure 3: Churn by Tenure
        self._plot_churn_by_tenure()
        
        # Figure 4: Churn by Payment Method
        self._plot_churn_by_payment()
        
        # Figure 5: Monthly Charges Distribution
        self._plot_charges_distribution()
        
        # Figure 6: Correlation Heatmap
        self._plot_correlation_heatmap()
        
        # Figure 7: Tenure vs Monthly Charges
        self._plot_tenure_charges()
        
        # Figure 8: Service Analysis
        self._plot_service_analysis()
        
        # Figure 9: Risk Tier Analysis
        self._plot_risk_analysis()
        
        # Figure 10: Customer Segment Analysis
        self._plot_segment_analysis()
        
        # Figure 11: Revenue Impact
        self._plot_revenue_impact()
        
        print("All visualizations saved to results/visualizations/")
        
    def _plot_churn_distribution(self):
        """Plot churn distribution pie chart."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Pie chart
        churn_counts = self.df[self.target_col].value_counts()
        colors = ['#2ecc71', '#e74c3c']
        axes[0].pie(churn_counts, labels=['Retained', 'Churned'], autopct='%1.1f%%',
                   colors=colors, explode=(0, 0.1), shadow=True)
        axes[0].set_title('Overall Churn Distribution', fontsize=14, fontweight='bold')
        
        # Bar chart
        segments = self.df['customer_segment'].value_counts()
        churn_by_segment = self.df.groupby('customer_segment')[self.target_col].mean() * 100
        
        x = np.arange(len(churn_by_segment.index))
        bars = axes[1].bar(x, churn_by_segment.values, color=colors[1], alpha=0.7)
        axes[1].set_xlabel('Customer Segment')
        axes[1].set_ylabel('Churn Rate (%)')
        axes[1].set_title('Churn Rate by Customer Segment', fontsize=14, fontweight='bold')
        axes[1].set_xticks(x)
        axes[1].set_xticklabels(churn_by_segment.index)
        
        # Add value labels on bars
        for bar, val in zip(bars, churn_by_segment.values):
            axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                        f'{val:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('results/visualizations/01_churn_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def _plot_churn_by_contract(self):
        """Plot churn analysis by contract type."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        contract_data = self.df.groupby('contract_type')[self.target_col].agg(['mean', 'count'])
        contract_data['churn_rate'] = contract_data['mean'] * 100
        
        colors = ['#3498db', '#9b59b6', '#1abc9c']
        
        # Churn rate by contract
        axes[0].barh(contract_data.index, contract_data['churn_rate'], color=colors)
        axes[0].set_xlabel('Churn Rate (%)')
        axes[0].set_title('Churn Rate by Contract Type', fontsize=14, fontweight='bold')
        for i, (idx, row) in enumerate(contract_data.iterrows()):
            axes[0].text(row['churn_rate'] + 0.5, i, f'{row["churn_rate"]:.1f}%', va='center')
        
        # Tenure distribution by contract
        for i, contract in enumerate(['Month-to-Month', 'One Year', 'Two Year']):
            subset = self.df[self.df['contract_type'] == contract]['tenure_months']
            axes[1].hist(subset, bins=30, alpha=0.6, label=contract, color=colors[i])
        
        axes[1].set_xlabel('Tenure (Months)')
        axes[1].set_ylabel('Frequency')
        axes[1].set_title('Tenure Distribution by Contract Type', fontsize=14, fontweight='bold')
        axes[1].legend()
        
        plt.tight_layout()
        plt.savefig('results/visualizations/02_churn_by_contract.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def _plot_churn_by_tenure(self):
        """Plot churn analysis by tenure."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Create tenure bins
        tenure_bins = [0, 12, 24, 48, 72, 100]
        tenure_labels = ['0-12', '13-24', '25-48', '49-72', '73+']
        self.df['tenure_group'] = pd.cut(self.df['tenure_months'], bins=tenure_bins, labels=tenure_labels)
        
        # Churn rate by tenure group
        tenure_churn = self.df.groupby('tenure_group')[self.target_col].mean() * 100
        
        colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(tenure_labels)))
        bars = axes[0].bar(tenure_labels, tenure_churn.values, color=colors)
        axes[0].set_xlabel('Tenure Group (Months)')
        axes[0].set_ylabel('Churn Rate (%)')
        axes[0].set_title('Churn Rate by Tenure Group', fontsize=14, fontweight='bold')
        
        for bar, val in zip(bars, tenure_churn.values):
            axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                        f'{val:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # Box plot of tenure by churn
        churned_tenure = self.df[self.df[self.target_col] == 1]['tenure_months']
        retained_tenure = self.df[self.df[self.target_col] == 0]['tenure_months']
        
        bp = axes[1].boxplot([retained_tenure, churned_tenure], 
                            labels=['Retained', 'Churned'],
                            patch_artist=True)
        bp['boxes'][0].set_facecolor('#2ecc71')
        bp['boxes'][1].set_facecolor('#e74c3c')
        axes[1].set_ylabel('Tenure (Months)')
        axes[1].set_title('Tenure Distribution: Retained vs Churned', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('results/visualizations/03_churn_by_tenure.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def _plot_churn_by_payment(self):
        """Plot churn analysis by payment method."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        payment_data = self.df.groupby('payment_method')[self.target_col].agg(['mean', 'count'])
        payment_data['churn_rate'] = payment_data['mean'] * 100
        payment_data = payment_data.sort_values('churn_rate', ascending=True)
        
        colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(payment_data)))
        bars = axes[0].barh(payment_data.index, payment_data['churn_rate'], color=colors)
        axes[0].set_xlabel('Churn Rate (%)')
        axes[0].set_title('Churn Rate by Payment Method', fontsize=14, fontweight='bold')
        
        for bar, val in zip(bars, payment_data['churn_rate'].values):
            axes[0].text(val + 0.5, bar.get_y() + bar.get_height()/2,
                        f'{val:.1f}%', va='center', fontweight='bold')
        
        # Monthly charges by payment method
        payment_charges = self.df.groupby('payment_method')['monthly_charges'].mean()
        payment_charges = payment_charges.reindex(payment_data.index)
        
        axes[1].barh(payment_charges.index, payment_charges.values, color='#3498db', alpha=0.7)
        axes[1].set_xlabel('Average Monthly Charges ($)')
        axes[1].set_title('Average Monthly Charges by Payment Method', fontsize=14, fontweight='bold')
        
        for i, val in enumerate(payment_charges.values):
            axes[1].text(val + 0.5, i, f'${val:.2f}', va='center')
        
        plt.tight_layout()
        plt.savefig('results/visualizations/04_churn_by_payment.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def _plot_charges_distribution(self):
        """Plot charges distribution analysis."""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Monthly charges distribution
        axes[0, 0].hist(self.df['monthly_charges'], bins=50, color='#3498db', alpha=0.7, edgecolor='black')
        axes[0, 0].axvline(self.df['monthly_charges'].mean(), color='red', linestyle='--', label=f'Mean: ${self.df["monthly_charges"].mean():.2f}')
        axes[0, 0].set_xlabel('Monthly Charges ($)')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].set_title('Monthly Charges Distribution', fontsize=12, fontweight='bold')
        axes[0, 0].legend()
        
        # Monthly charges by churn
        retained_charges = self.df[self.df[self.target_col] == 0]['monthly_charges']
        churned_charges = self.df[self.df[self.target_col] == 1]['monthly_charges']
        
        axes[0, 1].hist(retained_charges, bins=50, alpha=0.7, label='Retained', color='#2ecc71')
        axes[0, 1].hist(churned_charges, bins=50, alpha=0.7, label='Churned', color='#e74c3c')
        axes[0, 1].set_xlabel('Monthly Charges ($)')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].set_title('Monthly Charges: Retained vs Churned', fontsize=12, fontweight='bold')
        axes[0, 1].legend()
        
        # Total charges by churn
        retained_total = self.df[self.df[self.target_col] == 0]['total_charges']
        churned_total = self.df[self.df[self.target_col] == 1]['total_charges']
        
        axes[1, 0].hist(retained_total, bins=50, alpha=0.7, label='Retained', color='#2ecc71')
        axes[1, 0].hist(churned_total, bins=50, alpha=0.7, label='Churned', color='#e74c3c')
        axes[1, 0].set_xlabel('Total Charges ($)')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].set_title('Total Charges: Retained vs Churned', fontsize=12, fontweight='bold')
        axes[1, 0].legend()
        
        # Charges by contract type
        contract_charges = self.df.groupby('contract_type')['monthly_charges'].mean().sort_values()
        bars = axes[1, 1].bar(contract_charges.index, contract_charges.values, color=['#1abc9c', '#3498db', '#9b59b6'])
        axes[1, 1].set_xlabel('Contract Type')
        axes[1, 1].set_ylabel('Average Monthly Charges ($)')
        axes[1, 1].set_title('Average Monthly Charges by Contract Type', fontsize=12, fontweight='bold')
        
        for bar, val in zip(bars, contract_charges.values):
            axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                           f'${val:.2f}', ha='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('results/visualizations/05_charges_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def _plot_correlation_heatmap(self):
        """Plot correlation heatmap."""
        corr_cols = ['tenure_months', 'monthly_charges', 'total_charges', 
                     'Online_Security', 'Online_Backup', 'Device_Protection',
                     'Tech_Support', 'Streaming_TV', 'Streaming_Movies',
                     'satisfaction_score', self.target_col]
        
        corr_matrix = self.df[corr_cols].corr()
        
        plt.figure(figsize=(12, 10))
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='RdYlGn', center=0,
                   fmt='.2f', linewidths=0.5, vmin=-1, vmax=1,
                   annot_kws={'size': 9})
        plt.title('Feature Correlation Heatmap', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('results/visualizations/06_correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def _plot_tenure_charges(self):
        """Plot tenure vs monthly charges scatter."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Scatter plot
        retained = self.df[self.df[self.target_col] == 0]
        churned = self.df[self.df[self.target_col] == 1]
        
        axes[0].scatter(retained['tenure_months'], retained['monthly_charges'], 
                      alpha=0.5, s=10, c='#2ecc71', label='Retained')
        axes[0].scatter(churned['tenure_months'], churned['monthly_charges'], 
                      alpha=0.5, s=10, c='#e74c3c', label='Churned')
        axes[0].set_xlabel('Tenure (Months)')
        axes[0].set_ylabel('Monthly Charges ($)')
        axes[0].set_title('Tenure vs Monthly Charges by Churn Status', fontsize=12, fontweight='bold')
        axes[0].legend()
        
        # Add high-risk zone
        axes[0].axhline(y=70, color='red', linestyle='--', alpha=0.5)
        axes[0].axvline(x=12, color='red', linestyle='--', alpha=0.5)
        axes[0].annotate('High Risk Zone', xy=(6, 95), fontsize=10, color='red', fontweight='bold')
        
        # Average monthly charges over tenure
        avg_charges = self.df.groupby('tenure_group')['monthly_charges'].mean()
        churn_rate = self.df.groupby('tenure_group')[self.target_col].mean() * 100
        
        x = np.arange(len(avg_charges))
        ax2 = axes[1].twinx()
        
        bars = axes[1].bar(x, avg_charges.values, alpha=0.7, color='#3498db', label='Avg Monthly Charges')
        line = ax2.plot(x, churn_rate.values, 'o-', color='#e74c3c', linewidth=2, markersize=8, label='Churn Rate')
        
        axes[1].set_xlabel('Tenure Group (Months)')
        axes[1].set_ylabel('Average Monthly Charges ($)', color='#3498db')
        ax2.set_ylabel('Churn Rate (%)', color='#e74c3c')
        axes[1].set_xticks(x)
        axes[1].set_xticklabels(avg_charges.index)
        axes[1].set_title('Charges and Churn Rate by Tenure', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('results/visualizations/07_tenure_charges.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def _plot_service_analysis(self):
        """Plot analysis of additional services."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        services = ['Online_Security', 'Online_Backup', 'Device_Protection', 
                   'Tech_Support', 'Streaming_TV', 'Streaming_Movies']
        
        # Service adoption rate
        service_adoption = self.df[services].mean() * 100
        
        colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(services)))
        bars = axes[0].barh([s.replace('_', ' ') for s in services], service_adoption.values, color=colors)
        axes[0].set_xlabel('Adoption Rate (%)')
        axes[0].set_title('Additional Service Adoption Rate', fontsize=12, fontweight='bold')
        
        for bar, val in zip(bars, service_adoption.values):
            axes[0].text(val + 0.5, bar.get_y() + bar.get_height()/2,
                        f'{val:.1f}%', va='center', fontweight='bold')
        
        # Churn rate by service count
        self.df['total_services'] = self.df[services].sum(axis=1)
        service_churn = self.df.groupby('total_services')[self.target_col].mean() * 100
        
        colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(service_churn)))
        bars = axes[1].bar(service_churn.index, service_churn.values, color=colors)
        axes[1].set_xlabel('Number of Additional Services')
        axes[1].set_ylabel('Churn Rate (%)')
        axes[1].set_title('Churn Rate by Number of Additional Services', fontsize=12, fontweight='bold')
        
        for bar, val in zip(bars, service_churn.values):
            axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                        f'{val:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('results/visualizations/08_service_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def _plot_risk_analysis(self):
        """Plot risk tier analysis."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        risk_order = ['Low', 'Medium', 'High', 'Critical']
        
        # Count by risk tier
        risk_counts = self.df['risk_tier'].value_counts().reindex(risk_order)
        colors = ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']
        
        axes[0].pie(risk_counts, labels=risk_counts.index, autopct='%1.1f%%',
                   colors=colors, explode=[0, 0, 0.05, 0.1], shadow=True)
        axes[0].set_title('Customer Distribution by Risk Tier', fontsize=12, fontweight='bold')
        
        # Churn rate by risk tier
        risk_churn = self.df.groupby('risk_tier')[self.target_col].mean().reindex(risk_order) * 100
        
        bars = axes[1].bar(risk_churn.index, risk_churn.values, color=colors)
        axes[1].set_xlabel('Risk Tier')
        axes[1].set_ylabel('Churn Rate (%)')
        axes[1].set_title('Churn Rate by Risk Tier', fontsize=12, fontweight='bold')
        
        for bar, val in zip(bars, risk_churn.values):
            axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                        f'{val:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('results/visualizations/09_risk_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def _plot_segment_analysis(self):
        """Plot customer segment analysis."""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        segment_order = ['New', 'Developing', 'Established', 'Loyal']
        
        # Customer count by segment
        segment_counts = self.df['customer_segment'].value_counts().reindex(segment_order)
        colors = ['#e74c3c', '#f39c12', '#3498db', '#2ecc71']
        
        axes[0, 0].pie(segment_counts, labels=segment_counts.index, autopct='%1.1f%%',
                      colors=colors, explode=[0.1, 0, 0, 0])
        axes[0, 0].set_title('Customer Distribution by Segment', fontsize=12, fontweight='bold')
        
        # Revenue by segment
        segment_revenue = self.df.groupby('customer_segment')['monthly_charges'].sum().reindex(segment_order)
        axes[0, 1].bar(segment_order, segment_revenue.values, color=colors)
        axes[0, 1].set_xlabel('Customer Segment')
        axes[0, 1].set_ylabel('Total Monthly Revenue ($)')
        axes[0, 1].set_title('Monthly Revenue by Customer Segment', fontsize=12, fontweight='bold')
        axes[0, 1].ticklabel_format(style='plain', axis='y')
        
        # Churned customers by segment
        churned_by_segment = self.df[self.df[self.target_col] == 1].groupby('customer_segment').size().reindex(segment_order)
        retained_by_segment = self.df[self.df[self.target_col] == 0].groupby('customer_segment').size().reindex(segment_order)
        
        x = np.arange(len(segment_order))
        width = 0.35
        
        axes[1, 0].bar(x - width/2, retained_by_segment.values, width, label='Retained', color='#2ecc71')
        axes[1, 0].bar(x + width/2, churned_by_segment.values, width, label='Churned', color='#e74c3c')
        axes[1, 0].set_xlabel('Customer Segment')
        axes[1, 0].set_ylabel('Number of Customers')
        axes[1, 0].set_title('Retained vs Churned by Segment', fontsize=12, fontweight='bold')
        axes[1, 0].set_xticks(x)
        axes[1, 0].set_xticklabels(segment_order)
        axes[1, 0].legend()
        
        # Revenue at risk by segment
        revenue_at_risk = self.df[self.df[self.target_col] == 1].groupby('customer_segment')['monthly_charges'].sum().reindex(segment_order)
        axes[1, 1].bar(segment_order, revenue_at_risk.values, color='#e74c3c', alpha=0.7)
        axes[1, 1].set_xlabel('Customer Segment')
        axes[1, 1].set_ylabel('Monthly Revenue at Risk ($)')
        axes[1, 1].set_title('Monthly Revenue at Risk by Segment (Churned)', fontsize=12, fontweight='bold')
        
        for i, val in enumerate(revenue_at_risk.values):
            axes[1, 1].text(i, val + 500, f'${val:,.0f}', ha='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('results/visualizations/10_segment_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def _plot_revenue_impact(self):
        """Plot revenue impact analysis."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Revenue metrics
        total_monthly_revenue = self.df['monthly_charges'].sum()
        churned_revenue = self.df[self.df[self.target_col] == 1]['monthly_charges'].sum()
        retained_revenue = self.df[self.df[self.target_col] == 0]['monthly_charges'].sum()
        
        revenue_data = ['Retained Revenue', 'Churned Revenue']
        revenue_values = [retained_revenue, churned_revenue]
        colors = ['#2ecc71', '#e74c3c']
        
        bars = axes[0].bar(revenue_data, revenue_values, color=colors)
        axes[0].set_ylabel('Monthly Revenue ($)')
        axes[0].set_title('Monthly Revenue: Retained vs Churned', fontsize=12, fontweight='bold')
        
        for bar, val in zip(bars, revenue_values):
            axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2000,
                       f'${val:,.0f}', ha='center', fontweight='bold')
        
        # Churn impact summary
        churn_rate = self.df[self.target_col].mean() * 100
        revenue_loss_pct = churned_revenue / total_monthly_revenue * 100
        
        summary_text = f"""
        CHURN IMPACT SUMMARY
        ────────────────────
        Total Monthly Revenue: ${total_monthly_revenue:,.0f}
        Revenue from Churned: ${churned_revenue:,.0f}
        Revenue Retention Rate: {100-churn_rate:.1f}%
        
        Annual Revenue at Risk: ${churned_revenue * 12:,.0f}
        Customer Churn Rate: {churn_rate:.1f}%
        """
        
        axes[1].text(0.1, 0.5, summary_text, fontsize=11, family='monospace',
                    verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        axes[1].axis('off')
        axes[1].set_title('Financial Impact Summary', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('results/visualizations/11_revenue_impact.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def generate_eda_report(self):
        """Generate complete EDA report."""
        summary = self.generate_summary_statistics()
        churn_analysis = self.analyze_churn_by_segment()
        corr_matrix, churn_corr = self.analyze_correlations()
        test_results = self.statistical_tests()
        self.create_visualizations()
        
        print("\n" + "=" * 80)
        print("EDA COMPLETE")
        print("=" * 80)
        
        return {
            'summary': summary,
            'churn_analysis': churn_analysis,
            'correlations': churn_corr,
            'statistical_tests': test_results
        }


def main():
    """Run complete EDA."""
    df = pd.read_csv('data/customer_data.csv')
    
    eda = ChurnEDA(df)
    report = eda.generate_eda_report()
    
    return report


if __name__ == "__main__":
    main()
