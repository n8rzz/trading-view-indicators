"""
Signal Management System

This module provides a generic signal management system for trading strategies.
It handles the detection of entry and exit signals in a strategy-agnostic way.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
import pandas as pd

from signal_context import SignalContext


class SignalType(Enum):
    """Types of trading signals"""
    ENTRY = "ENTRY"
    EXIT = "EXIT"


class SignalDirection(Enum):
    """Direction of the signal"""
    LONG = "LONG"
    SHORT = "SHORT"
    NEUTRAL = "NEUTRAL"


@dataclass
class Signal:
    """
    Represents a trading signal
    
    Attributes:
        signal_type: Type of signal (ENTRY or EXIT)
        direction: Direction of the signal (LONG, SHORT, or NEUTRAL)
        strength: Signal strength (0.0 to 1.0)
        metadata: Additional signal-specific data
        timestamp: When the signal was generated
    """
    signal_type: SignalType
    direction: SignalDirection
    strength: float
    metadata: Dict[str, Any]
    timestamp: Optional[pd.Timestamp] = None
    
    def __post_init__(self):
        """Validate signal data after initialization"""
        if not 0.0 <= self.strength <= 1.0:
            raise ValueError(f"Signal strength must be between 0.0 and 1.0, got {self.strength}")
        
        if self.timestamp is None:
            self.timestamp = pd.Timestamp.now()

class SignalManager(ABC):
    """
    Abstract base class for signal managers
    
    Each strategy should implement its own signal manager that knows how to
    detect entry and exit signals for that specific strategy.
    """
    
    def __init__(self, strategy):
        """
        Initialize the signal manager
        
        Args:
            strategy: The trading strategy instance
        """
        self.strategy = strategy
    
    @abstractmethod
    def detect_entry_signals(self, market_data: pd.DataFrame, context: SignalContext) -> List[Signal]:
        """
        Detect entry signals from market data
        
        Args:
            market_data: Market data (OHLCV bars)
            context: Strategy-specific context for signal detection
            
        Returns:
            List of entry signals, empty list if no signals
        """
        pass
    
    @abstractmethod
    def detect_exit_signals(self, market_data: pd.DataFrame, context: SignalContext) -> List[Signal]:
        """
        Detect exit signals from market data
        
        Args:
            market_data: Market data (OHLCV bars)
            context: Strategy-specific context for signal detection
            
        Returns:
            List of exit signals, empty list if no signals
        """
        pass
    
    def process_all_signals(self, market_data: pd.DataFrame, context: SignalContext) -> Dict[str, List[Signal]]:
        """
        Process all signals (entry and exit)
        
        Args:
            market_data: Market data (OHLCV bars)
            context: Strategy-specific context for signal detection
            
        Returns:
            Dictionary with 'entry' and 'exit' keys containing lists of signals
        """
        entry_signals = self.detect_entry_signals(market_data, context)
        exit_signals = self.detect_exit_signals(market_data, context)
        
        return {
            'entry': entry_signals,
            'exit': exit_signals
        }
    
    def has_signals(self, market_data: pd.DataFrame, context: SignalContext) -> bool:
        """
        Check if there are any signals in the current market data
        
        Args:
            market_data: Market data (OHLCV bars)
            context: Strategy-specific context for signal detection
            
        Returns:
            True if there are any entry or exit signals
        """
        all_signals = self.process_all_signals(market_data, context)
        return len(all_signals['entry']) > 0 or len(all_signals['exit']) > 0
