"""
Logging Configuration Module

This module sets up structured logging for the ORB trading bot using structlog.
It provides consistent, structured logging across all components.
"""

import structlog
import logging
import sys
from typing import Any, Dict


def setup_logging(level: str = "INFO", use_json: bool = False) -> structlog.BoundLogger:
    """
    Set up structured logging for the ORB trading bot
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        use_json: Whether to output logs in JSON format
        
    Returns:
        Configured structlog logger
    """
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, level.upper()),
    )
    
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    
    if use_json:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    return structlog.get_logger()


def get_logger(name: str = None) -> structlog.BoundLogger:
    """
    Get a structured logger instance
    
    Args:
        name: Logger name (defaults to calling module)
        
    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)


class TradingLogger:
    """Helper class for trading-specific structured logging"""
    
    def __init__(self, logger: structlog.BoundLogger):
        self.logger = logger
    
    def log_market_data(self, symbol: str, bars_count: int, date_range: Dict[str, str]) -> None:
        """Log market data fetch information"""
        self.logger.info(
            "Market data fetched",
            symbol=symbol,
            bars_count=bars_count,
            date_range=date_range
        )
    
    def log_opening_range(self, symbol: str, orh: float, orl: float, range_percent: float) -> None:
        """Log opening range calculation"""
        self.logger.info(
            "Opening range calculated",
            symbol=symbol,
            orh=round(orh, 2),
            orl=round(orl, 2),
            range_percent=round(range_percent, 2)
        )
    
    def log_range_analysis(self, symbol: str, actual_range: float, required_range: float, 
                          range_ratio: float, current_price: float) -> None:
        """Log range analysis metrics"""
        self.logger.info(
            "Range analysis",
            symbol=symbol,
            actual_range=round(actual_range, 2),
            required_range=round(required_range, 2),
            range_ratio=round(range_ratio, 2),
            current_price=round(current_price, 2)
        )
    
    def log_opportunity_window(self, symbol: str, start_time: str, end_time: str, 
                              duration_minutes: float, is_active: bool) -> None:
        """Log opportunity window information"""
        self.logger.info(
            "Opportunity window analysis",
            symbol=symbol,
            start_time=start_time,
            end_time=end_time,
            duration_minutes=round(duration_minutes, 0),
            is_active=is_active
        )
    
    def log_breakout_detected(self, symbol: str, breakout_type: str, direction: str,
                             breakout_level: float, strength: float, distance_from_midline: float) -> None:
        """Log breakout detection"""
        self.logger.warning(
            "BREAKOUT DETECTED",
            symbol=symbol,
            type=breakout_type,
            direction=direction,
            breakout_level=round(breakout_level, 2),
            strength=round(strength, 2),
            distance_from_midline=round(distance_from_midline, 2)
        )
    
    def log_no_breakout(self, symbol: str, current_price: float, orh: float, orl: float,
                       opportunity_window_active: bool) -> None:
        """Log when no breakout is detected"""
        self.logger.info(
            "No breakout detected",
            symbol=symbol,
            current_price=round(current_price, 2),
            orh=round(orh, 2),
            orl=round(orl, 2),
            opportunity_window_active=opportunity_window_active
        )
    
    def log_strategy_start(self, symbol: str, opening_range_duration: int, 
                          opportunity_window_end: str, min_range_size_percent: float) -> None:
        """Log strategy initialization"""
        self.logger.info(
            "ORB Strategy initialized",
            symbol=symbol,
            opening_range_duration=opening_range_duration,
            opportunity_window_end=opportunity_window_end,
            min_range_size_percent=min_range_size_percent
        )
