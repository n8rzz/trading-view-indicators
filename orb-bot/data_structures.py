"""
Shared Data Structures Module

This module contains shared data structures used across the ORB trading strategy.
"""

from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple, TYPE_CHECKING
import pytz

if TYPE_CHECKING:
    import pandas as pd


@dataclass
class OpportunityWindow:
    """Opportunity Window data structure"""
    start_time: datetime
    end_time: datetime
    midline: float
    duration_minutes: float
    is_active: bool
    
    def is_currently_active(self, timezone: pytz.timezone) -> bool:
        """
        Check if current time is within this opportunity window
        
        Args:
            timezone: Timezone to use for current time calculation
            
        Returns:
            True if currently within opportunity window, False otherwise
        """
        now = datetime.now(timezone)
        return self.start_time <= now <= self.end_time


@dataclass
class MarketDataResult:
    """Market data result with historical flag"""
    data: 'pd.DataFrame'
    is_historical: bool
    data_date: datetime
    days_old: int = 0


@dataclass
class OpeningRange:
    """Opening range calculation result"""
    start_time: datetime
    end_time: datetime
    high: float
    low: float
    range_size: float
    range_percent: float
    current_price: float
    bars_count: int
    required_range_size: float
    range_ratio: float
    is_historical_data: bool
    data_date: datetime
    days_old: int = 0

# FIXME: use enums for `type` and `direction`
@dataclass
class BreakoutSignal:
    """Breakout signal data structure"""
    type: str  # 'ORH_BREAKOUT' or 'ORL_BREAKOUT'
    current_price: float
    breakout_level: float
    direction: str  # 'UP' or 'DOWN'
    timestamp: datetime
    distance_from_midline: float
    breakout_strength: float  # Percentage strength of breakout
    
    def display_breakout_info(self) -> str:
        """
        Generate a formatted string displaying breakout information
        
        Returns:
            Formatted string with breakout details
        """
        return (
            f"🚨 BREAKOUT DETECTED!\n"
            f"   Type: {self.type}\n"
            f"   Direction: {self.direction}\n"
            f"   Breakout Level: ${self.breakout_level:.2f}\n"
            f"   Breakout Strength: {self.breakout_strength:.2f}%\n"
            f"   Distance from Midline: ${self.distance_from_midline:.2f}"
        )

# FIXME: use enums for `type`
@dataclass
class ExitSignal:
    """Exit signal data structure"""
    type: str  # SignalType enum value (e.g., 'MIDLINE_CROSS')
    current_price: float
    orh: float
    orl: float
    opportunity_window_midline: float
    timestamp: datetime
    reason: str  # Description of why exit was triggered
    
    def display_exit_info(self) -> str:
        """
        Generate a formatted string displaying exit information
        
        Returns:
            Formatted string with exit details
        """
        return (
            f"🚪 EXIT SIGNAL DETECTED!\n"
            f"   Type: {self.type}\n"
            f"   Reason: {self.reason}\n"
            f"   Current Price: ${self.current_price:.2f}\n"
            f"   ORH: ${self.orh:.2f}\n"
            f"   ORL: ${self.orl:.2f}\n"
            f"   Opportunity Window Midline: ${self.opportunity_window_midline:.2f}"
        )
