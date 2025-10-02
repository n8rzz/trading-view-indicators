"""
Alpaca API Client for ORB Trading Bot

This module provides a clean interface to the Alpaca API for fetching market data
and executing trades. It handles authentication, data fetching, and error handling.
"""

import os
import pandas as pd
import pytz
from typing import Optional, List
from datetime import datetime, timedelta
from dotenv import load_dotenv
from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from logger_config import get_logger

logger = get_logger(__name__)


class AlpacaClient:
    """
    Wrapper class for Alpaca API interactions
    
    Handles authentication, data fetching, and provides a clean interface
    for the ORB trading strategy.
    """
    
    def __init__(self, use_paper_trading: bool = True):
        """
        Initialize Alpaca client
        
        Args:
            use_paper_trading: If True, uses paper trading environment
        """
        self.use_paper_trading = use_paper_trading
        self.client: Optional[StockHistoricalDataClient] = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Alpaca data client with environment variables"""
        load_dotenv()
        
        api_key = os.getenv('ALPACA_API_KEY')
        secret_key = os.getenv('ALPACA_SECRET_KEY')
        
        if not api_key or not secret_key:
            raise ValueError(
                "ALPACA_API_KEY and ALPACA_SECRET_KEY must be set in environment variables. "
                "Create a .env file with your Alpaca credentials."
            )
        
        try:
            self.client = StockHistoricalDataClient(api_key, secret_key)
            logger.info(f"Alpaca client initialized successfully (Paper Trading: {self.use_paper_trading})")
        except Exception as e:
            logger.error(f"Failed to initialize Alpaca client: {e}")
            raise
    
    def fetch_bars(
        self, 
        symbol: str, 
        limit: int = 100,
        timeframe: TimeFrame = TimeFrame.Minute
    ) -> pd.DataFrame:
        """
        Fetch historical bars for a symbol
        
        Args:
            symbol: Stock symbol (e.g., 'SPY')
            limit: Number of bars to fetch (default: 100)
            timeframe: Timeframe for bars (default: 1 minute)
            
        Returns:
            DataFrame with OHLCV data and timestamp
        """
        if not self.client:
            raise RuntimeError("Alpaca client not initialized")
        
        try:
            end_time = datetime.now()
            # Fetch data for the last 5 days to ensure 100 bars
            start_time = end_time - timedelta(days=5)  
            
            request_params = StockBarsRequest(
                symbol_or_symbols=[symbol],
                timeframe=timeframe,
                start=start_time,
                end=end_time,
                limit=limit
            )
            
            bars = self.client.get_stock_bars(request_params)
            df = bars.df
            
            if df.empty:
                logger.warning(f"No data returned for symbol {symbol}")
                return pd.DataFrame()
            
            # Reset index to get symbol and timestamp as columns 
            df = df.reset_index()
            df = df.sort_values('timestamp')
            
            logger.info(f"Fetched {len(df)} bars for {symbol}")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching bars for {symbol}: {e}")
            return pd.DataFrame()
    
    def fetch_today_bars(
        self, 
        symbol: str,
        timeframe: TimeFrame = TimeFrame.Minute
    ) -> pd.DataFrame:
        """
        Fetch bars for today's trading session
        
        Args:
            symbol: Stock symbol (e.g., 'SPY')
            timeframe: Timeframe for bars (default: 1 minute)
            
        Returns:
            DataFrame with today's OHLCV data
        """
        # Get today's date in Eastern Time (market timezone) since US stock markets operate on ET
        eastern_tz = pytz.timezone('US/Eastern')
        today = datetime.now(eastern_tz).date()
        # Market open and close times in Eastern Time
        market_open = datetime.combine(today, datetime.min.time().replace(hour=9, minute=30))
        market_close = datetime.combine(today, datetime.min.time().replace(hour=16, minute=0))
        # Convert to UTC for API call
        market_open_utc = eastern_tz.localize(market_open).astimezone(pytz.UTC)
        market_close_utc = eastern_tz.localize(market_close).astimezone(pytz.UTC)
        
        try:
            request_params = StockBarsRequest(
                symbol_or_symbols=[symbol],
                timeframe=timeframe,
                start=market_open_utc,
                end=market_close_utc
            )
            
            bars = self.client.get_stock_bars(request_params)
            df = bars.df
            
            if df.empty:
                logger.warning(f"No data returned for {symbol} today")
                return pd.DataFrame()
            
            df = df.reset_index()
            df = df.sort_values('timestamp')
            
            logger.info(f"Fetched {len(df)} bars for {symbol} today")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching today's bars for {symbol}: {e}")
            return pd.DataFrame()
    
    def is_market_open(self) -> bool:
        """
        Check if the market is currently open
        
        Returns:
            True if market is open, False otherwise
        """
        eastern_tz = pytz.timezone('US/Eastern')
        now = datetime.now(eastern_tz)
        
        # Market hours: 9:30 AM - 4:00 PM ET, Monday-Friday
        market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
        market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
        
        # Check if it's a weekday and within market hours
        is_weekday = now.weekday() < 5  # Monday = 0, Friday = 4
        is_market_hours = market_open <= now <= market_close
        
        return is_weekday and is_market_hours
    
    def get_market_status(self) -> dict:
        """
        Get current market status information
        
        Returns:
            Dictionary with market status details
        """
        eastern_tz = pytz.timezone('US/Eastern')
        now = datetime.now(eastern_tz)
        
        market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
        market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
        
        is_weekday = now.weekday() < 5
        is_market_hours = market_open <= now <= market_close
        is_open = is_weekday and is_market_hours
        
        return {
            'is_open': is_open,
            'is_weekday': is_weekday,
            'is_market_hours': is_market_hours,
            'current_time': now,
            'market_open': market_open,
            'market_close': market_close,
            'timezone': 'US/Eastern'
        }
