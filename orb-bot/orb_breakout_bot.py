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
from orb_signal_manager import ORBSignalManager, ORBContext

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


def process_signals_with_manager(strategy: ORBBreakoutStrategy, bars_df: pd.DataFrame,
                                opening_range_data: OpeningRange, opportunity_window: OpportunityWindow) -> None:
    """Process all signals using the signal manager"""
    signal_manager = ORBSignalManager(strategy)
    context = ORBContext(opening_range_data, opportunity_window)
    
    all_signals = signal_manager.process_all_signals(bars_df, context)
    
    for signal in all_signals['entry']:
        logger.info(f"Entry signal detected: {signal.metadata['breakout_type']} - {signal.metadata['strategy_action']}")
    
    for signal in all_signals['exit']:
        logger.info(f"Exit signal detected: {signal.metadata['exit_type']} - {signal.metadata['strategy_action']}")
        if strategy.position_manager.has_positions():
            mock_exit_signal = type('MockExitSignal', (), {
                'type': signal.metadata['exit_type'],
                'current_price': signal.metadata['current_price'],
                'orh': signal.metadata['orh'],
                'orl': signal.metadata['orl'],
                'opportunity_window_midline': signal.metadata['midline'],
                'reason': signal.metadata['reason']
            })()
            strategy.position_manager.close_all_positions(mock_exit_signal)


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
    
    process_signals_with_manager(strategy, bars_df, opening_range_data, opportunity_window)

if __name__ == "__main__":
    main()
