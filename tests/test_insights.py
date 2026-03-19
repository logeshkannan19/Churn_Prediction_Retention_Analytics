"""
Unit tests for insights module.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_generation import TelecomDataGenerator
from src.insights_recommendations import ChurnInsights


class TestChurnInsights:
    """Test cases for ChurnInsights."""

    def setup_method(self):
        """Setup test fixtures."""
        generator = TelecomDataGenerator(n_customers=500, seed=42)
        self.df = generator.generate_data()
        self.insights = ChurnInsights(self.df)

    def test_calculate_key_metrics(self):
        """Test key metrics calculation."""
        metrics = self.insights.calculate_key_metrics()
        
        assert 'total_customers' in metrics
        assert 'churned_customers' in metrics
        assert 'churn_rate_pct' in metrics
        assert metrics['total_customers'] == 500
        assert metrics['churn_rate_pct'] > 0
        assert metrics['churn_rate_pct'] < 100

    def test_get_segment_analysis(self):
        """Test segment analysis."""
        segments = self.insights.get_segment_analysis()
        
        assert 'New' in segments
        assert 'Developing' in segments
        assert 'Established' in segments
        assert 'Loyal' in segments
        
        for segment in segments.values():
            assert 'count' in segment
            assert 'churn_rate' in segment
            assert 'avg_tenure' in segment

    def test_quantify_insights(self):
        """Test insights quantification."""
        insights = self.insights.quantify_insights()
        
        assert len(insights) > 0
        for insight in insights:
            assert 'category' in insight
            assert 'insight' in insight
            assert 'quantified' in insight
            assert 'impact' in insight

    def test_generate_retention_strategies(self):
        """Test retention strategy generation."""
        strategies = self.insights.generate_retention_strategies()
        
        assert len(strategies) > 0
        for strategy in strategies:
            assert 'name' in strategy
            assert 'target_segment' in strategy
            assert 'actions' in strategy
            assert 'expected_impact' in strategy
            assert 'priority' in strategy

    def test_calculate_roi_projections(self):
        """Test ROI projection calculation."""
        roi = self.insights.calculate_roi_projections()
        
        assert 'baseline_annual_loss' in roi
        assert 'retention_investment_estimate' in roi
        assert 'projections' in roi
        assert roi['baseline_annual_loss'] > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
