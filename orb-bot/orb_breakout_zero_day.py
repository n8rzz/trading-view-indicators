"""
ORB Breakout Zero Day Options Strategy

This strategy implements the Opening Range Breakout (ORB) strategy for zero-day options trading:
- When price crosses above ORH (Opening Range High), sell a put with strike near ORL
- When price crosses below ORL (Opening Range Low), sell a call with strike near ORH

Based on the TradingView Pine Script indicator: orb-with-opportunity-window.pine
"""
import pandas as pd
import numpy as np
import pytz
from datetime import datetime, time, timedelta, timezone
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from alpaca_client import AlpacaClient
from market_analyzer import MarketAnalyzer, OpportunityWindow, BreakoutSignal
from logger_config import setup_logging, TradingLogger

logger = setup_logging(level="INFO")
trading_logger = TradingLogger(logger)


class OptionType(Enum):
    CALL = "CALL"
    PUT = "PUT"


class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"


class SignalType(Enum):
    ORH_BREAKOUT = "ORH_BREAKOUT"
    ORL_BREAKOUT = "ORL_BREAKOUT"


@dataclass
class OptionOrder:
    """Represents an options order"""
    option_type: OptionType
    price: float
    quantity: int
    reason: str
    side: OrderSide
    strike: float
    symbol: str
    timestamp: datetime


@dataclass
class OpeningRange:
    """Opening Range data structure"""
    end_time: datetime
    high: float
    low: float
    range_percent: float
    range_size: float
    start_time: datetime


@dataclass
class BreakoutSignal:
    """Breakout signal data structure"""
    current_price: float
    orh: float
    orl: float
    price: float
    signal_type: SignalType
    timestamp: datetime


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
        """
        self.symbol = symbol
        self.opening_range_duration = opening_range_duration
        self.opportunity_window_end = opportunity_window_end
        self.min_range_size_percent = min_range_size_percent
        self.strike_offset_percent = strike_offset_percent
        self.max_daily_trades = max_daily_trades
        self.days_to_expiration = days_to_expiration
        
        # State variables
        self.opening_range: Optional[OpeningRange] = None
        self.opportunity_window: Optional[OpportunityWindow] = None
        self.daily_trades: List[OptionOrder] = []
        self.breakout_signals: List[BreakoutSignal] = []
        self.last_trade_date: Optional[datetime] = None
        
        # Market hours (assuming US market)
        self.market_open = time(8, 30)  # 8:30 AM CST
        self.market_close = time(15, 0) # 3:00 PM CST
        
        self.alpaca_client = AlpacaClient(use_paper_trading=True)
        self.market_analyzer = MarketAnalyzer(timezone='US/Central')
    
    def fetch_latest_bars(self, limit: int = 100) -> pd.DataFrame:
        """
        Fetch the latest bars for the symbol
        
        Args:
            limit: Number of bars to fetch (default: 100)
            
        Returns:
            DataFrame with OHLCV data
        """
        return self.alpaca_client.fetch_bars(self.symbol, limit=limit)
    
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
        

def main():
    """
    Example usage of the ORB Breakout Strategy
    """
    strategy = ORBBreakoutStrategy(
        symbol="SPY",
        opening_range_duration=60,              # 1 hour opening range
        opportunity_window_end=time(12, 0, tzinfo=pytz.timezone('US/Central')),     # 12:00 PM CST
        min_range_size_percent=0.2,             # 0.2% minimum range
        strike_offset_percent=0.1,              # 0.1% strike offset
        max_daily_trades=2,
        days_to_expiration=1
    )
    
    trading_logger.log_strategy_start(
        symbol=strategy.symbol,
        opening_range_duration=strategy.opening_range_duration,
        opportunity_window_end=str(strategy.opportunity_window_end),
        min_range_size_percent=strategy.min_range_size_percent
    )

    logger.info("Fetching latest 100 bars...")
    
    bars_df = strategy.fetch_latest_bars(limit=100)
    
    if bars_df.empty:
        logger.error("No bars data available")
        return
        
    trading_logger.log_market_data(
        symbol=strategy.symbol,
        bars_count=len(bars_df),
        date_range={
            "start": str(bars_df['timestamp'].min()),
            "end": str(bars_df['timestamp'].max())
        }
    )

    logger.info("Calculating opening range...")

    opening_range = strategy.calculate_opening_range_high_low(bars_df)
    
    if not opening_range:
        logger.error("Could not calculate opening range")
        return
    
    bars_df = strategy.fetch_latest_bars(limit=100)
    opening_range_data = strategy.market_analyzer.calculate_opening_range(
        bars_df, 
        strategy.opening_range_duration, 
        strategy.min_range_size_percent
    )
    
    trading_logger.log_opening_range(
        symbol=strategy.symbol,
        orh=opening_range.high,
        orl=opening_range.low,
        range_percent=opening_range.range_percent
    )
    
    if not opening_range_data: 
        return

    trading_logger.log_range_analysis(
        symbol=strategy.symbol,
        actual_range=opening_range_data['range_size'],
        required_range=opening_range_data['required_range_size'],
        range_ratio=opening_range_data['range_ratio'],
        current_price=opening_range_data['current_price']
    )
    
    logger.info("Calculating opportunity window...")
    
    opportunity_window = strategy.market_analyzer.calculate_opportunity_window(
        opening_range_data,
        strategy.opportunity_window_end
    )
    
    if not opportunity_window:
        logger.error("Could not calculate opportunity window")
        return
    
    # Log opportunity window analysis
    trading_logger.log_opportunity_window(
        symbol=strategy.symbol,
        start_time=str(opportunity_window.start_time),
        end_time=str(opportunity_window.end_time),
        duration_minutes=opportunity_window.duration_minutes,
        is_active=opportunity_window.is_active
    )
    
    current_price = strategy.market_analyzer.get_current_price(bars_df)

    if not current_price:
        logger.error("Could not get current price")
        return
    
    logger.info("Looking for breakouts...")
    
    breakout = strategy.market_analyzer.detect_breakout(
        current_price,
        opening_range_data,
        opportunity_window
    )
    
    if breakout:
        trading_logger.log_breakout_detected(
            symbol=strategy.symbol,
            breakout_type=breakout.type,
            direction=breakout.direction,
            breakout_level=breakout.breakout_level,
            strength=breakout.breakout_strength,
            distance_from_midline=breakout.distance_from_midline
        )
        return

    trading_logger.log_no_breakout(
        symbol=strategy.symbol,
        current_price=current_price,
        orh=opening_range_data['high'],
        orl=opening_range_data['low'],
        opportunity_window_active=opportunity_window.is_active
    )


if __name__ == "__main__":
    main()
