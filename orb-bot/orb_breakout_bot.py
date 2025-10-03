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
from alpaca.data import TimeFrame
from market_analyzer import MarketAnalyzer
from data_structures import OpportunityWindow, BreakoutSignal, ExitSignal, OpeningRange
from position_manager import PositionManager, OptionOrder, OptionType, OrderSide
from logger_config import initialize_trading_logger
from orb_strategy import ORBBreakoutStrategy, SignalType

logger, trading_logger, log_file_path, env_info = initialize_trading_logger(level="INFO", log_to_file=True)


def create_strategy() -> ORBBreakoutStrategy:
    """Create and initialize the ORB Breakout Strategy"""
    strategy = ORBBreakoutStrategy(
        symbol="SPY",
        opening_range_duration=60,             
        opportunity_window_end=time(12, 0, tzinfo=pytz.timezone('US/Central')),
        min_range_size_percent=0.2,
        strike_offset_percent=0.1,
        max_daily_trades=2,
        days_to_expiration=1,
        interval=15
    )
    
    trading_logger.log_strategy_start(
        symbol=strategy.symbol,
        opening_range_duration=strategy.opening_range_duration,
        opportunity_window_end=str(strategy.opportunity_window_end),
        min_range_size_percent=strategy.min_range_size_percent
    )
    
    return strategy


def fetch_and_validate_market_data(symbol: str, interval: int) -> Optional[pd.DataFrame]:
    """Fetch market data and validate it's available"""
    logger.info(f"Fetching latest 100 bars for {symbol} with {interval}-minute intervals...")
    
    from alpaca_client import AlpacaClient
    from alpaca.data import TimeFrame
    
    alpaca_client = AlpacaClient(use_paper_trading=True)
    timeframe = TimeFrame(interval, TimeFrame.Minute.unit)
    bars_df = alpaca_client.fetch_today_bars(symbol, timeframe=timeframe)
    
    if bars_df.empty:
        logger.error("No bars data available")
        return None
        
    trading_logger.log_market_data(
        symbol=symbol,
        bars_count=len(bars_df),
        date_range={
            "start": str(bars_df['timestamp'].min()),
            "end": str(bars_df['timestamp'].max())
        }
    )
    
    return bars_df


def detect_and_log_breakouts(strategy: ORBBreakoutStrategy, bars_df: pd.DataFrame, 
                            opening_range_data: OpeningRange, opportunity_window: OpportunityWindow) -> None:
    """Detect breakouts and log the results"""
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
    
    if not breakout:
        trading_logger.log_no_breakout(
            symbol=strategy.symbol,
            current_price=current_price,
            orh=opening_range_data.high,
            orl=opening_range_data.low,
            opportunity_window_active=opportunity_window.is_active
        )
        return

    trading_logger.log_breakout_detected(
        symbol=strategy.symbol,
        breakout_type=breakout.type,
        direction=breakout.direction,
        breakout_level=breakout.breakout_level,
        strength=breakout.breakout_strength,
        distance_from_midline=breakout.distance_from_midline
    )


def detect_and_log_exit_signals(strategy: ORBBreakoutStrategy, bars_df: pd.DataFrame,
                               opening_range_data: OpeningRange, opportunity_window: OpportunityWindow) -> None:
    """Detect exit signals and close positions if conditions are met"""
    current_price = strategy.market_analyzer.get_current_price(bars_df)

    if not current_price:
        logger.error("Could not get current price for exit detection")
        return

    logger.info("Checking for exit signals...")
    
    exit_signal = strategy.market_analyzer.detect_exit_signal(
        current_price=current_price,
        opening_range_data=opening_range_data,
        opportunity_window=opportunity_window,
        has_short_call=strategy.position_manager.has_short_call,
        has_short_put=strategy.position_manager.has_short_put
    )

    if not exit_signal:
        return
    
    trading_logger.log_exit_signal_detected(
        symbol=strategy.symbol,
        exit_type=exit_signal.type,
        current_price=exit_signal.current_price,
        orh=exit_signal.orh,
        orl=exit_signal.orl,
        midline=exit_signal.opportunity_window_midline,
        reason=exit_signal.reason
    )
    
    if not strategy.position_manager.has_positions():
        return
        
    strategy.position_manager.close_all_positions(exit_signal)


def main():
    """
    Main execution flow for the ORB Breakout Strategy
    """
    strategy = create_strategy()
    bars_df = fetch_and_validate_market_data(strategy.symbol, strategy.interval)
    
    if bars_df is None or bars_df.empty:
        logger.error("Failed to fetch or validate market data - exiting")
        return
    
    strategy.update_bars(bars_df)
    opening_range_data = strategy.calculate_and_validate_opening_range(bars_df)
    
    if not opening_range_data:
        return
    
    opportunity_window = strategy.calculate_opportunity_window(opening_range_data)
    
    if not opportunity_window:
        return
    
    detect_and_log_breakouts(strategy, bars_df, opening_range_data, opportunity_window)
    detect_and_log_exit_signals(strategy, bars_df, opening_range_data, opportunity_window)

if __name__ == "__main__":
    main()
