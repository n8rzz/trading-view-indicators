"""
Integration tests for Signal Management System

Tests the signal manager integration with the ORB strategy and market analyzer.
"""
import unittest
import pandas as pd
import numpy as np
from datetime import datetime, time
import pytz
from unittest.mock import Mock, patch

from orb_strategy import ORBBreakoutStrategy
from orb_signal_manager import ORBSignalManager, ORBContext
from signal_manager import SignalType, SignalDirection
from data_structures import OpeningRange, OpportunityWindow, BreakoutType, ExitSignalType


class TestSignalManagerIntegration(unittest.TestCase):
    """Integration tests for signal manager with ORB strategy"""
    
    def setUp(self):
        """Set up test data and strategy"""
        self.strategy = ORBBreakoutStrategy(
            symbol="SPY",
            opening_range_duration=60,
            min_range_size_percent=0.2,
            interval=15
        )
        self.signal_manager = ORBSignalManager(self.strategy)
        self.market_data = pd.DataFrame({
            'timestamp': pd.date_range('2025-01-01 08:30', periods=20, freq='15min'),
            'open': [445.0, 445.5, 446.0, 446.5, 447.0, 447.5, 448.0, 448.5, 449.0, 449.5,
                     450.0, 450.5, 451.0, 451.5, 452.0, 452.5, 453.0, 453.5, 454.0, 454.5],
            'high': [446.0, 446.5, 447.0, 447.5, 448.0, 448.5, 449.0, 449.5, 450.0, 450.5,
                     451.0, 451.5, 452.0, 452.5, 453.0, 453.5, 454.0, 454.5, 455.0, 455.5],
            'low': [444.0, 444.5, 445.0, 445.5, 446.0, 446.5, 447.0, 447.5, 448.0, 448.5,
                    449.0, 449.5, 450.0, 450.5, 451.0, 451.5, 452.0, 452.5, 453.0, 453.5],
            'close': [445.5, 446.0, 446.5, 447.0, 447.5, 448.0, 448.5, 449.0, 449.5, 450.0,
                      450.5, 451.0, 451.5, 452.0, 452.5, 453.0, 453.5, 454.0, 454.5, 455.0],
            'volume': [1000] * 20
        })
        self.opening_range = OpeningRange(
            start_time=datetime(2025, 1, 1, 8, 30),
            end_time=datetime(2025, 1, 1, 9, 30),
            high=450.0,  # ORH
            low=445.0,   # ORL
            range_size=5.0,
            range_percent=1.1,
            current_price=447.5,
            bars_count=100,
            required_range_size=4.0,
            range_ratio=1.25,
            is_historical_data=False,
            data_date=datetime(2025, 1, 1)
        )
        self.opportunity_window = OpportunityWindow(
            start_time=datetime(2025, 1, 1, 9, 30),
            end_time=datetime(2025, 1, 1, 12, 0),
            midline=447.5,
            duration_minutes=150,
            is_active=True
        )
        
        self.context = ORBContext(self.opening_range, self.opportunity_window)
    
    def test_signal_manager_with_real_strategy(self):
        """Test that signal manager works with real strategy instance"""
        # This should not raise any errors
        self.assertIsInstance(self.signal_manager.strategy, ORBBreakoutStrategy)
        self.assertEqual(self.signal_manager.strategy.symbol, "SPY")
    
    @patch('orb_signal_manager.trading_logger')
    def test_entry_signal_detection_integration(self, mock_logger):
        """Test entry signal detection with real market analyzer"""
        # Mock the market analyzer methods to return specific results
        with patch.object(self.strategy.market_analyzer, 'get_current_price') as mock_get_price, \
             patch.object(self.strategy.market_analyzer, 'detect_breakout') as mock_detect_breakout:
            
            mock_get_price.return_value = 451.0
            mock_breakout = Mock()
            mock_breakout.type = BreakoutType.ORH_BREAKOUT
            mock_breakout.breakout_strength = 0.8
            mock_breakout.breakout_level = 451.0
            mock_breakout.distance_from_midline = 2.0
            mock_detect_breakout.return_value = mock_breakout
            
            signals = self.signal_manager.detect_entry_signals(self.market_data, self.context)
            
            self.assertEqual(len(signals), 1)
            signal = signals[0]
            self.assertEqual(signal.signal_type, SignalType.ENTRY)
            self.assertEqual(signal.direction, SignalDirection.SHORT)
            self.assertEqual(signal.strength, 0.8)
            self.assertEqual(signal.metadata['breakout_type'], BreakoutType.ORH_BREAKOUT.value)
            self.assertEqual(signal.metadata['strategy_action'], 'sell_put')
            
            mock_get_price.assert_called_once_with(self.market_data)
            mock_detect_breakout.assert_called_once()
    
    @patch('orb_signal_manager.trading_logger')
    def test_exit_signal_detection_integration(self, mock_logger):
        """Test exit signal detection with real market analyzer"""
        with patch.object(self.strategy.market_analyzer, 'get_current_price') as mock_get_price, \
             patch.object(self.strategy.market_analyzer, 'detect_exit_signal') as mock_detect_exit:
            
            mock_get_price.return_value = 447.5  # Price at midline
            mock_exit_signal = Mock()
            mock_exit_signal.type = ExitSignalType.MIDLINE_CROSS
            mock_exit_signal.current_price = 447.5
            mock_exit_signal.orh = 450.0
            mock_exit_signal.orl = 445.0
            mock_exit_signal.opportunity_window_midline = 447.5
            mock_exit_signal.reason = "Price crossed opportunity window midline"
            mock_detect_exit.return_value = mock_exit_signal
            
            signals = self.signal_manager.detect_exit_signals(self.market_data, self.context)
            
            self.assertEqual(len(signals), 1)
            
            signal = signals[0]
            
            self.assertEqual(signal.signal_type, SignalType.EXIT)
            self.assertEqual(signal.direction, SignalDirection.NEUTRAL)
            self.assertEqual(signal.strength, 1.0)
            self.assertEqual(signal.metadata['exit_type'], ExitSignalType.MIDLINE_CROSS.value)
            self.assertEqual(signal.metadata['strategy_action'], 'close_all_positions')
            
            mock_get_price.assert_called_once_with(self.market_data)
            mock_detect_exit.assert_called_once()
    
    def test_process_all_signals_integration(self):
        """Test processing all signals with real strategy"""
        # Mock the market analyzer methods
        with patch.object(self.strategy.market_analyzer, 'get_current_price') as mock_get_price, \
             patch.object(self.strategy.market_analyzer, 'detect_breakout') as mock_detect_breakout, \
             patch.object(self.strategy.market_analyzer, 'detect_exit_signal') as mock_detect_exit:
            
            mock_get_price.return_value = 451.0
            mock_breakout = Mock()
            mock_breakout.type = BreakoutType.ORH_BREAKOUT
            mock_breakout.breakout_strength = 0.8
            mock_breakout.breakout_level = 451.0
            mock_breakout.distance_from_midline = 2.0
            mock_detect_breakout.return_value = mock_breakout
            mock_exit_signal = Mock()
            mock_exit_signal.type = ExitSignalType.MIDLINE_CROSS
            mock_exit_signal.current_price = 451.0
            mock_exit_signal.orh = 450.0
            mock_exit_signal.orl = 445.0
            mock_exit_signal.opportunity_window_midline = 447.5
            mock_exit_signal.reason = "Price crossed opportunity window midline"
            mock_detect_exit.return_value = mock_exit_signal
            all_signals = self.signal_manager.process_all_signals(self.market_data, self.context)
            
            self.assertIn('entry', all_signals)
            self.assertIn('exit', all_signals)
            self.assertEqual(len(all_signals['entry']), 1)
            self.assertEqual(len(all_signals['exit']), 1)
            
            entry_signal = all_signals['entry'][0]

            self.assertEqual(entry_signal.signal_type, SignalType.ENTRY)
            self.assertEqual(entry_signal.direction, SignalDirection.SHORT)
            
            exit_signal = all_signals['exit'][0]
            
            self.assertEqual(exit_signal.signal_type, SignalType.EXIT)
            self.assertEqual(exit_signal.direction, SignalDirection.NEUTRAL)
    
    def test_signal_strength_capping(self):
        """Test that signal strength is properly capped at 1.0"""
        with patch.object(self.strategy.market_analyzer, 'get_current_price') as mock_get_price, \
             patch.object(self.strategy.market_analyzer, 'detect_breakout') as mock_detect_breakout:
            
            mock_get_price.return_value = 451.0
            
            # Mock breakout with strength > 1.0
            mock_breakout = Mock()
            mock_breakout.type = BreakoutType.ORH_BREAKOUT
            mock_breakout.breakout_strength = 1.5  # > 1.0
            mock_breakout.breakout_level = 451.0
            mock_breakout.distance_from_midline = 2.0
            mock_detect_breakout.return_value = mock_breakout
            
            signals = self.signal_manager.detect_entry_signals(self.market_data, self.context)
            
            self.assertEqual(len(signals), 1)
            self.assertEqual(signals[0].strength, 1.0)
    
    def test_signal_metadata_completeness(self):
        """Test that signal metadata contains all expected fields"""
        with patch.object(self.strategy.market_analyzer, 'get_current_price') as mock_get_price, \
             patch.object(self.strategy.market_analyzer, 'detect_breakout') as mock_detect_breakout:
            
            mock_get_price.return_value = 451.0
            
            mock_breakout = Mock()
            mock_breakout.type = BreakoutType.ORH_BREAKOUT
            mock_breakout.breakout_strength = 0.8
            mock_breakout.breakout_level = 451.0
            mock_breakout.distance_from_midline = 2.0
            mock_detect_breakout.return_value = mock_breakout
            
            signals = self.signal_manager.detect_entry_signals(self.market_data, self.context)
            
            self.assertEqual(len(signals), 1)

            metadata = signals[0].metadata
            expected_fields = [
                'breakout_type', 'breakout_level', 'current_price',
                'orh', 'orl', 'distance_from_midline', 'strategy_action'
            ]
            
            for field in expected_fields:
                self.assertIn(field, metadata, f"Missing field: {field}")
        
            self.assertEqual(metadata['breakout_type'], BreakoutType.ORH_BREAKOUT.value)
            self.assertEqual(metadata['current_price'], 451.0)
            self.assertEqual(metadata['orh'], 450.0)
            self.assertEqual(metadata['orl'], 445.0)
            self.assertEqual(metadata['strategy_action'], 'sell_put')


if __name__ == '__main__':
    unittest.main()
