"""
Test suite for OptionPricer class

This module tests the OptionPricer functionality including:
- Input validation
- Option symbol creation
- Error handling
- Data parsing
"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from option_pricer import OptionPricer, OptionPricingData


class TestOptionPricer(unittest.TestCase):
    """Test cases for OptionPricer class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.pricer = OptionPricer(use_paper_trading=True)
    
    def test_input_validation_valid_inputs(self):
        """Test input validation with valid inputs"""
        future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        result = self.pricer._validate_inputs('SPY', 500.0, 'call', future_date)
        self.assertIsNone(result, "Valid inputs should pass validation")
        
        result = self.pricer._validate_inputs('QQQ', 100.0, 'put', future_date)
        self.assertIsNone(result, "Valid inputs should pass validation")
    
    def test_input_validation_invalid_symbol(self):
        """Test input validation with invalid symbols"""
        future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        result = self.pricer._validate_inputs('', 500.0, 'call', future_date)
        self.assertIsNotNone(result)
        self.assertIn('Symbol must be a non-empty string', result)
        
        result = self.pricer._validate_inputs(None, 500.0, 'call', future_date)
        self.assertIsNotNone(result)
        self.assertIn('Symbol must be a non-empty string', result)
        
        result = self.pricer._validate_inputs('SPY123', 500.0, 'call', future_date)
        self.assertIsNotNone(result)
        self.assertIn('Invalid symbol format', result)
    
    def test_input_validation_invalid_strike(self):
        """Test input validation with invalid strikes"""
        future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        result = self.pricer._validate_inputs('SPY', -100.0, 'call', future_date)
        self.assertIsNotNone(result)
        self.assertIn('Strike must be positive', result)
        
        result = self.pricer._validate_inputs('SPY', 0, 'call', future_date)
        self.assertIsNotNone(result)
        self.assertIn('Strike must be positive', result)
        
        result = self.pricer._validate_inputs('SPY', 'invalid', 'call', future_date)
        self.assertIsNotNone(result)
        self.assertIn('Strike must be a number', result)
        
        result = self.pricer._validate_inputs('SPY', 50000.0, 'call', future_date)
        self.assertIsNotNone(result)
        self.assertIn('Strike seems unreasonably high', result)
    
    def test_input_validation_invalid_option_type(self):
        """Test input validation with invalid option types"""
        future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        result = self.pricer._validate_inputs('SPY', 500.0, 'invalid', future_date)
        self.assertIsNotNone(result)
        self.assertIn("Option type must be 'call' or 'put'", result)
        
        result = self.pricer._validate_inputs('SPY', 500.0, '', future_date)
        self.assertIsNotNone(result)
        self.assertIn('Option type must be a non-empty string', result)
        
        result = self.pricer._validate_inputs('SPY', 500.0, None, future_date)
        self.assertIsNotNone(result)
        self.assertIn('Option type must be a non-empty string', result)
    
    def test_input_validation_invalid_expiration_date(self):
        """Test input validation with invalid expiration dates"""
        result = self.pricer._validate_inputs('SPY', 500.0, 'call', 'invalid-date')
        self.assertIsNotNone(result)
        self.assertIn('Invalid expiration date format', result)
        
        past_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        result = self.pricer._validate_inputs('SPY', 500.0, 'call', past_date)
        self.assertIsNotNone(result)
        self.assertIn('Expiration date cannot be in the past', result)
        
        result = self.pricer._validate_inputs('SPY', 500.0, 'call', '')
        self.assertIsNotNone(result)
        self.assertIn('Expiration date must be a non-empty string', result)
    
    def test_create_option_symbol_valid(self):
        """Test option symbol creation with valid inputs"""
        future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        exp_date = datetime.strptime(future_date, '%Y-%m-%d')
        date_str = exp_date.strftime('%y%m%d')
        
        symbol = self.pricer._create_option_symbol('SPY', 500.0, 'call', future_date)
        expected_symbol = f'SPY{date_str}C00500000'
        self.assertEqual(symbol, expected_symbol)
        
        symbol = self.pricer._create_option_symbol('SPY', 500.0, 'put', future_date)
        expected_symbol = f'SPY{date_str}P00500000'
        self.assertEqual(symbol, expected_symbol)
        
        symbol = self.pricer._create_option_symbol('SPY', 450.5, 'call', future_date)
        expected_symbol = f'SPY{date_str}C00450500'
        self.assertEqual(symbol, expected_symbol)
    
    def test_create_option_symbol_invalid(self):
        """Test option symbol creation with invalid inputs"""
        future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        with self.assertRaises(ValueError):
            self.pricer._create_option_symbol('SPY', -100.0, 'call', future_date)
        
        with self.assertRaises(ValueError):
            self.pricer._create_option_symbol('SPY', 500.0, 'call', 'invalid-date')
    
    def test_calculate_target_strikes(self):
        """Test target strike calculation"""
        strikes = self.pricer.calculate_target_strikes(500.0, 510.0, 490.0, 0.1)
        
        expected_put_strike = 490.0 * (1 - 0.1)  # 441.0
        expected_call_strike = 510.0 * (1 + 0.1)  # 561.0
        
        self.assertEqual(strikes['put_strike'], expected_put_strike)
        self.assertEqual(strikes['call_strike'], expected_call_strike)
        self.assertEqual(strikes['current_price'], 500.0)
        self.assertEqual(strikes['orh'], 510.0)
        self.assertEqual(strikes['orl'], 490.0)
    
    def test_fetch_option_pricing_invalid_inputs(self):
        """Test fetch_option_pricing with invalid inputs"""
        future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        result = self.pricer.fetch_option_pricing('', 500.0, 'call', future_date)
        self.assertIsNone(result)
        
        result = self.pricer.fetch_option_pricing('SPY', -100.0, 'call', future_date)
        self.assertIsNone(result)
        
        result = self.pricer.fetch_option_pricing('SPY', 500.0, 'invalid', future_date)
        self.assertIsNone(result)
        
        result = self.pricer.fetch_option_pricing('SPY', 500.0, 'call', 'invalid-date')
        self.assertIsNone(result)
    
    @patch('option_pricer.OptionPricer._fetch_option_bars')
    def test_fetch_option_pricing_no_data(self, mock_fetch_bars):
        """Test fetch_option_pricing when no data is returned"""
        future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        mock_fetch_bars.return_value = None
        
        result = self.pricer.fetch_option_pricing('SPY', 500.0, 'call', future_date)
        self.assertIsNone(result)
    
    @patch('option_pricer.OptionPricer._fetch_option_bars')
    @patch('option_pricer.OptionPricer._parse_option_data')
    def test_fetch_option_pricing_parse_failure(self, mock_parse_data, mock_fetch_bars):
        """Test fetch_option_pricing when parsing fails"""
        future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        mock_fetch_bars.return_value = {'close': 5.0, 'volume': 100, 'timestamp': datetime.now()}
        mock_parse_data.return_value = None
        
        result = self.pricer.fetch_option_pricing('SPY', 500.0, 'call', future_date)
        self.assertIsNone(result)
    
    def test_parse_option_data_valid(self):
        """Test parsing valid option data"""
        option_bars = {
            'close': 5.0,
            'volume': 1000,
            'timestamp': datetime.now()
        }
        
        result = self.pricer._parse_option_data(option_bars, 'SPY', 500.0, 'call', '2024-01-05')
        
        self.assertIsInstance(result, OptionPricingData)
        self.assertEqual(result.symbol, 'SPY')
        self.assertEqual(result.strike, 500.0)
        self.assertEqual(result.option_type, 'call')
        self.assertEqual(result.current_price, 5.0)
        self.assertEqual(result.volume, 1000)
    
    def test_parse_option_data_invalid(self):
        """Test parsing invalid option data"""
        option_bars = {'close': 5.0}
        
        result = self.pricer._parse_option_data(option_bars, 'SPY', 500.0, 'call', '2024-01-05')
        self.assertIsNone(result)
        
        option_bars = {
            'close': -5.0,
            'volume': 1000,
            'timestamp': datetime.now()
        }
        
        result = self.pricer._parse_option_data(option_bars, 'SPY', 500.0, 'call', '2024-01-05')
        self.assertIsNone(result)
    
    def test_get_next_expiration_date(self):
        """Test expiration date calculation"""
        exp_date = self.pricer.get_next_expiration_date(1)
        
        self.assertIsInstance(exp_date, str)
        self.assertEqual(len(exp_date), 10)
        self.assertEqual(exp_date[4], '-')
        self.assertEqual(exp_date[7], '-')


if __name__ == '__main__':
    unittest.main(verbosity=2)
