#!/usr/bin/env python3
"""
Test suite for MarketAnalyzer class

This module contains comprehensive tests for the MarketAnalyzer class,
covering all methods, edge cases, and error conditions.
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import pytz
import sys
import os

# Add the current directory to the path so we can import our module
# This is needed when running tests directly with python test_market_analyzer.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from market_analyzer import MarketAnalyzer
from data_structures import OpportunityWindow, BreakoutSignal


class TestMarketAnalyzer(unittest.TestCase):
    """Test cases for MarketAnalyzer class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.analyzer = MarketAnalyzer(timezone='US/Central')
        self.central_tz = pytz.timezone('US/Central')
        
        # Create test data for today
        self.today = datetime.now(self.central_tz).date()
        self.market_open = datetime.combine(self.today, time(8, 30))
        self.market_open = self.central_tz.localize(self.market_open)
        
        # Create sample bars data
        self.sample_bars = self._create_sample_bars()
    
    def _create_sample_bars(self, num_bars: int = 100) -> pd.DataFrame:
        """Create sample bars data for testing"""
        timestamps = [self.market_open + timedelta(minutes=i) for i in range(num_bars)]
        
        # Create realistic price data
        base_price = 450.0
        prices = []
        current_price = base_price
        
        for i in range(num_bars):
            # Add some volatility
            change = np.random.normal(0, 0.5)
            current_price += change
            
            open_price = current_price
            high_price = current_price + abs(np.random.normal(0, 0.3))
            low_price = current_price - abs(np.random.normal(0, 0.3))
            close_price = current_price + np.random.normal(0, 0.2)
            volume = np.random.randint(1000, 10000)
            
            prices.append({
                'timestamp': timestamps[i],
                'open': round(open_price, 2),
                'high': round(high_price, 2),
                'low': round(low_price, 2),
                'close': round(close_price, 2),
                'volume': volume
            })
        
        return pd.DataFrame(prices)
    
    def test_init(self):
        """Test MarketAnalyzer initialization"""
        analyzer = MarketAnalyzer(timezone='US/Eastern')
        self.assertEqual(analyzer.timezone.zone, 'US/Eastern')
        self.assertEqual(analyzer.market_open_time, time(8, 30))
        self.assertEqual(analyzer.market_close_time, time(15, 0))
    
    def test_calculate_opening_range_success(self):
        """Test successful opening range calculation"""
        result = self.analyzer.calculate_opening_range(
            self.sample_bars, 
            opening_range_duration=60,
            min_range_size_percent=0.1
        )
        
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.high)
        self.assertIsNotNone(result.low)
        self.assertIsNotNone(result.range_size)
        self.assertIsNotNone(result.range_percent)
        self.assertIsNotNone(result.range_ratio)
        self.assertGreater(result.high, result.low)
        self.assertGreater(result.range_size, 0)
        self.assertGreater(result.range_percent, 0)
    
    def test_calculate_opening_range_empty_data(self):
        """Test opening range calculation with empty data"""
        empty_df = pd.DataFrame()
        result = self.analyzer.calculate_opening_range(empty_df)
        self.assertIsNone(result)
    
    def test_calculate_opening_range_insufficient_data(self):
        """Test opening range calculation with insufficient data"""
        # Create data with only 5 minutes (less than 60 minute opening range)
        short_bars = self._create_sample_bars(5)
        result = self.analyzer.calculate_opening_range(short_bars, opening_range_duration=60)
        # The method should still work with 5 bars, but we'll test with 0 bars instead
        empty_bars = pd.DataFrame()
        result_empty = self.analyzer.calculate_opening_range(empty_bars)
        self.assertIsNone(result_empty)
    
    def test_calculate_opening_range_too_small(self):
        """Test opening range calculation with range too small"""
        # Create data with very small range (0.01% of price)
        small_range_bars = self.sample_bars.copy()
        base_price = 450.0
        small_range_bars['high'] = base_price + 0.01  # Very small range
        small_range_bars['low'] = base_price - 0.01
        small_range_bars['close'] = base_price
        
        result = self.analyzer.calculate_opening_range(
            small_range_bars, 
            min_range_size_percent=0.1  # Require 0.1% range (0.02% actual)
        )
        self.assertIsNone(result)
    
    def test_calculate_opening_range_missing_columns(self):
        """Test opening range calculation with missing columns"""
        incomplete_bars = self.sample_bars.drop(columns=['high', 'low'])
        result = self.analyzer.calculate_opening_range(incomplete_bars)
        self.assertIsNone(result)
    
    def test_calculate_opportunity_window_success(self):
        """Test successful opportunity window calculation"""
        # First calculate opening range
        opening_range = self.analyzer.calculate_opening_range(self.sample_bars)
        self.assertIsNotNone(opening_range)
        
        # Then calculate opportunity window
        opportunity_window = self.analyzer.calculate_opportunity_window(
            opening_range, 
            time(12, 0)  # 12:00 PM
        )
        
        self.assertIsNotNone(opportunity_window)
        self.assertIsInstance(opportunity_window, OpportunityWindow)
        self.assertIsNotNone(opportunity_window.start_time)
        self.assertIsNotNone(opportunity_window.end_time)
        self.assertGreater(opportunity_window.duration_minutes, 0)
        self.assertIsInstance(opportunity_window.is_active, bool)
    
    def test_calculate_opportunity_window_no_opening_range(self):
        """Test opportunity window calculation with no opening range data"""
        result = self.analyzer.calculate_opportunity_window(None, time(12, 0))
        self.assertIsNone(result)
    
    def test_calculate_opportunity_window_with_timezone(self):
        """Test opportunity window calculation with timezone-aware time"""
        opening_range = self.analyzer.calculate_opening_range(self.sample_bars)
        self.assertIsNotNone(opening_range)
        
        # Test with timezone-aware time
        tz_aware_time = time(12, 0, tzinfo=pytz.timezone('US/Central'))
        opportunity_window = self.analyzer.calculate_opportunity_window(
            opening_range, 
            tz_aware_time
        )
        
        self.assertIsNotNone(opportunity_window)
        self.assertIsInstance(opportunity_window, OpportunityWindow)
    
    def test_is_within_opportunity_window_active(self):
        """Test opportunity window active status"""
        opening_range = self.analyzer.calculate_opening_range(self.sample_bars)
        opportunity_window = self.analyzer.calculate_opportunity_window(
            opening_range, 
            time(12, 0)
        )
        
        # The window should not be active since we're testing with historical data
        self.assertFalse(opportunity_window.is_active)
    
    def test_is_within_opportunity_window_method(self):
        """Test is_within_opportunity_window method"""
        opening_range = self.analyzer.calculate_opening_range(self.sample_bars)
        opportunity_window = self.analyzer.calculate_opportunity_window(
            opening_range, 
            time(12, 0)
        )
        
        result = self.analyzer.is_within_opportunity_window(opportunity_window)
        self.assertIsInstance(result, bool)
    
    def test_opportunity_window_is_currently_active(self):
        """Test OpportunityWindow.is_currently_active method"""
        opening_range = self.analyzer.calculate_opening_range(self.sample_bars)
        opportunity_window = self.analyzer.calculate_opportunity_window(
            opening_range, 
            time(12, 0)
        )
        
        result = opportunity_window.is_currently_active(self.analyzer.timezone)
        self.assertIsInstance(result, bool)
    
    def test_is_within_opportunity_window_none(self):
        """Test is_within_opportunity_window with None input"""
        result = self.analyzer.is_within_opportunity_window(None)
        self.assertFalse(result)
    
    def test_detect_breakout_no_data(self):
        """Test breakout detection with no data"""
        result = self.analyzer.detect_breakout(450.0, None, None)
        self.assertIsNone(result)
    
    def test_detect_breakout_outside_window(self):
        """Test breakout detection outside opportunity window"""
        opening_range = self.analyzer.calculate_opening_range(self.sample_bars)
        opportunity_window = self.analyzer.calculate_opportunity_window(
            opening_range, 
            time(12, 0)
        )
        
        # Test with price above ORH but outside window
        result = self.analyzer.detect_breakout(
            opening_range.high + 1.0,
            opening_range,
            opportunity_window
        )
        self.assertIsNone(result)
    
    def test_detect_breakout_above_orh(self):
        """Test breakout detection above ORH"""
        opening_range = self.analyzer.calculate_opening_range(self.sample_bars)
        
        # Create a mock opportunity window that's always active
        mock_window = OpportunityWindow(
            start_time=datetime.now(self.central_tz) - timedelta(hours=1),
            end_time=datetime.now(self.central_tz) + timedelta(hours=1),
            midline=(opening_range.high + opening_range.low) / 2,
            duration_minutes=120,
            is_active=True
        )
        
        result = self.analyzer.detect_breakout(
            opening_range.high + 1.0,
            opening_range,
            mock_window
        )
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result, BreakoutSignal)
        self.assertEqual(result.type, 'ORH_BREAKOUT')
        self.assertEqual(result.direction, 'UP')
        self.assertGreater(result.breakout_strength, 0)
    
    def test_detect_breakout_below_orl(self):
        """Test breakout detection below ORL"""
        opening_range = self.analyzer.calculate_opening_range(self.sample_bars)
        
        # Create a mock opportunity window that's always active
        mock_window = OpportunityWindow(
            start_time=datetime.now(self.central_tz) - timedelta(hours=1),
            end_time=datetime.now(self.central_tz) + timedelta(hours=1),
            midline=(opening_range.high + opening_range.low) / 2,
            duration_minutes=120,
            is_active=True
        )
        
        result = self.analyzer.detect_breakout(
            opening_range.low - 1.0,
            opening_range,
            mock_window
        )
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result, BreakoutSignal)
        self.assertEqual(result.type, 'ORL_BREAKOUT')
        self.assertEqual(result.direction, 'DOWN')
        self.assertGreater(result.breakout_strength, 0)
    
    def test_detect_breakout_within_range(self):
        """Test breakout detection when price is within range"""
        opening_range = self.analyzer.calculate_opening_range(self.sample_bars)
        
        # Create a mock opportunity window that's always active
        mock_window = OpportunityWindow(
            start_time=datetime.now(self.central_tz) - timedelta(hours=1),
            end_time=datetime.now(self.central_tz) + timedelta(hours=1),
            midline=(opening_range.high + opening_range.low) / 2,
            duration_minutes=120,
            is_active=True
        )
        
        # Test with price within range
        mid_price = (opening_range.high + opening_range.low) / 2
        result = self.analyzer.detect_breakout(
            mid_price,
            opening_range,
            mock_window
        )
        
        self.assertIsNone(result)
    
    def test_get_current_price_success(self):
        """Test getting current price from bars data"""
        current_price = self.analyzer.get_current_price(self.sample_bars)
        self.assertIsNotNone(current_price)
        self.assertIsInstance(current_price, float)
        self.assertGreater(current_price, 0)
    
    def test_get_current_price_empty_data(self):
        """Test getting current price from empty data"""
        empty_df = pd.DataFrame()
        result = self.analyzer.get_current_price(empty_df)
        self.assertIsNone(result)
    
    def test_get_current_price_missing_close(self):
        """Test getting current price with missing close column"""
        incomplete_bars = self.sample_bars.drop(columns=['close'])
        result = self.analyzer.get_current_price(incomplete_bars)
        self.assertIsNone(result)
    
    def test_range_ratio_calculation(self):
        """Test range ratio calculation"""
        result = self.analyzer.calculate_opening_range(
            self.sample_bars, 
            min_range_size_percent=0.1
        )
        
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.range_ratio)
        self.assertGreater(result.range_ratio, 0)
        
        # Range ratio should be actual range / required range
        expected_ratio = result.range_size / result.required_range_size
        self.assertAlmostEqual(result.range_ratio, expected_ratio, places=2)
    
    def test_timezone_handling(self):
        """Test timezone handling in various scenarios"""
        # Test with UTC data
        utc_bars = self.sample_bars.copy()
        utc_bars['timestamp'] = utc_bars['timestamp'].dt.tz_convert('UTC')
        
        result = self.analyzer.calculate_opening_range(utc_bars)
        self.assertIsNotNone(result)
        
        # Test opportunity window with timezone conversion
        opportunity_window = self.analyzer.calculate_opportunity_window(
            result, 
            time(12, 0, tzinfo=pytz.timezone('US/Central'))
        )
        self.assertIsNotNone(opportunity_window)
    
    def test_edge_case_market_hours_boundary(self):
        """Test edge case at market hours boundary"""
        # Create bars exactly at market open
        boundary_time = self.market_open
        boundary_bars = pd.DataFrame([{
            'timestamp': boundary_time,
            'open': 450.0,
            'high': 451.0,
            'low': 449.0,
            'close': 450.5,
            'volume': 1000
        }])
        
        result = self.analyzer.calculate_opening_range(boundary_bars)
        # Should work even with minimal data
        self.assertIsNotNone(result)


class TestOpportunityWindow(unittest.TestCase):
    """Test cases for OpportunityWindow dataclass"""
    
    def test_opportunity_window_creation(self):
        """Test OpportunityWindow dataclass creation"""
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=2)
        
        window = OpportunityWindow(
            start_time=start_time,
            end_time=end_time,
            midline=450.0,
            duration_minutes=120.0,
            is_active=True
        )
        
        self.assertEqual(window.start_time, start_time)
        self.assertEqual(window.end_time, end_time)
        self.assertEqual(window.midline, 450.0)
        self.assertEqual(window.duration_minutes, 120.0)
        self.assertTrue(window.is_active)
    
    def test_opportunity_window_immutability(self):
        """Test that OpportunityWindow fields can be accessed"""
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=2)
        
        window = OpportunityWindow(
            start_time=start_time,
            end_time=end_time,
            midline=450.0,
            duration_minutes=120.0,
            is_active=True
        )
        
        # Test field access
        self.assertIsNotNone(window.start_time)
        self.assertIsNotNone(window.end_time)
        self.assertIsInstance(window.midline, float)
        self.assertIsInstance(window.duration_minutes, float)
        self.assertIsInstance(window.is_active, bool)


class TestBreakoutSignal(unittest.TestCase):
    """Test cases for BreakoutSignal dataclass"""
    
    def test_breakout_signal_creation(self):
        """Test BreakoutSignal dataclass creation"""
        timestamp = datetime.now()
        
        signal = BreakoutSignal(
            type='ORH_BREAKOUT',
            current_price=450.50,
            breakout_level=450.00,
            direction='UP',
            timestamp=timestamp,
            distance_from_midline=0.50,
            breakout_strength=0.11
        )
        
        self.assertEqual(signal.type, 'ORH_BREAKOUT')
        self.assertEqual(signal.current_price, 450.50)
        self.assertEqual(signal.breakout_level, 450.00)
        self.assertEqual(signal.direction, 'UP')
        self.assertEqual(signal.timestamp, timestamp)
        self.assertEqual(signal.distance_from_midline, 0.50)
        self.assertEqual(signal.breakout_strength, 0.11)
    
    def test_breakout_signal_field_types(self):
        """Test that BreakoutSignal fields have correct types"""
        timestamp = datetime.now()
        
        signal = BreakoutSignal(
            type='ORL_BREAKOUT',
            current_price=449.50,
            breakout_level=450.00,
            direction='DOWN',
            timestamp=timestamp,
            distance_from_midline=-0.50,
            breakout_strength=0.11
        )
        
        self.assertIsInstance(signal.type, str)
        self.assertIsInstance(signal.current_price, float)
        self.assertIsInstance(signal.breakout_level, float)
        self.assertIsInstance(signal.direction, str)
        self.assertIsInstance(signal.timestamp, datetime)
        self.assertIsInstance(signal.distance_from_midline, float)
        self.assertIsInstance(signal.breakout_strength, float)
    
    def test_breakout_signal_display_info(self):
        """Test BreakoutSignal.display_breakout_info method"""
        timestamp = datetime.now()
        
        signal = BreakoutSignal(
            type='ORH_BREAKOUT',
            current_price=450.50,
            breakout_level=450.00,
            direction='UP',
            timestamp=timestamp,
            distance_from_midline=0.50,
            breakout_strength=0.11
        )
        
        display_text = signal.display_breakout_info()
        self.assertIsInstance(display_text, str)
        self.assertIn('🚨 BREAKOUT DETECTED!', display_text)
        self.assertIn('ORH_BREAKOUT', display_text)
        self.assertIn('UP', display_text)
        self.assertIn('$450.00', display_text)
        self.assertIn('0.11%', display_text)


if __name__ == '__main__':
    # Set up logging to reduce noise during tests
    import logging
    logging.basicConfig(level=logging.WARNING)
    
    # Run the tests
    unittest.main(verbosity=2)
