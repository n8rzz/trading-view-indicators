"""
Logging Configuration Module

This module sets up structured logging for the ORB trading bot using structlog.
It provides consistent, structured logging across all components.
"""

import structlog
import logging
import sys
import os
from typing import Any, Dict


def _is_cloud_environment() -> bool:
    """
    Detect if we're running in a cloud environment
    
    Returns:
        True if running in cloud environment, False otherwise
    """
    environment = os.getenv('ENVIRONMENT', 'local').lower()
    return environment in ['cloud', 'production', 'staging']


def setup_logging(level: str = "INFO", use_json: bool = False, log_to_file: bool = True, force_json: bool = False) -> structlog.BoundLogger:
    """
    Set up structured logging for the ORB trading bot
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        use_json: Whether to output logs in JSON format
        log_to_file: Whether to write logs to a file
        force_json: Force JSON output (useful for cloud deployments)
        
    Returns:
        Configured structlog logger
    """
    # Detect cloud environment
    is_cloud_env = _is_cloud_environment()
    
    # Set up handlers
    handlers = []
    
    # Console handler (always enabled)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    handlers.append(console_handler)
    
    # File handler (if enabled and not in cloud environment)
    if log_to_file and not is_cloud_env:
        import os
        from datetime import datetime

        # Create logs directory in the orb-bot directory
        log_dir = os.path.join(os.path.dirname(__file__), "logs")
        
        os.makedirs(log_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = os.path.join(log_dir, f"orb_trading_bot_{timestamp}.log")
        file_handler = logging.FileHandler(log_file)
        
        file_handler.setLevel(getattr(logging, level.upper()))
        handlers.append(file_handler)
    
    # Configure logging with handlers
    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, level.upper()),
        handlers=handlers,
        force=True  # Override any existing configuration
    )
    
    # Base processors for all outputs
    base_processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    
    # Configure structlog with appropriate renderer
    # In cloud environments, always use JSON for better log aggregation
    if use_json or force_json or is_cloud_env:
        processors = base_processors + [structlog.processors.JSONRenderer()]
    else:
        # Use ConsoleRenderer for console output (works well with both console and file)
        processors = base_processors + [structlog.dev.ConsoleRenderer(colors=False)]
    
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


def get_log_file_path() -> str:
    """
    Get the current log file path
    
    Returns:
        Path to the current log file, or "stdout" if in cloud environment
    """
    if _is_cloud_environment():
        return "stdout"
    
    from datetime import datetime
    
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    timestamp = datetime.now().strftime("%Y%m%d")
    return os.path.join(log_dir, f"orb_trading_bot_{timestamp}.log")


def get_environment_info() -> Dict[str, Any]:
    """
    Get environment information for logging context
    
    Returns:
        Dictionary with environment information
    """
    environment = os.getenv('ENVIRONMENT', 'local')
    is_cloud = _is_cloud_environment()
    
    info = {
        "environment": environment,
        "is_cloud": is_cloud,
        "log_output": "stdout" if is_cloud else "file",
    }
    
    return info


def initialize_trading_logger(level: str = "INFO", log_to_file: bool = True) -> tuple[structlog.BoundLogger, "TradingLogger", str, Dict[str, Any]]:
    """
    Initialize the complete logging system for trading applications
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Whether to write logs to a file
        
    Returns:
        Tuple of (logger, trading_logger, log_file_path, env_info)
    """
    logger = setup_logging(level=level, log_to_file=log_to_file)
    trading_logger = TradingLogger(logger)
    log_file_path = get_log_file_path()
    env_info = get_environment_info()
    
    logger.info("Logging initialized", log_file=log_file_path, **env_info)
    
    return logger, trading_logger, log_file_path, env_info


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
    
    def log_historical_data_warning(self, symbol: str, data_date: str, days_old: int) -> None:
        """Log warning when using historical data"""
        self.logger.warning(
            "TRADING DISABLED - Historical data detected",
            symbol=symbol,
            data_date=data_date,
            days_old=days_old,
            reason="Historical data should not trigger live trades"
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
