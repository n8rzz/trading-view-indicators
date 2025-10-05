"""
Unit tests for Signal Management System

Tests the base signal classes and ORB-specific implementations.
"""
import unittest
import pandas as pd
import numpy as np
from datetime import datetime, time
import pytz
from unittest.mock import Mock, MagicMock

from signal_manager import Signal, SignalType, SignalDirection, SignalManager
from signal_context import SignalContext
from orb_signal_manager import ORBContext, ORBSignalManager
from data_structures import OpeningRange, OpportunityWindow, BreakoutType, ExitSignalType


class TestSignal(unittest.TestCase):
    """Test the Signal dataclass"""
    
    def test_signal_creation(self):
        """Test basic signal creation"""
        signal = Signal(
            signal_type=SignalType.ENTRY,
            direction=SignalDirection.LONG,
            strength=0.8,
            metadata={'test': 'value'}
        )
        
        self.assertEqual(signal.signal_type, SignalType.ENTRY)
        self.assertEqual(signal.direction, SignalDirection.LONG)
        self.assertEqual(signal.strength, 0.8)
        self.assertEqual(signal.metadata['test'], 'value')
        self.assertIsNotNone(signal.timestamp)
    
    def test_signal_strength_validation(self):
        """Test signal strength validation"""
        # Valid strength
        signal = Signal(
            signal_type=SignalType.ENTRY,
            direction=SignalDirection.LONG,
            strength=0.5,
            metadata={}
        )
        self.assertEqual(signal.strength, 0.5)
        
        # Invalid strength - too high
        with self.assertRaises(ValueError):
            Signal(
                signal_type=SignalType.ENTRY,
                direction=SignalDirection.LONG,
                strength=1.5,
                metadata={}
            )
        
        # Invalid strength - too low
        with self.assertRaises(ValueError):
            Signal(
                signal_type=SignalType.ENTRY,
                direction=SignalDirection.LONG,
                strength=-0.1,
                metadata={}
            )
    
    def test_signal_timestamp_auto_generation(self):
        """Test that timestamp is automatically generated if not provided"""
        signal = Signal(
            signal_type=SignalType.ENTRY,
            direction=SignalDirection.LONG,
            strength=0.5,
            metadata={}
        )
        self.assertIsNotNone(signal.timestamp)
        self.assertIsInstance(signal.timestamp, pd.Timestamp)
    
    def test_signal_timestamp_manual_setting(self):
        """Test that timestamp can be manually set"""
        custom_timestamp = pd.Timestamp('2025-01-01 12:00:00')
        signal = Signal(
            signal_type=SignalType.ENTRY,
            direction=SignalDirection.LONG,
            strength=0.5,
            metadata={},
            timestamp=custom_timestamp
        )
        self.assertEqual(signal.timestamp, custom_timestamp)


class TestSignalContext(unittest.TestCase):
    """Test the SignalContext base class"""
    
    def test_signal_context_is_abstract(self):
        """Test that SignalContext cannot be instantiated directly"""
        with self.assertRaises(TypeError):
            SignalContext()


class TestORBContext(unittest.TestCase):
    """Test the ORB-specific context class"""
    
    def setUp(self):
        """Set up test data"""
        self.opening_range = OpeningRange(
            start_time=datetime(2025, 1, 1, 8, 30),
            end_time=datetime(2025, 1, 1, 9, 30),
            high=450.0,
            low=445.0,
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
    
    def test_orb_context_creation(self):
        """Test ORB context creation"""
        context = ORBContext(self.opening_range, self.opportunity_window)
        
        self.assertEqual(context.opening_range_data, self.opening_range)
        self.assertEqual(context.opportunity_window, self.opportunity_window)
    
    def test_orb_context_inheritance(self):
        """Test that ORBContext inherits from SignalContext"""
        context = ORBContext(self.opening_range, self.opportunity_window)
        self.assertIsInstance(context, SignalContext)


class TestSignalManager(unittest.TestCase):
    """Test the SignalManager base class"""
    
    def test_signal_manager_is_abstract(self):
        """Test that SignalManager cannot be instantiated directly"""
        with self.assertRaises(TypeError):
            SignalManager(Mock())


class TestORBSignalManager(unittest.TestCase):
    """Test the ORB-specific signal manager"""
    
    def setUp(self):
        """Set up test data and mocks"""
        # Create mock strategy
        self.mock_strategy = Mock()
        self.mock_strategy.symbol = "SPY"
        self.mock_strategy.market_analyzer = Mock()
        self.mock_strategy.position_manager = Mock()
        
        # Create ORB signal manager
        self.signal_manager = ORBSignalManager(self.mock_strategy)
        
        # Create test data
        self.opening_range = OpeningRange(
            start_time=datetime(2025, 1, 1, 8, 30),
            end_time=datetime(2025, 1, 1, 9, 30),
            high=450.0,
            low=445.0,
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
        
        # Create sample market data
        self.market_data = pd.DataFrame({
            'timestamp': pd.date_range('2025-01-01 08:30', periods=10, freq='15min'),
            'open': [445.0] * 10,
            'high': [450.0] * 10,
            'low': [444.0] * 10,
            'close': [448.0] * 10,
            'volume': [1000] * 10
        })
    
    def test_orb_signal_manager_creation(self):
        """Test ORB signal manager creation"""
        self.assertEqual(self.signal_manager.strategy, self.mock_strategy)
        self.assertIsInstance(self.signal_manager, SignalManager)
    
    def test_detect_entry_signals_no_current_price(self):
        """Test entry signal detection when current price cannot be determined"""
        self.mock_strategy.market_analyzer.get_current_price.return_value = None
        
        signals = self.signal_manager.detect_entry_signals(self.market_data, self.context)
        
        self.assertEqual(len(signals), 0)
        self.mock_strategy.market_analyzer.get_current_price.assert_called_once_with(self.market_data)
    
    def test_detect_entry_signals_no_breakout(self):
        """Test entry signal detection when no breakout is detected"""
        self.mock_strategy.market_analyzer.get_current_price.return_value = 448.0
        self.mock_strategy.market_analyzer.detect_breakout.return_value = None
        
        signals = self.signal_manager.detect_entry_signals(self.market_data, self.context)
        
        self.assertEqual(len(signals), 0)
        self.mock_strategy.market_analyzer.detect_breakout.assert_called_once()
    
    def test_detect_entry_signals_orh_breakout(self):
        """Test entry signal detection for ORH breakout"""
        # Mock breakout data
        mock_breakout = Mock()
        mock_breakout.type = BreakoutType.ORH_BREAKOUT
        mock_breakout.breakout_strength = 0.8
        mock_breakout.breakout_level = 451.0
        mock_breakout.distance_from_midline = 2.0
        
        self.mock_strategy.market_analyzer.get_current_price.return_value = 451.0
        self.mock_strategy.market_analyzer.detect_breakout.return_value = mock_breakout
        
        signals = self.signal_manager.detect_entry_signals(self.market_data, self.context)
        
        self.assertEqual(len(signals), 1)
        signal = signals[0]
        self.assertEqual(signal.signal_type, SignalType.ENTRY)
        self.assertEqual(signal.direction, SignalDirection.SHORT)
        self.assertEqual(signal.strength, 0.8)
        self.assertEqual(signal.metadata['breakout_type'], BreakoutType.ORH_BREAKOUT.value)
        self.assertEqual(signal.metadata['strategy_action'], 'sell_put')
    
    def test_detect_entry_signals_orl_breakout(self):
        """Test entry signal detection for ORL breakout"""
        # Mock breakout data
        mock_breakout = Mock()
        mock_breakout.type = BreakoutType.ORL_BREAKOUT
        mock_breakout.breakout_strength = 0.9
        mock_breakout.breakout_level = 444.0
        mock_breakout.distance_from_midline = -2.0
        
        self.mock_strategy.market_analyzer.get_current_price.return_value = 444.0
        self.mock_strategy.market_analyzer.detect_breakout.return_value = mock_breakout
        
        signals = self.signal_manager.detect_entry_signals(self.market_data, self.context)
        
        self.assertEqual(len(signals), 1)
        signal = signals[0]
        self.assertEqual(signal.signal_type, SignalType.ENTRY)
        self.assertEqual(signal.direction, SignalDirection.SHORT)
        self.assertEqual(signal.strength, 0.9)
        self.assertEqual(signal.metadata['breakout_type'], BreakoutType.ORL_BREAKOUT.value)
        self.assertEqual(signal.metadata['strategy_action'], 'sell_call')
    
    def test_detect_exit_signals_no_current_price(self):
        """Test exit signal detection when current price cannot be determined"""
        self.mock_strategy.market_analyzer.get_current_price.return_value = None
        
        signals = self.signal_manager.detect_exit_signals(self.market_data, self.context)
        
        self.assertEqual(len(signals), 0)
        self.mock_strategy.market_analyzer.get_current_price.assert_called_once_with(self.market_data)
    
    def test_detect_exit_signals_no_exit_signal(self):
        """Test exit signal detection when no exit signal is detected"""
        self.mock_strategy.market_analyzer.get_current_price.return_value = 448.0
        self.mock_strategy.market_analyzer.detect_exit_signal.return_value = None
        
        signals = self.signal_manager.detect_exit_signals(self.market_data, self.context)
        
        self.assertEqual(len(signals), 0)
        self.mock_strategy.market_analyzer.detect_exit_signal.assert_called_once()
    
    def test_detect_exit_signals_with_exit_signal(self):
        """Test exit signal detection when exit signal is detected"""
        # Mock exit signal data
        mock_exit_signal = Mock()
        mock_exit_signal.type = ExitSignalType.MIDLINE_CROSS
        mock_exit_signal.current_price = 447.5
        mock_exit_signal.orh = 450.0
        mock_exit_signal.orl = 445.0
        mock_exit_signal.opportunity_window_midline = 447.5
        mock_exit_signal.reason = "Price crossed opportunity window midline"
        
        self.mock_strategy.market_analyzer.get_current_price.return_value = 447.5
        self.mock_strategy.market_analyzer.detect_exit_signal.return_value = mock_exit_signal
        
        signals = self.signal_manager.detect_exit_signals(self.market_data, self.context)
        
        self.assertEqual(len(signals), 1)
        signal = signals[0]
        self.assertEqual(signal.signal_type, SignalType.EXIT)
        self.assertEqual(signal.direction, SignalDirection.NEUTRAL)
        self.assertEqual(signal.strength, 1.0)
        self.assertEqual(signal.metadata['exit_type'], ExitSignalType.MIDLINE_CROSS.value)
        self.assertEqual(signal.metadata['strategy_action'], 'close_all_positions')
    
    def test_process_all_signals(self):
        """Test processing all signals"""
        # Mock entry signal
        mock_breakout = Mock()
        mock_breakout.type = BreakoutType.ORH_BREAKOUT
        mock_breakout.breakout_strength = 0.8
        mock_breakout.breakout_level = 451.0
        mock_breakout.distance_from_midline = 2.0
        
        self.mock_strategy.market_analyzer.get_current_price.return_value = 451.0
        self.mock_strategy.market_analyzer.detect_breakout.return_value = mock_breakout
        self.mock_strategy.market_analyzer.detect_exit_signal.return_value = None
        
        all_signals = self.signal_manager.process_all_signals(self.market_data, self.context)
        
        self.assertIn('entry', all_signals)
        self.assertIn('exit', all_signals)
        self.assertEqual(len(all_signals['entry']), 1)
        self.assertEqual(len(all_signals['exit']), 0)
    
    def test_has_signals_true(self):
        """Test has_signals returns True when signals exist"""
        # Mock entry signal
        mock_breakout = Mock()
        mock_breakout.type = BreakoutType.ORH_BREAKOUT
        mock_breakout.breakout_strength = 0.8
        mock_breakout.breakout_level = 451.0
        mock_breakout.distance_from_midline = 2.0
        
        self.mock_strategy.market_analyzer.get_current_price.return_value = 451.0
        self.mock_strategy.market_analyzer.detect_breakout.return_value = mock_breakout
        self.mock_strategy.market_analyzer.detect_exit_signal.return_value = None
        
        has_signals = self.signal_manager.has_signals(self.market_data, self.context)
        
        self.assertTrue(has_signals)
    
    def test_has_signals_false(self):
        """Test has_signals returns False when no signals exist"""
        self.mock_strategy.market_analyzer.get_current_price.return_value = 448.0
        self.mock_strategy.market_analyzer.detect_breakout.return_value = None
        self.mock_strategy.market_analyzer.detect_exit_signal.return_value = None
        
        has_signals = self.signal_manager.has_signals(self.market_data, self.context)
        
        self.assertFalse(has_signals)


if __name__ == '__main__':
    unittest.main()
