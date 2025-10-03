"""
Market Data Analysis Module

This module contains classes and methods for analyzing market data,
calculating technical indicators, and performing mathematical operations
on price data for the ORB trading strategy.
"""

import pandas as pd
import numpy as np
import pytz
from datetime import datetime, time, timedelta
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from logger_config import get_logger
from data_structures import OpportunityWindow, MarketDataResult, OpeningRange, BreakoutSignal, ExitSignal
from exit_detector import ExitDetector

logger = get_logger(__name__)


class MarketAnalyzer:
    """
    Handles mathematical calculations and analysis of market data
    
    This class encapsulates all the technical analysis and mathematical
    operations needed for the ORB trading strategy, keeping the trading
    logic separate from the calculations.
    """
    
    def __init__(self, timezone: str = 'US/Central'):
        """
        Initialize the Market Analyzer
        
        Args:
            timezone: Timezone for market data analysis (default: US/Central)
        """
        self.timezone = pytz.timezone(timezone)
        self.market_open_time = time(8, 30)  # 8:30 AM CT
        self.market_close_time = time(15, 0)  # 3:00 PM CT
        self.exit_detector = ExitDetector(self.timezone)
    
    def calculate_opening_range(
        self, 
        bars_df: pd.DataFrame, 
        opening_range_duration: int = 60,
        min_range_size_percent: float = 0.2
    ) -> Optional[OpeningRange]:
        """
        Calculate Opening Range High and Low from the provided bars data
        
        Args:
            bars_df: DataFrame with OHLCV data containing timestamp, open, high, low, close, volume
            opening_range_duration: Duration of opening range in minutes (default: 60)
            min_range_size_percent: Minimum opening range size as percentage of current price
            
        Returns:
            Dictionary with opening range data or None if calculation fails
        """
        if bars_df.empty:
            logger.warning("Cannot calculate opening range from empty data")
            return None
        
        try:
            # Step 1: Get validated market data
            market_data_result = self._get_validated_market_data(bars_df)
            if not market_data_result:
                return None
            
            # Step 2: Extract opening range period
            opening_range_data = self._extract_opening_range_period(
                market_data_result.data, opening_range_duration
            )
            
            if opening_range_data is None or opening_range_data.empty:
                return None
            
            # Step 3: Calculate ORH/ORL and validate range
            orh, orl = self._calculate_orh_orl(opening_range_data)
            range_metrics = self._calculate_range_metrics(
                orh, orl, opening_range_data, min_range_size_percent
            )
            if not range_metrics:
                return None
            
            # Step 4: Build and return OpeningRange object
            return self._build_opening_range_object(
                market_data_result, opening_range_data, orh, orl, 
                range_metrics, opening_range_duration, min_range_size_percent
            )
            
        except Exception as e:
            logger.error(f"Error calculating opening range: {e}")
            return None
    
    def _get_validated_market_data(self, bars_df: pd.DataFrame) -> Optional[MarketDataResult]:
        """
        Get and validate market data for opening range calculation
        
        Args:
            bars_df: Raw bars DataFrame
            
        Returns:
            MarketDataResult if valid, None otherwise
        """
        processed_bars = self._prepare_market_data(bars_df)
        if processed_bars is None or processed_bars.empty:
            return None
        
        market_data_result = self._filter_today_market_hours(processed_bars)
        if market_data_result.data.empty:
            logger.warning("No market hours data found for today")
            return None
        
        if market_data_result.is_historical:
            logger.warning(
                "Trading disabled - using historical data",
                data_date=market_data_result.data_date.isoformat(),
                days_old=market_data_result.days_old,
                reason="Historical data should not trigger live trades"
            )
        
        return market_data_result
    
    def _calculate_orh_orl(self, opening_range_data: pd.DataFrame) -> Tuple[float, float]:
        """
        Calculate Opening Range High and Low from opening range data
        
        Args:
            opening_range_data: DataFrame with opening range bars
            
        Returns:
            Tuple of (ORH, ORL)
        """
        orh = opening_range_data['high'].max()
        orl = opening_range_data['low'].min()
        return orh, orl
    
    def _build_opening_range_object(self, market_data_result: MarketDataResult, 
                                   opening_range_data: pd.DataFrame, orh: float, orl: float,
                                   range_metrics: Dict, opening_range_duration: int, 
                                   min_range_size_percent: float) -> OpeningRange:
        """
        Build the final OpeningRange object
        
        Args:
            market_data_result: Validated market data result
            opening_range_data: Opening range period data
            orh: Opening range high
            orl: Opening range low
            range_metrics: Calculated range metrics
            opening_range_duration: Duration in minutes
            min_range_size_percent: Minimum range size percentage
            
        Returns:
            OpeningRange object
        """
        opening_range_start = market_data_result.data['timestamp'].min()
        opening_range_end = opening_range_start + timedelta(minutes=opening_range_duration)
        required_range_size = range_metrics['current_price'] * (min_range_size_percent / 100)
        range_ratio = range_metrics['range_size'] / required_range_size if required_range_size > 0 else 0
        
        result = OpeningRange(
            start_time=opening_range_start,
            end_time=opening_range_end,
            high=orh,
            low=orl,
            range_size=range_metrics['range_size'],
            range_percent=range_metrics['range_percent'],
            current_price=range_metrics['current_price'],
            bars_count=len(opening_range_data),
            required_range_size=required_range_size,
            range_ratio=range_ratio,
            is_historical_data=market_data_result.is_historical,
            data_date=market_data_result.data_date,
            days_old=market_data_result.days_old
        )
        
        logger.info(f"Opening Range calculated: ORH={orh:.2f}, ORL={orl:.2f}, Range={range_metrics['range_percent']:.2f}%")
        return result
    
    def _prepare_market_data(self, bars_df: pd.DataFrame) -> Optional[pd.DataFrame]:
        """
        Prepare and validate market data for analysis
        
        Args:
            bars_df: Raw bars DataFrame
            
        Returns:
            Processed DataFrame or None if preparation fails
        """
        try:
            df = bars_df.copy()
            
            if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Set timezone to US/Central if not already set
            if df['timestamp'].dt.tz is None:
                df['timestamp'] = df['timestamp'].dt.tz_localize(self.timezone)
            
            required_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                logger.error(f"Missing required columns: {missing_columns}")
                return None
            
            df = df.sort_values('timestamp')
            
            return df
            
        except Exception as e:
            logger.error(f"Error preparing market data: {e}")
            return None
    
    def _filter_today_market_hours(self, bars_df: pd.DataFrame) -> MarketDataResult:
        """
        Filter bars for the most recent trading day's data within market hours
        
        Args:
            bars_df: Processed bars DataFrame
            
        Returns:
            MarketDataResult with filtered data and historical flag
        """
        today = datetime.now(self.timezone)
        today_date = today.date()
        
        # First try to get today's data within market hours
        today_bars = bars_df[
            (bars_df['timestamp'].dt.date == today_date) &
            (bars_df['timestamp'].dt.time >= self.market_open_time) &
            (bars_df['timestamp'].dt.time <= self.market_close_time)
        ].copy()
        
        # If no data for today, get the most recent trading day's data
        if today_bars.empty:
            most_recent_date = bars_df['timestamp'].dt.date.max()
            days_old = (today_date - most_recent_date).days

            logger.warning(
                "Using historical data instead of today's data",
                today_date=today_date.isoformat(),
                most_recent_date=most_recent_date.isoformat(),
                days_old=days_old,
                reason="No market data available for today"
            )
            
            today_bars = bars_df[
                (bars_df['timestamp'].dt.date == most_recent_date) &
                (bars_df['timestamp'].dt.time >= self.market_open_time) &
                (bars_df['timestamp'].dt.time <= self.market_close_time)
            ].copy()
            
            return MarketDataResult(
                data=today_bars,
                is_historical=True,
                data_date=datetime.combine(most_recent_date, datetime.min.time()).replace(tzinfo=self.timezone),
                days_old=days_old
            )
        
        logger.info(
            "Using today's market data",
            date=today_date.isoformat(),
            bars_count=len(today_bars)
        )
        
        return MarketDataResult(
            data=today_bars,
            is_historical=False,
            data_date=datetime.combine(today_date, datetime.min.time()).replace(tzinfo=self.timezone),
            days_old=0
        )
    
    def _extract_opening_range_period(
        self, 
        today_bars: pd.DataFrame, 
        opening_range_duration: int
    ) -> Optional[pd.DataFrame]:
        """
        Extract bars within the opening range period
        
        Args:
            today_bars: Today's market hours bars
            opening_range_duration: Duration of opening range in minutes
            
        Returns:
            DataFrame with opening range period bars or None if no data
        """
        if today_bars.empty:
            return None
        
        opening_range_start = today_bars['timestamp'].min()
        opening_range_end = opening_range_start + timedelta(minutes=opening_range_duration)
        opening_range_bars = today_bars[
            today_bars['timestamp'] <= opening_range_end
        ]
        
        if opening_range_bars.empty:
            logger.warning("No data found within opening range period")
            return None
        
        return opening_range_bars
    
    def _calculate_range_metrics(
        self, 
        orh: float, 
        orl: float, 
        opening_range_data: pd.DataFrame,
        min_range_size_percent: float
    ) -> Optional[Dict]:
        """
        Calculate range size and percentage metrics
        
        Args:
            orh: Opening Range High
            orl: Opening Range Low
            opening_range_data: DataFrame with opening range period data
            min_range_size_percent: Minimum range size percentage threshold
            
        Returns:
            Dictionary with range metrics or None if range is too small
        """
        range_size = orh - orl
        current_price = opening_range_data['close'].iloc[-1]  # Last close price in opening range
        range_percent = (range_size / current_price) * 100 if current_price > 0 else 0
        
        if range_percent < min_range_size_percent:
            logger.warning(f"Opening range too small: {range_percent:.2f}% < {min_range_size_percent}%")
            return None
        
        return {
            'range_size': range_size,
            'range_percent': range_percent,
            'current_price': current_price
        }
    
    def calculate_opportunity_window(
        self, 
        opening_range_data: OpeningRange,
        opportunity_window_end_time: time
    ) -> Optional[OpportunityWindow]:
        """
        Calculate the opportunity window based on opening range data
        
        Args:
            opening_range_data: OpeningRange dataclass with opening range information
            opportunity_window_end_time: End time for the opportunity window
            
        Returns:
            OpportunityWindow dataclass or None if calculation fails
        """
        try:
            if not opening_range_data:
                return None
            
            start_time = self._normalize_timezone(opening_range_data.end_time)
            today = datetime.now(self.timezone).date()
            end_datetime = datetime.combine(today, opportunity_window_end_time)
            end_time = self._normalize_timezone(end_datetime)
            midline = (opening_range_data.high + opening_range_data.low) / 2
            window_duration = end_time - start_time
            
            return OpportunityWindow(
                start_time=start_time,
                end_time=end_time,
                midline=midline,
                duration_minutes=window_duration.total_seconds() / 60,
                is_active=self._is_opportunity_window_active(start_time, end_time)
            )
            
        except Exception as e:
            logger.error(f"Error calculating opportunity window: {e}")
            return None
    
    def _normalize_timezone(self, dt: datetime) -> datetime:
        """
        Normalize a datetime to the analyzer's timezone
        
        Args:
            dt: Datetime to normalize
            
        Returns:
            Datetime in the analyzer's timezone
        """
        if dt.tzinfo is None:
            return self.timezone.localize(dt)
        return dt.astimezone(self.timezone)
    
    def _is_opportunity_window_active(self, start_time: datetime, end_time: datetime) -> bool:
        """
        Check if we're currently within the opportunity window
        
        Args:
            start_time: Opportunity window start time
            end_time: Opportunity window end time
            
        Returns:
            True if currently within the opportunity window
        """
        now = datetime.now(self.timezone)
        return start_time <= now <= end_time
    
    def is_within_opportunity_window(self, opportunity_window: OpportunityWindow) -> bool:
        """
        Check if current time is within the opportunity window
        
        Args:
            opportunity_window: OpportunityWindow dataclass instance
            
        Returns:
            True if within opportunity window, False otherwise
        """
        if not opportunity_window:
            return False
        
        return opportunity_window.is_currently_active(self.timezone)
    
    def detect_breakout(
        self, 
        current_price: float, 
        opening_range_data: OpeningRange,
        opportunity_window: OpportunityWindow
    ) -> Optional[BreakoutSignal]:
        """
        Detect if current price has broken out of the opening range
        
        Args:
            current_price: Current market price
            opening_range_data: OpeningRange dataclass instance
            opportunity_window: OpportunityWindow dataclass instance
            
        Returns:
            BreakoutSignal dataclass with breakout information or None if no breakout
        """
        try:
            if not opening_range_data or not opportunity_window:
                return None
            
            if not self.is_within_opportunity_window(opportunity_window):
                return None
            
            orh = opening_range_data.high
            orl = opening_range_data.low
            midline = opportunity_window.midline
            
            if current_price > orh:
                return BreakoutSignal(
                    type='ORH_BREAKOUT',
                    current_price=current_price,
                    breakout_level=orh,
                    direction='UP',
                    timestamp=datetime.now(self.timezone),
                    distance_from_midline=current_price - midline,
                    breakout_strength=(current_price - orh) / orh * 100  # Percentage above ORH
                )
            
            if current_price < orl:
                return BreakoutSignal(
                    type='ORL_BREAKOUT',
                    current_price=current_price,
                    breakout_level=orl,
                    direction='DOWN',
                    timestamp=datetime.now(self.timezone),
                    distance_from_midline=current_price - midline,
                    breakout_strength=(orl - current_price) / orl * 100  # Percentage below ORL
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error detecting breakout: {e}")
            return None
    
    def get_current_price(self, bars_df: pd.DataFrame) -> Optional[float]:
        """
        Get the current market price from the latest bar
        
        Args:
            bars_df: DataFrame with market data
            
        Returns:
            Current price (close of latest bar) or None if no data
        """
        try:
            if bars_df.empty:
                return None
            
            latest_bar = bars_df.iloc[-1]
            return float(latest_bar['close'])
            
        except Exception as e:
            logger.error(f"Error getting current price: {e}")
            return None
    
    def detect_exit_signal(self, current_price: float, opening_range_data: OpeningRange, 
                          opportunity_window: OpportunityWindow, has_short_call: bool = False, 
                          has_short_put: bool = False) -> Optional[ExitSignal]:
        """
        Detect exit signals based on the strategy rules:
        - Price has broken out of the OR within the Opportunity window
        - Price has re-entered the opening range and has crossed the opportunity window midline
        
        Args:
            current_price: Current market price
            opening_range_data: Opening range data (ORH, ORL)
            opportunity_window: Opportunity window data
            has_short_call: Whether we have an open short call position
            has_short_put: Whether we have an open short put position
            
        Returns:
            ExitSignal if exit conditions are met, None otherwise
        """
        try:
            if not opportunity_window.is_active:
                return None
            
            return self.exit_detector.detect_midline_cross_exit(
                current_price, opening_range_data, opportunity_window, has_short_call, has_short_put
            )
            
        except Exception as e:
            logger.error(f"Error detecting exit signal: {e}")
            return None
