"""Tests for budget extraction functionality"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from budget_extraction import extract_budget


class TestExtractBudget(unittest.TestCase):
    """Test cases for extract_budget function"""
    
    def test_empty_input(self):
        """Test with empty/None input"""
        result = extract_budget(None, 0)
        self.assertIsNone(result["budget_value"])
        self.assertIsNone(result["budget_currency"])
        self.assertIsNone(result["budget_text"])
        
        result = extract_budget("", 0)
        self.assertIsNone(result["budget_value"])
        self.assertIsNone(result["budget_currency"])
        self.assertIsNone(result["budget_text"])
    
    def test_basic_dollar_pattern(self):
        """Test basic $X pattern"""
        result = extract_budget("The budget is $1000000", 0)
        self.assertEqual(result["budget_value"], 1000000.0)
        self.assertEqual(result["budget_currency"], "USD")
        self.assertEqual(result["budget_text"], "$1000000")
        
    def test_dollar_with_space(self):
        """Test $ X pattern with space"""
        result = extract_budget("Budget: $ 500000", 0)
        self.assertEqual(result["budget_value"], 500000.0)
        self.assertEqual(result["budget_currency"], "USD")
        
    def test_usd_prefix(self):
        """Test USD X pattern"""
        result = extract_budget("Cost is USD 2000000", 0)
        self.assertEqual(result["budget_value"], 2000000.0)
        self.assertEqual(result["budget_currency"], "USD")
        self.assertEqual(result["budget_text"], "USD 2000000")
        
    def test_usd_suffix(self):
        """Test X USD pattern"""
        result = extract_budget("Budget: 3000000 USD", 0)
        self.assertEqual(result["budget_value"], 3000000.0)
        self.assertEqual(result["budget_currency"], "USD")
        self.assertEqual(result["budget_text"], "3000000 USD")
        
    def test_k_suffix(self):
        """Test k suffix normalization"""
        result = extract_budget("Budget is $50k", 0)
        self.assertEqual(result["budget_value"], 50000.0)
        self.assertEqual(result["budget_currency"], "USD")
        
        result = extract_budget("Budget is $100K", 0)
        self.assertEqual(result["budget_value"], 100000.0)
        
    def test_m_suffix(self):
        """Test m suffix normalization"""
        result = extract_budget("Budget is $1.5m", 0)
        self.assertEqual(result["budget_value"], 1500000.0)
        self.assertEqual(result["budget_currency"], "USD")
        
        result = extract_budget("Budget is $2M", 0)
        self.assertEqual(result["budget_value"], 2000000.0)
        
    def test_comma_removal(self):
        """Test that commas are removed"""
        result = extract_budget("Budget: $1,000,000", 0)
        self.assertEqual(result["budget_value"], 1000000.0)
        self.assertEqual(result["budget_currency"], "USD")
        
    def test_multiple_matches_largest_wins(self):
        """Test that largest value is returned when multiple matches"""
        result = extract_budget("Ranges from $50000 to $200000", 0)
        self.assertEqual(result["budget_value"], 200000.0)
        self.assertEqual(result["budget_currency"], "USD")
        
    def test_range_pattern(self):
        """Test range pattern X-Y"""
        result = extract_budget("Budget: $50k-$200k", 0)
        # Should extract the larger value from the range
        self.assertEqual(result["budget_value"], 200000.0)
        self.assertEqual(result["budget_currency"], "USD")
        
    def test_small_purchase_phrase(self):
        """Test small purchase phrase detection"""
        result = extract_budget("This is a small purchase", 0)
        self.assertIsNone(result["budget_value"])
        self.assertEqual(result["budget_currency"], "USD")
        self.assertEqual(result["budget_text"], "indicated small/under threshold")
        
    def test_under_threshold_phrase(self):
        """Test under threshold phrase detection"""
        result = extract_budget("under $50k budget", 0)
        self.assertIsNone(result["budget_value"])
        self.assertEqual(result["budget_currency"], "USD")
        self.assertEqual(result["budget_text"], "indicated small/under threshold")
        
    def test_not_to_exceed_phrase(self):
        """Test not to exceed phrase detection"""
        result = extract_budget("not to exceed budget limits", 0)
        self.assertIsNone(result["budget_value"])
        self.assertEqual(result["budget_currency"], "USD")
        self.assertEqual(result["budget_text"], "indicated small/under threshold")
        
    def test_no_budget_found(self):
        """Test when no budget is found"""
        result = extract_budget("This is just some text without any budget", 0)
        self.assertIsNone(result["budget_value"])
        self.assertIsNone(result["budget_currency"])
        self.assertIsNone(result["budget_text"])
        
    def test_decimal_values(self):
        """Test decimal budget values"""
        result = extract_budget("Budget: $1500.50", 0)
        self.assertEqual(result["budget_value"], 1500.50)
        self.assertEqual(result["budget_currency"], "USD")
        
    def test_decimal_with_suffix(self):
        """Test decimal with k/m suffix"""
        result = extract_budget("Budget: $1.5m", 0)
        self.assertEqual(result["budget_value"], 1500000.0)
        self.assertEqual(result["budget_currency"], "USD")
        
    def test_min_budget_config_parameter(self):
        """Test that min_budget_config parameter is accepted"""
        # The function should accept this parameter even if not used in logic
        result = extract_budget("Budget: $100000", 50000)
        self.assertEqual(result["budget_value"], 100000.0)
        self.assertEqual(result["budget_currency"], "USD")


if __name__ == '__main__':
    unittest.main()
