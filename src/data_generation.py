"""
Data Generation Module
======================
Generates synthetic telecom customer data with realistic patterns
for churn prediction analysis.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class TelecomDataGenerator:
    """
    Generates synthetic telecom customer dataset with realistic churn patterns.
    
    Key Churn Drivers (based on industry research):
    - Short tenure customers have higher churn rates
    - Month-to-month contracts have highest churn
    - High monthly charges increase churn probability
    - Fiber optic users may have different patterns
    - Electronic check payment users show higher churn
    - Customers without additional services more likely to churn
    """
    
    def __init__(self, n_customers=7500, seed=42):
        self.n_customers = n_customers
        np.random.seed(seed)
        random.seed(seed)
        
    def generate_customer_id(self, n):
        """Generate unique customer IDs."""
        return [f'CUS{str(i).zfill(7)}' for i in range(1, n + 1)]
    
    def generate_tenure(self, n):
        """
        Generate tenure in months with realistic distribution.
        Weighted toward newer customers (industry typical).
        """
        tenure_distribution = [
            (0, 12, 0.25),      # New customers (0-12 months): 25%
            (13, 24, 0.20),     # Early-mid tenure: 20%
            (25, 48, 0.30),     # Mid-term: 30%
            (49, 72, 0.15),     # Long-term: 15%
            (73, 100, 0.10)     # Very long-term: 10%
        ]
        
        tenures = []
        for low, high, weight in tenure_distribution:
            count = int(n * weight)
            tenures.extend(np.random.randint(low, high + 1, count))
        
        while len(tenures) < n:
            for low, high, _ in tenure_distribution:
                if len(tenures) < n:
                    tenures.append(np.random.randint(low, high + 1))
        
        return np.array(tenures[:n])
    
    def generate_contract_type(self, n):
        """Generate contract type with industry-standard distribution."""
        contracts = np.random.choice(
            ['Month-to-Month', 'One Year', 'Two Year'],
            n,
            p=[0.55, 0.25, 0.20]  # 55% month-to-month is industry typical
        )
        return contracts
    
    def generate_internet_service(self, n):
        """Generate internet service type."""
        services = np.random.choice(
            ['Fiber Optic', 'DSL', 'No Internet'],
            n,
            p=[0.45, 0.35, 0.20]
        )
        return services
    
    def generate_payment_method(self, n):
        """Generate payment method."""
        methods = np.random.choice(
            ['Electronic Check', 'Bank Transfer (Automatic)', 
             'Credit Card (Automatic)', 'Mailed Check'],
            n,
            p=[0.35, 0.25, 0.25, 0.15]
        )
        return methods
    
    def generate_monthly_charges(self, tenure, contract_type, internet_service):
        """
        Generate monthly charges based on services and tenure.
        Base charges + service add-ons + tenure-based pricing.
        """
        charges = np.zeros(len(tenure))
        
        for i, service in enumerate(internet_service):
            if service == 'No Internet':
                charges[i] = np.random.uniform(25, 40)
            elif service == 'DSL':
                charges[i] = np.random.uniform(40, 60)
            else:
                charges[i] = np.random.uniform(60, 110)
        
        additional_services = np.random.randint(0, 4, len(tenure))
        charges += additional_services * np.random.uniform(5, 15, len(tenure))
        
        tenure_factor = 1 - (tenure / 200) * 0.15
        charges = charges * np.clip(tenure_factor, 0.85, 1.0)
        
        return np.round(charges, 2)
    
    def generate_total_charges(self, tenure, monthly_charges):
        """Calculate total charges based on tenure and monthly charges."""
        # Add some variance to make it realistic
        variance = np.random.uniform(0.95, 1.05, len(tenure))
        return np.round(monthly_charges * tenure * variance, 2)
    
    def generate_additional_services(self, n):
        """Generate binary flags for additional services."""
        return {
            'Online_Security': np.random.choice([0, 1], n, p=[0.65, 0.35]),
            'Online_Backup': np.random.choice([0, 1], n, p=[0.60, 0.40]),
            'Device_Protection': np.random.choice([0, 1], n, p=[0.58, 0.42]),
            'Tech_Support': np.random.choice([0, 1], n, p=[0.62, 0.38]),
            'Streaming_TV': np.random.choice([0, 1], n, p=[0.45, 0.55]),
            'Streaming_Movies': np.random.choice([0, 1], n, p=[0.45, 0.55])
        }
    
    def generate_churn_label(self, tenure, contract_type, monthly_charges, 
                            payment_method, internet_service, additional_services):
        """
        Generate churn label based on multiple risk factors.
        This creates realistic churn patterns observed in telecom industry.
        """
        n = len(tenure)
        churn_probability = np.zeros(n)
        
        # Factor 1: Tenure (strong predictor) - tuned for ~26% overall churn
        churn_probability += np.where(tenure < 12, 0.18,
                            np.where(tenure < 24, 0.12,
                            np.where(tenure < 48, 0.06,
                            np.where(tenure < 72, 0.03, 0.01))))
        
        # Factor 2: Contract Type (strong predictor)
        churn_probability += np.where(contract_type == 'Month-to-Month', 0.14,
                            np.where(contract_type == 'One Year', 0.04, 0.01))
        
        # Factor 3: Monthly Charges (higher charges = higher churn risk)
        charge_normalized = (monthly_charges - 30) / 100
        churn_probability += charge_normalized * 0.10
        
        # Factor 4: Payment Method (electronic check users churn more)
        churn_probability += np.where(payment_method == 'Electronic Check', 0.10,
                            np.where(payment_method == 'Mailed Check', 0.04, 0.01))
        
        # Factor 5: Internet Service Type
        churn_probability += np.where(internet_service == 'Fiber Optic', 0.05,
                            np.where(internet_service == 'DSL', 0.02, -0.01))
        
        # Factor 6: Number of additional services (protective factor)
        total_services = sum(additional_services.values()) / 6
        churn_probability -= total_services * 0.07
        
        # Factor 7: Interaction - New + Month-to-Month + High Charges (very high risk)
        high_risk_mask = (tenure < 12) & (contract_type == 'Month-to-Month') & (monthly_charges > 70)
        churn_probability[high_risk_mask] += 0.10
        
        # Convert probability to binary churn
        churn_labels = (np.random.random(n) < churn_probability).astype(int)
        
        return churn_labels
    
    def generate_satisfaction_score(self, churn_label, tenure, additional_services):
        """
        Generate satisfaction score (1-10) - influenced by churn status.
        """
        base_score = 7 + np.random.randn(len(tenure)) * 1.5
        
        base_score = np.where(churn_label == 1, base_score - 2, base_score)
        
        base_score += tenure / 50
        
        total_services = sum([additional_services[key] for key in additional_services])
        base_score += total_services / 12
        
        return np.clip(np.round(base_score, 1), 1, 10)
    
    def generate_data(self):
        """Generate complete customer dataset."""
        print(f"Generating {self.n_customers:,} customer records...")
        
        # Generate base features
        customer_ids = self.generate_customer_id(self.n_customers)
        tenure = self.generate_tenure(self.n_customers)
        contract_type = self.generate_contract_type(self.n_customers)
        internet_service = self.generate_internet_service(self.n_customers)
        payment_method = self.generate_payment_method(self.n_customers)
        
        # Generate charges
        monthly_charges = self.generate_monthly_charges(
            tenure, contract_type, internet_service
        )
        total_charges = self.generate_total_charges(tenure, monthly_charges)
        
        # Generate additional services
        additional_services = self.generate_additional_services(self.n_customers)
        
        # Generate churn label (depends on other features)
        churn_labels = self.generate_churn_label(
            tenure, contract_type, monthly_charges,
            payment_method, internet_service, additional_services
        )
        
        # Generate satisfaction score
        satisfaction_scores = self.generate_satisfaction_score(
            churn_labels, tenure, additional_services
        )
        
        # Assemble DataFrame
        df = pd.DataFrame({
            'customer_id': customer_ids,
            'tenure_months': tenure,
            'contract_type': contract_type,
            'internet_service': internet_service,
            'payment_method': payment_method,
            'monthly_charges': monthly_charges,
            'total_charges': total_charges,
            **additional_services,
            'churn': churn_labels,
            'satisfaction_score': satisfaction_scores
        })
        
        # Add date features
        reference_date = datetime(2025, 1, 1)
        df['account_creation_date'] = [
            reference_date - timedelta(days=int(t * 30.44)) 
            for t in df['tenure_months']
        ]
        df['last_activity_date'] = [
            reference_date - timedelta(days=random.randint(0, 30))
            for _ in range(len(df))
        ]
        
        # Add customer segment
        df['customer_segment'] = df.apply(self._assign_segment, axis=1)
        
        # Add risk tier
        df['risk_tier'] = df.apply(self._assign_risk_tier, axis=1)
        
        print(f"Dataset generated: {len(df):,} records")
        print(f"Overall churn rate: {df['churn'].mean()*100:.2f}%")
        
        return df
    
    def _assign_segment(self, row):
        """Assign customer segment based on tenure and contract."""
        if row['tenure_months'] <= 12:
            return 'New'
        elif row['tenure_months'] <= 36:
            return 'Developing'
        elif row['tenure_months'] <= 60:
            return 'Established'
        else:
            return 'Loyal'
    
    def _assign_risk_tier(self, row):
        """Assign risk tier based on churn probability factors."""
        score = 0
        
        if row['tenure_months'] < 12:
            score += 2
        elif row['tenure_months'] < 24:
            score += 1
            
        if row['contract_type'] == 'Month-to-Month':
            score += 2
        elif row['contract_type'] == 'One Year':
            score += 1
            
        if row['monthly_charges'] > 80:
            score += 1
            
        if row['payment_method'] == 'Electronic Check':
            score += 1
            
        if sum([row['Online_Security'], row['Online_Backup'], 
                row['Tech_Support']]) < 2:
            score += 1
            
        if score >= 6:
            return 'Critical'
        elif score >= 4:
            return 'High'
        elif score >= 2:
            return 'Medium'
        else:
            return 'Low'
    
    def save_data(self, df, filepath='data/customer_data.csv'):
        """Save dataset to CSV."""
        df.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")
        return filepath


def main():
    """Generate and save the telecom customer dataset."""
    generator = TelecomDataGenerator(n_customers=7500)
    df = generator.generate_data()
    
    # Save to data directory
    output_path = generator.save_data(df, 'data/customer_data.csv')
    
    # Also create a processed version for ML
    df_processed = df.copy()
    df_processed.to_csv('data/customer_data_processed.csv', index=False)
    
    return df


if __name__ == "__main__":
    df = main()
    print(f"\nDataset shape: {df.shape}")
    print(f"\nColumn overview:\n{df.dtypes}")
