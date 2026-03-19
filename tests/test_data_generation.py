"""
Unit tests for data generation module.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_generation import TelecomDataGenerator


class TestDataGeneration:
    """Test cases for TelecomDataGenerator."""

    def setup_method(self):
        """Setup test fixtures."""
        self.generator = TelecomDataGenerator(n_customers=100, seed=42)

    def test_generator_initialization(self):
        """Test generator initializes correctly."""
        assert self.generator.n_customers == 100

    def test_generate_customer_id(self):
        """Test customer ID generation."""
        ids = self.generator.generate_customer_id(10)
        assert len(ids) == 10
        assert ids[0] == 'CUS0000001'
        assert ids[-1] == 'CUS0000010'

    def test_generate_tenure(self):
        """Test tenure generation."""
        tenure = self.generator.generate_tenure(100)
        assert len(tenure) == 100
        assert tenure.min() >= 0
        assert tenure.max() <= 100

    def test_generate_contract_type(self):
        """Test contract type generation."""
        contracts = self.generator.generate_contract_type(100)
        assert len(contracts) == 100
        assert all(c in ['Month-to-Month', 'One Year', 'Two Year'] for c in contracts)

    def test_generate_internet_service(self):
        """Test internet service generation."""
        services = self.generator.generate_internet_service(100)
        assert len(services) == 100
        assert all(s in ['Fiber Optic', 'DSL', 'No Internet'] for s in services)

    def test_generate_payment_method(self):
        """Test payment method generation."""
        methods = self.generator.generate_payment_method(100)
        assert len(methods) == 100
        expected = ['Electronic Check', 'Bank Transfer (Automatic)', 
                    'Credit Card (Automatic)', 'Mailed Check']
        assert all(m in expected for m in methods)

    def test_generate_monthly_charges(self):
        """Test monthly charges generation."""
        tenure = self.generator.generate_tenure(50)
        contract = self.generator.generate_contract_type(50)
        internet = self.generator.generate_internet_service(50)
        
        charges = self.generator.generate_monthly_charges(tenure, contract, internet)
        assert len(charges) == 50
        assert charges.min() > 0

    def test_generate_total_charges(self):
        """Test total charges calculation."""
        import numpy as np
        tenure = np.array([12, 24, 36])
        monthly = np.array([50.0, 75.0, 100.0])
        total = self.generator.generate_total_charges(tenure, monthly)
        assert len(total) == 3

    def test_generate_additional_services(self):
        """Test additional services generation."""
        services = self.generator.generate_additional_services(100)
        assert 'Online_Security' in services
        assert 'Tech_Support' in services
        assert len(services) == 6

    def test_assign_segment(self):
        """Test customer segment assignment."""
        row_new = {'tenure_months': 6, 'contract_type': 'Month-to-Month'}
        row_developing = {'tenure_months': 24, 'contract_type': 'One Year'}
        row_established = {'tenure_months': 48, 'contract_type': 'Two Year'}
        row_loyal = {'tenure_months': 80, 'contract_type': 'Two Year'}
        
        assert self.generator._assign_segment(row_new) == 'New'
        assert self.generator._assign_segment(row_developing) == 'Developing'
        assert self.generator._assign_segment(row_established) == 'Established'
        assert self.generator._assign_segment(row_loyal) == 'Loyal'

    def test_assign_risk_tier(self):
        """Test risk tier assignment."""
        low_risk = {'tenure_months': 60, 'contract_type': 'Two Year', 
                   'monthly_charges': 50, 'payment_method': 'Credit Card (Automatic)',
                   'Online_Security': 1, 'Online_Backup': 1, 'Tech_Support': 1}
        
        high_risk = {'tenure_months': 6, 'contract_type': 'Month-to-Month',
                    'monthly_charges': 100, 'payment_method': 'Electronic Check',
                    'Online_Security': 0, 'Online_Backup': 0, 'Tech_Support': 0}
        
        risk_low = self.generator._assign_risk_tier(low_risk)
        risk_high = self.generator._assign_risk_tier(high_risk)
        
        assert risk_low == 'Low'
        assert risk_high == 'Critical'

    def test_generate_data(self):
        """Test complete data generation."""
        gen = TelecomDataGenerator(n_customers=200, seed=42)
        df = gen.generate_data()
        
        assert len(df) == 200
        assert 'customer_id' in df.columns
        assert 'churn' in df.columns
        assert df['churn'].isin([0, 1]).all()
        assert 0 <= df['churn'].mean() <= 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
