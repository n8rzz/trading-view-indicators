#!/usr/bin/env python3
"""
Test script to demonstrate structured logging capabilities
"""

from logger_config import setup_logging, TradingLogger
import time

def test_structured_logging():
    """Test structured logging with different output formats"""
    
    print("=== Testing Console Output (Default) ===")
    logger = setup_logging(level="INFO", use_json=False)
    trading_logger = TradingLogger(logger)
    
    # Test basic logging
    logger.info("Testing basic structured logging")
    
    # Test trading-specific logging
    trading_logger.log_strategy_start(
        symbol="SPY",
        opening_range_duration=60,
        opportunity_window_end="12:00:00",
        min_range_size_percent=0.2
    )
    
    trading_logger.log_market_data(
        symbol="SPY",
        bars_count=100,
        date_range={"start": "2025-10-01 08:30:00", "end": "2025-10-01 09:51:00"}
    )
    
    trading_logger.log_opening_range(
        symbol="SPY",
        orh=450.25,
        orl=448.75,
        range_percent=0.33
    )
    
    trading_logger.log_breakout_detected(
        symbol="SPY",
        breakout_type="ORH_BREAKOUT",
        direction="UP",
        breakout_level=450.25,
        strength=0.15,
        distance_from_midline=0.50
    )
    
    print("\n=== Testing JSON Output ===")
    logger_json = setup_logging(level="INFO", use_json=True)
    trading_logger_json = TradingLogger(logger_json)
    
    # Test JSON logging
    trading_logger_json.log_no_breakout(
        symbol="SPY",
        current_price=449.50,
        orh=450.25,
        orl=448.75,
        opportunity_window_active=True
    )

if __name__ == "__main__":
    test_structured_logging()
