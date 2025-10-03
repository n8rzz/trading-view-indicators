"""
ORB Breakout Strategy Module

This module contains the ORBBreakoutStrategy class for implementing the Opening Range Breakout
strategy for zero-day options trading.
"""
import pandas as pd
import numpy as np
import pytz
from datetime import datetime, time, timedelta, timezone
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from market_analyzer import MarketAnalyzer
from data_structures import OpportunityWindow, BreakoutSignal, ExitSignal, OpeningRange
from position_manager import PositionManager, OptionOrder, OptionType, OrderSide
from logger_config import initialize_trading_logger


class SignalType(Enum):
    ORH_BREAKOUT = "ORH_BREAKOUT"
    ORL_BREAKOUT = "ORL_BREAKOUT"
    MIDLINE_CROSS = "MIDLINE_CROSS"


logger, trading_logger, log_file_path, env_info = initialize_trading_logger(level="INFO", log_to_file=True)


class ORBBreakoutStrategy:
    """
    Opening Range Breakout Strategy for Expiring Options
    
    Strategy Logic:
    1. Calculate Opening Range High and Low (ORH/ORL)
    2. Calculate Opportunity Window
    3. Monitor for breakouts above ORH or below ORL within the Opportunity Window
    4. On ORH breakout: Sell put with strike near ORL
    5. On ORL breakout: Sell call with strike near ORH
    """
    
    def __init__(
        self, 
        symbol: str,
        opening_range_duration: int = 60, # minutes
        opportunity_window_end: time = time(12, 0, tzinfo=pytz.timezone('US/Central')), # 12:00 PM CST
        min_range_size_percent: float = 0.2, # minimum Opening Range size as % of price
        strike_offset_percent: float = 0.1, # strike offset from OR levels
        max_daily_trades: int = 1,
        days_to_expiration: int = 1,
        interval: int = 15, # minutes - candle size for data requests
        bars_df: Optional[pd.DataFrame] = None, # optional initial market data
    ):
        """
        Initialize the ORB Breakout Strategy
        
        Args:
            symbol:                     Trading symbol (e.g., 'SPY')
            opening_range_duration:     Duration of opening range in minutes
            opportunity_window_end:     End of opportunity window in minutes from market open
            min_range_size_percent:     Minimum opening range size as percentage of current price
            strike_offset_percent:      Strike price offset from OR levels as percentage
            max_daily_trades:           Maximum number of trades per day
            days_to_expiration:         Number of days until option expiration
            interval:                   Candle size in minutes for data requests (default: 15)
            bars_df:                    Optional initial market data DataFrame
        """
        self.symbol = symbol
        self.opening_range_duration = opening_range_duration
        self.opportunity_window_end = opportunity_window_end
        self.min_range_size_percent = min_range_size_percent
        self.strike_offset_percent = strike_offset_percent
        self.max_daily_trades = max_daily_trades
        self.days_to_expiration = days_to_expiration
        self.interval = interval
        self.current_bars: Optional[pd.DataFrame] = bars_df
        
        self.opening_range: Optional[OpeningRange] = None
        self.opportunity_window: Optional[OpportunityWindow] = None
        self.daily_trades: List[OptionOrder] = []
        self.breakout_signals: List[BreakoutSignal] = []
        self.last_trade_date: Optional[datetime] = None
        
        # Position management
        self.position_manager = PositionManager(symbol)
        
        self.market_open = time(8, 30)  # 8:30 AM CST
        self.market_close = time(15, 0) # 3:00 PM CST
        
        self.market_analyzer = MarketAnalyzer(timezone='US/Central')
    
    def update_bars(self, bars_df: pd.DataFrame) -> None:
        """
        Update the strategy with new market data
        
        Args:
            bars_df: DataFrame with OHLCV data
        """
        self.current_bars = bars_df
    
    
    def calculate_opening_range_high_low(self, bars_df: pd.DataFrame) -> Optional[OpeningRange]:
        """
        Calculate Opening Range High and Low from the provided bars data
        
        Args:
            bars_df: DataFrame with OHLCV data containing timestamp, open, high, low, close, volume
            
        Returns:
            OpeningRange object with ORH, ORL, and timing information
        """
        opening_range_data = self.market_analyzer.calculate_opening_range(
            bars_df, 
            self.opening_range_duration, 
            self.min_range_size_percent
        )
        
        if not opening_range_data:
            return None
        
        return OpeningRange(
            start_time=opening_range_data['start_time'],
            end_time=opening_range_data['end_time'],
            high=opening_range_data['high'],
            low=opening_range_data['low'],
            range_size=opening_range_data['range_size'],
            range_percent=opening_range_data['range_percent']
        )
    
    def calculate_and_validate_opening_range(self, bars_df: pd.DataFrame) -> Optional[OpeningRange]:
        """Calculate opening range and validate it meets requirements"""
        logger.info("Calculating opening range...")

        opening_range_data = self.market_analyzer.calculate_opening_range(
            bars_df, 
            self.opening_range_duration, 
            self.min_range_size_percent
        )
        
        if not opening_range_data: 
            logger.error("Could not calculate opening range")
            return None

        if opening_range_data.is_historical_data:
            trading_logger.log_historical_data_warning(
                symbol=self.symbol,
                data_date=str(opening_range_data.data_date),
                days_old=opening_range_data.days_old
            )
            return None

        trading_logger.log_opening_range(
            symbol=self.symbol,
            orh=opening_range_data.high,
            orl=opening_range_data.low,
            range_percent=opening_range_data.range_percent
        )

        trading_logger.log_range_analysis(
            symbol=self.symbol,
            actual_range=opening_range_data.range_size,
            required_range=opening_range_data.required_range_size,
            range_ratio=opening_range_data.range_ratio,
            current_price=opening_range_data.current_price
        )
        
        return opening_range_data
    
    def calculate_opportunity_window(self, opening_range_data: OpeningRange) -> Optional[OpportunityWindow]:
        """Calculate and validate the opportunity window"""
        logger.info("Calculating opportunity window...")
        
        opportunity_window = self.market_analyzer.calculate_opportunity_window(
            opening_range_data,
            self.opportunity_window_end
        )
        
        if not opportunity_window:
            logger.error("Could not calculate opportunity window")
            return None
        
        trading_logger.log_opportunity_window(
            symbol=self.symbol,
            start_time=str(opportunity_window.start_time),
            end_time=str(opportunity_window.end_time),
            duration_minutes=opportunity_window.duration_minutes,
            is_active=opportunity_window.is_active
        )
        
        return opportunity_window
