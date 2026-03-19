"""
Feature Engineering Module
===========================
Creates meaningful features for churn prediction model:
- Tenure segmentation
- Contract-type grouping
- Charge-based features
- Service-based features
- Risk scoring
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder


class FeatureEngineer:
    """
    Feature engineering pipeline for churn prediction.
    
    Created Features:
    1. Tenure Segments: Categorize customers by tenure (new, mid, long-term)
    2. Charge Buckets: Group monthly charges into meaningful ranges
    3. Service Count: Total number of additional services
    4. Contract-Risk Score: Risk score based on contract type
    5. Revenue Metrics: Customer lifetime value, revenue per month
    6. Interaction Features: Combined features for better prediction
    """
    
    def __init__(self, df):
        self.df = df.copy()
        self.label_encoders = {}
        self.scaler = StandardScaler()
        
    def create_tenure_features(self):
        """
        Create tenure-based features.
        
        Why Important:
        - Tenure is the strongest predictor of churn
        - New customers (<12 months) have highest churn risk
        - Longer tenure indicates customer commitment
        """
        # Tenure groups
        self.df['tenure_group'] = pd.cut(
            self.df['tenure_months'],
            bins=[0, 12, 24, 48, 72, 100],
            labels=['New (0-12)', 'Early (13-24)', 'Mid (25-48)', 
                   'Established (49-72)', 'Loyal (73+)']
        )
        
        # Binary tenure flags
        self.df['is_new_customer'] = (self.df['tenure_months'] <= 12).astype(int)
        self.df['is_long_tenure'] = (self.df['tenure_months'] >= 48).astype(int)
        self.df['is_mid_tenure'] = ((self.df['tenure_months'] > 12) & 
                                   (self.df['tenure_months'] < 48)).astype(int)
        
        # Tenure satisfaction ratio
        self.df['tenure_to_satisfaction'] = self.df['tenure_months'] / self.df['satisfaction_score']
        
        return self
        
    def create_charge_features(self):
        """
        Create charge-based features.
        
        Why Important:
        - High monthly charges correlate with higher churn
        - Price sensitivity varies by customer segment
        - Total charges indicate customer lifetime value
        """
        # Monthly charge buckets
        self.df['charge_bucket'] = pd.cut(
            self.df['monthly_charges'],
            bins=[0, 35, 55, 75, 100, 200],
            labels=['Budget (<$35)', 'Standard ($35-55)', 
                   'Premium ($55-75)', 'High ($75-100)', 'Premium+ ($100+)']
        )
        
        # Charge per tenure month (average monthly spending)
        self.df['avg_monthly_spend'] = np.where(
            self.df['tenure_months'] > 0,
            self.df['total_charges'] / self.df['tenure_months'],
            self.df['monthly_charges']
        )
        
        # Is high-value customer
        self.df['is_high_value'] = (self.df['monthly_charges'] > 80).astype(int)
        
        # Is budget customer
        self.df['is_budget'] = (self.df['monthly_charges'] < 40).astype(int)
        
        # Charge volatility (difference between actual and average)
        self.df['charge_volatility'] = abs(self.df['monthly_charges'] - self.df['avg_monthly_spend'])
        
        return self
        
    def create_contract_features(self):
        """
        Create contract-type features.
        
        Why Important:
        - Month-to-month contracts have highest churn (no commitment)
        - Long-term contracts lock customers in
        - Contract type indicates customer commitment level
        """
        # Contract risk score (higher = more churn risk)
        contract_risk = {
            'Month-to-Month': 3,
            'One Year': 2,
            'Two Year': 1
        }
        self.df['contract_risk_score'] = self.df['contract_type'].map(contract_risk)
        
        # Is month-to-month
        self.df['is_monthly_contract'] = (self.df['contract_type'] == 'Month-to-Month').astype(int)
        
        # Is long-term contract
        self.df['is_long_term_contract'] = (self.df['contract_type'].isin(['One Year', 'Two Year'])).astype(int)
        
        return self
        
    def create_service_features(self):
        """
        Create service-related features.
        
        Why Important:
        - More services = higher engagement = lower churn
        - Streaming services indicate entertainment dependency
        - Tech support/security indicate value placed on service quality
        """
        services = ['Online_Security', 'Online_Backup', 'Device_Protection',
                   'Tech_Support', 'Streaming_TV', 'Streaming_Movies']
        
        # Total services count
        self.df['total_services'] = self.df[services].sum(axis=1)
        
        # Has core services (security, backup, support)
        self.df['has_core_services'] = (
            (self.df['Online_Security'] == 1) | 
            (self.df['Online_Backup'] == 1) | 
            (self.df['Tech_Support'] == 1)
        ).astype(int)
        
        # Has streaming services
        self.df['has_streaming'] = (
            (self.df['Streaming_TV'] == 1) | 
            (self.df['Streaming_Movies'] == 1)
        ).astype(int)
        
        # Has all services (highly engaged)
        self.df['is_fully_engaged'] = (self.df['total_services'] >= 5).astype(int)
        
        # Has no services (high churn risk)
        self.df['has_no_additional'] = (self.df['total_services'] == 0).astype(int)
        
        # Services per month of tenure (engagement rate)
        self.df['service_engagement_rate'] = np.where(
            self.df['tenure_months'] > 0,
            self.df['total_services'] / (self.df['tenure_months'] / 12),
            self.df['total_services']
        )
        
        return self
        
    def create_internet_features(self):
        """
        Create internet service features.
        
        Why Important:
        - Fiber optic users may have different satisfaction patterns
        - No internet service = phone-only customers (different profile)
        """
        # Is fiber optic user
        self.df['is_fiber'] = (self.df['internet_service'] == 'Fiber Optic').astype(int)
        
        # Is DSL user
        self.df['is_dsl'] = (self.df['internet_service'] == 'DSL').astype(int)
        
        # No internet service
        self.df['is_phone_only'] = (self.df['internet_service'] == 'No Internet').astype(int)
        
        return self
        
    def create_payment_features(self):
        """
        Create payment method features.
        
        Why Important:
        - Electronic check users show higher churn rates
        - Auto-pay customers more likely to stay (convenience factor)
        - Mailed check indicates older/different demographic
        """
        # Is electronic check (high churn risk)
        self.df['is_electronic_check'] = (self.df['payment_method'] == 'Electronic Check').astype(int)
        
        # Is automatic payment (lower churn)
        self.df['is_auto_pay'] = self.df['payment_method'].isin(
            ['Bank Transfer (Automatic)', 'Credit Card (Automatic)']
        ).astype(int)
        
        # Payment risk score
        payment_risk = {
            'Electronic Check': 3,
            'Mailed Check': 2,
            'Bank Transfer (Automatic)': 1,
            'Credit Card (Automatic)': 1
        }
        self.df['payment_risk_score'] = self.df['payment_method'].map(payment_risk)
        
        return self
        
    def create_interaction_features(self):
        """
        Create interaction features (combinations of multiple variables).
        
        Why Important:
        - Combined risk factors are stronger predictors
        - New + Month-to-Month + High Charges = Critical risk
        - Captures non-linear relationships
        """
        # High risk combination: New customer + Month-to-Month + High charges
        self.df['high_risk_new'] = (
            (self.df['tenure_months'] <= 12) & 
            (self.df['contract_type'] == 'Month-to-Month') & 
            (self.df['monthly_charges'] > 70)
        ).astype(int)
        
        # Very high risk: Month-to-Month + Electronic Check
        self.df['risky_contract_payment'] = (
            (self.df['contract_type'] == 'Month-to-Month') & 
            (self.df['payment_method'] == 'Electronic Check')
        ).astype(int)
        
        # Value customer: Long tenure + High charges + Long contract
        self.df['value_customer'] = (
            (self.df['tenure_months'] >= 36) & 
            (self.df['monthly_charges'] > 60) &
            (self.df['contract_type'].isin(['One Year', 'Two Year']))
        ).astype(int)
        
        # At-risk value: High charges but no additional services
        self.df['at_risk_value'] = (
            (self.df['monthly_charges'] > 70) & 
            (self.df['total_services'] < 2)
        ).astype(int)
        
        # Engaged streamer: Has streaming + good tenure
        self.df['engaged_streamer'] = (
            (self.df['has_streaming'] == 1) & 
            (self.df['tenure_months'] >= 24)
        ).astype(int)
        
        return self
        
    def create_revenue_features(self):
        """
        Create revenue/value-based features.
        
        Why Important:
        - Customer Lifetime Value (CLV) is key business metric
        - Helps prioritize retention efforts by revenue impact
        """
        # Estimated customer lifetime value (assuming 36-month avg lifetime)
        avg_monthly_revenue = self.df['monthly_charges'].mean()
        self.df['estimated_clv'] = self.df['monthly_charges'] * 36
        
        # Revenue at risk (for churned customers)
        self.df['revenue_at_risk'] = self.df['monthly_charges'] * 12  # Annual
        
        # Tenure value (total revenue from customer)
        self.df['tenure_value'] = self.df['total_charges']
        
        return self
        
    def create_risk_score(self):
        """
        Create composite risk score.
        
        Why Important:
        - Single metric to identify high-risk customers
        - Combines multiple risk factors
        - Useful for prioritization
        """
        risk_score = 0
        
        # Tenure risk
        risk_score += np.where(self.df['tenure_months'] <= 6, 3,
                     np.where(self.df['tenure_months'] <= 12, 2,
                     np.where(self.df['tenure_months'] <= 24, 1, 0)))
        
        # Contract risk
        risk_score += self.df['contract_risk_score'] - 1
        
        # Payment risk
        risk_score += np.where(self.df['payment_method'] == 'Electronic Check', 2,
                     np.where(self.df['payment_method'] == 'Mailed Check', 1, 0))
        
        # Service engagement (protective)
        risk_score -= np.where(self.df['total_services'] >= 4, 2,
                      np.where(self.df['total_services'] >= 2, 1, 0))
        
        # Charge risk
        risk_score += np.where(self.df['monthly_charges'] > 90, 2,
                     np.where(self.df['monthly_charges'] > 70, 1, 0))
        
        # Satisfaction risk
        risk_score += np.where(self.df['satisfaction_score'] < 4, 2,
                     np.where(self.df['satisfaction_score'] < 6, 1, 0))
        
        self.df['composite_risk_score'] = risk_score
        
        # Risk tier
        self.df['risk_tier_calculated'] = pd.cut(
            risk_score,
            bins=[-10, 0, 2, 4, 10],
            labels=['Very Low', 'Low', 'Medium', 'High']
        )
        
        return self
        
    def encode_categorical_features(self):
        """
        Encode categorical features for ML models.
        
        Methods:
        - Label Encoding for ordinal features
        - One-Hot Encoding for nominal features
        """
        # Label encoding for ordinal features
        tenure_order = {'New (0-12)': 0, 'Early (13-24)': 1, 'Mid (25-48)': 2, 
                       'Established (49-72)': 3, 'Loyal (73+)': 4}
        self.df['tenure_group_encoded'] = self.df['tenure_group'].map(tenure_order)
        
        charge_order = {'Budget (<$35)': 0, 'Standard ($35-55)': 1, 
                        'Premium ($55-75)': 2, 'High ($75-100)': 3, 
                        'Premium+ ($100+)': 4}
        self.df['charge_bucket_encoded'] = self.df['charge_bucket'].map(charge_order)
        
        contract_order = {'Month-to-Month': 0, 'One Year': 1, 'Two Year': 2}
        self.df['contract_type_encoded'] = self.df['contract_type'].map(contract_order)
        
        # One-hot encoding for nominal features
        self.df = pd.get_dummies(self.df, columns=['internet_service', 'payment_method'],
                                 drop_first=False)
        
        return self
        
    def create_final_featureset(self):
        """
        Create final feature set for modeling.
        
        Returns DataFrame with:
        - All original features
        - All engineered features
        - Proper encoding
        """
        # Apply all feature engineering steps
        self.create_tenure_features()
        self.create_charge_features()
        self.create_contract_features()
        self.create_service_features()
        self.create_internet_features()
        self.create_payment_features()
        self.create_interaction_features()
        self.create_revenue_features()
        self.create_risk_score()
        self.encode_categorical_features()
        
        # Define final feature columns for modeling
        feature_columns = [
            # Original numeric
            'tenure_months', 'monthly_charges', 'total_charges', 'satisfaction_score',
            
            # Engineered numeric
            'avg_monthly_spend', 'charge_volatility', 'total_services',
            'service_engagement_rate', 'estimated_clv', 'revenue_at_risk', 'tenure_value',
            'composite_risk_score',
            
            # Binary flags
            'is_new_customer', 'is_long_tenure', 'is_mid_tenure',
            'is_high_value', 'is_budget', 'is_monthly_contract', 'is_long_term_contract',
            'has_core_services', 'has_streaming', 'is_fully_engaged', 'has_no_additional',
            'is_fiber', 'is_dsl', 'is_phone_only',
            'is_electronic_check', 'is_auto_pay',
            'high_risk_new', 'risky_contract_payment', 'value_customer', 
            'at_risk_value', 'engaged_streamer',
            
            # Encoded categorical
            'tenure_group_encoded', 'charge_bucket_encoded', 'contract_type_encoded',
            
            # Service flags
            'Online_Security', 'Online_Backup', 'Device_Protection',
            'Tech_Support', 'Streaming_TV', 'Streaming_Movies',
            
            # One-hot encoded
            'internet_service_DSL', 'internet_service_Fiber Optic', 
            'internet_service_No Internet',
            'payment_method_Bank Transfer (Automatic)', 
            'payment_method_Credit Card (Automatic)',
            'payment_method_Electronic Check', 'payment_method_Mailed Check'
        ]
        
        # Keep only columns that exist
        available_features = [col for col in feature_columns if col in self.df.columns]
        
        return self.df[available_features]
    
    def get_feature_importance_guide(self):
        """
        Return feature importance guide explaining each feature.
        """
        guide = """
        FEATURE IMPORTANCE GUIDE FOR CHURN PREDICTION
        =============================================
        
        HIGH IMPACT FEATURES:
        1. tenure_months - Strongest predictor; longer tenure = lower churn
        2. contract_type_encoded - Month-to-month contracts have 3x higher churn
        3. is_electronic_check - Electronic check users churn 40% more
        4. total_services - More services = higher engagement = lower churn
        5. composite_risk_score - Combined risk metric
        
        MEDIUM IMPACT FEATURES:
        6. monthly_charges - Higher charges correlate with higher churn
        7. satisfaction_score - Lower satisfaction = higher churn probability
        8. is_new_customer - Customers <12 months have highest churn risk
        9. has_core_services - Security/backup/support reduce churn
        10. high_risk_new - Interaction: new + monthly + high charges
        
        CONTEXTUAL FEATURES:
        11. is_fiber - Fiber users have different churn patterns
        12. has_streaming - Streamers may have entertainment dependency
        13. risky_contract_payment - Monthly + electronic check combo
        14. value_customer - High-value long-term customers
        15. at_risk_value - High payer without services (dissatisfied?)
        
        WHY THESE FEATURES MATTER:
        - Commitment = Loyalty: Long-term contracts reduce churn
        - Engagement = Retention: More services = stickier product
        - Price Sensitivity: High charges cause price-sensitive churn
        - Convenience = Stay: Auto-pay reduces friction/churn
        """
        return guide


def main():
    """Run feature engineering on customer data."""
    df = pd.read_csv('data/customer_data.csv')
    
    engineer = FeatureEngineer(df)
    features = engineer.create_final_featureset()
    
    # Save engineered features
    features.to_csv('data/engineered_features.csv', index=False)
    
    print(f"Feature engineering complete!")
    print(f"Original features: {len(df.columns)}")
    print(f"Engineered features: {len(features.columns)}")
    print(f"\nFeature importance guide:")
    print(engineer.get_feature_importance_guide())
    
    return features


if __name__ == "__main__":
    features = main()
