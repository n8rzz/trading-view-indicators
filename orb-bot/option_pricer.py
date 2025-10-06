"""
Option Pricing Module

This module handles option contract pricing data retrieval and analysis.
It calculates target strikes based on ORB levels and fetches option pricing data.
"""

import os
import pandas as pd
import pytz
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from dataclasses import dataclass
from dotenv import load_dotenv
from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import OptionBarsRequest
from alpaca.data.timeframe import TimeFrame
from logger_config import get_logger

logger = get_logger(__name__)


@dataclass
class OptionPricingData:
    """Option pricing data structure"""
    symbol: str
    strike: float
    option_type: str  # 'call' or 'put'
    expiration_date: str
    current_price: float
    bid: float
    ask: float
    mid_price: float
    volume: int
    open_interest: int
    implied_volatility: float
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float
    timestamp: datetime


class OptionPricer:
    """
    Handles option pricing data retrieval and analysis
    
    Calculates target strikes based on ORB levels and fetches
    real-time option pricing data from Alpaca.
    """
    
    def __init__(self, use_paper_trading: bool = True):
        """
        Initialize Option Pricer
        
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
                "Please check your .env file."
            )
        
        try:
            self.client = StockHistoricalDataClient(
                api_key=api_key,
                secret_key=secret_key
            )
            logger.info(f"Option Pricer initialized successfully (Paper Trading: {self.use_paper_trading})")
        except Exception as e:
            logger.error(f"Failed to initialize Alpaca client: {e}")
            raise
    
    def calculate_target_strikes(self, 
                                current_price: float, 
                                orh: float, 
                                orl: float, 
                                strike_offset_percent: float = 0.1) -> Dict[str, float]:
        """
        Calculate target strike prices for ORB strategy
        
        Args:
            current_price: Current underlying price
            orh: Opening Range High
            orl: Opening Range Low
            strike_offset_percent: Strike offset from OR levels as percentage
            
        Returns:
            Dictionary with target strikes for calls and puts
        """
        # For ORH breakout: Sell put with strike near ORL (with offset)
        put_strike = orl * (1 - strike_offset_percent)
        
        # For ORL breakout: Sell call with strike near ORH (with offset)
        call_strike = orh * (1 + strike_offset_percent)
        
        # Round to nearest $0.50 for SPY options
        put_strike = round(put_strike * 2) / 2
        call_strike = round(call_strike * 2) / 2
        
        return {
            'put_strike': put_strike,
            'call_strike': call_strike,
            'current_price': current_price,
            'orh': orh,
            'orl': orl
        }
    
    def get_next_expiration_date(self, days_to_expiration: int = 1) -> str:
        """
        Get the next expiration date for options
        
        Args:
            days_to_expiration: Number of days until expiration
            
        Returns:
            Expiration date in YYYY-MM-DD format
        """
        # For now, we'll use a simple calculation
        # In production, you'd want to get actual option expiration dates
        expiration_date = datetime.now() + timedelta(days=days_to_expiration)
        
        # Round to next Friday (typical option expiration)
        days_until_friday = (4 - expiration_date.weekday()) % 7
        if days_until_friday == 0 and expiration_date.weekday() != 4:
            days_until_friday = 7
        expiration_date += timedelta(days=days_until_friday)
        
        return expiration_date.strftime('%Y-%m-%d')
    
    def fetch_option_pricing(self, 
                           symbol: str, 
                           strike: float, 
                           option_type: str, 
                           expiration_date: str) -> Optional[OptionPricingData]:
        """
        Fetch option pricing data from Alpaca
        
        Args:
            symbol: Underlying symbol (e.g., 'SPY')
            strike: Strike price
            option_type: 'call' or 'put'
            expiration_date: Expiration date in YYYY-MM-DD format
            
        Returns:
            OptionPricingData object or None if not found
        """
        try:
            validation_error = self._validate_inputs(symbol, strike, option_type, expiration_date)
            if validation_error:
                logger.error(f"Input validation failed: {validation_error}")
                return None
            
            logger.info(f"Fetching option pricing for {symbol} {strike} {option_type} {expiration_date}")
            
            # Create option symbol in Alpaca format: SPY240105C00500000
            # Format: {SYMBOL}{YYMMDD}{C/P}{STRIKE*1000}
            try:
                option_symbol = self._create_option_symbol(symbol, strike, option_type, expiration_date)
                logger.debug(f"Generated option symbol: {option_symbol}")
            except ValueError as e:
                logger.error(f"Failed to create option symbol: {e}")
                return None
            except Exception as e:
                logger.error(f"Unexpected error creating option symbol: {e}")
                return None
            
            try:
                option_bars = self._fetch_option_bars(option_symbol)
            except Exception as e:
                logger.error(f"API error fetching option bars for {option_symbol}: {e}")
                return None
            
            if not option_bars:
                logger.warning(f"No option data found for {option_symbol} - contract may not exist or be inactive")
                return None
            
            try:
                option_data = self._parse_option_data(option_bars, symbol, strike, option_type, expiration_date)
            except Exception as e:
                logger.error(f"Failed to parse option data for {option_symbol}: {e}")
                return None
            
            if not option_data:
                logger.warning(f"Parsed option data is invalid for {option_symbol}")
                return None
            
            logger.info(f"Successfully fetched option pricing for {option_symbol}")
            return option_data
            
        except Exception as e:
            logger.error(f"Unexpected error in fetch_option_pricing: {e}", exc_info=True)
            return None
    
    def _validate_inputs(self, symbol: str, strike: float, option_type: str, expiration_date: str) -> Optional[str]:
        """
        Validate input parameters for option pricing request
        
        Args:
            symbol: Underlying symbol
            strike: Strike price
            option_type: Option type
            expiration_date: Expiration date
            
        Returns:
            Error message if validation fails, None if valid
        """
        if not symbol or not isinstance(symbol, str):
            return "Symbol must be a non-empty string"
        
        if not symbol.isalpha() or len(symbol) > 5:
            return f"Invalid symbol format: {symbol}. Must be 1-5 alphabetic characters"
        
        if not isinstance(strike, (int, float)):
            return f"Strike must be a number, got: {type(strike)}"
        
        if strike <= 0:
            return f"Strike must be positive, got: {strike}"
        
        if strike > 10000:  # Reasonable upper bound
            return f"Strike seems unreasonably high: {strike}"
        
        if not option_type or not isinstance(option_type, str):
            return "Option type must be a non-empty string"
        
        if option_type.lower() not in ['call', 'put']:
            return f"Option type must be 'call' or 'put', got: {option_type}"
        
        if not expiration_date or not isinstance(expiration_date, str):
            return "Expiration date must be a non-empty string"
        
        try:
            exp_date = datetime.strptime(expiration_date, '%Y-%m-%d')
            if exp_date < datetime.now():
                return f"Expiration date cannot be in the past: {expiration_date}"
        except ValueError:
            return f"Invalid expiration date format: {expiration_date}. Expected YYYY-MM-DD"
        
        return None 
    
    def _create_option_symbol(self, symbol: str, strike: float, option_type: str, expiration_date: str) -> str:
        """
        Create Alpaca option symbol format
        
        Args:
            symbol: Underlying symbol (e.g., 'SPY')
            strike: Strike price
            option_type: 'call' or 'put'
            expiration_date: Expiration date in YYYY-MM-DD format
            
        Returns:
            Option symbol in Alpaca format (e.g., 'SPY240105C00500000')
            
        Raises:
            ValueError: If inputs are invalid or option symbol cannot be created
        """
        try:
            # Parse expiration date
            exp_date = datetime.strptime(expiration_date, '%Y-%m-%d')
            
            # Format: YYMMDD
            date_str = exp_date.strftime('%y%m%d')
            
            # Option type: C for call, P for put
            type_char = 'C' if option_type.lower() == 'call' else 'P'
            
            # Strike price * 1000, zero-padded to 8 digits
            # Validate strike can be converted to int
            strike_int = int(strike * 1000)
            if strike_int <= 0:
                raise ValueError(f"Invalid strike price: {strike} (converted to {strike_int})")
            
            strike_str = f"{strike_int:08d}"
            
            option_symbol = f"{symbol}{date_str}{type_char}{strike_str}"
            
            # Validate final symbol length (should be reasonable)
            if len(option_symbol) > 20:
                raise ValueError(f"Generated option symbol too long: {option_symbol}")
            
            return option_symbol
            
        except ValueError as e:
            logger.error(f"ValueError creating option symbol: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating option symbol: {e}")
            raise ValueError(f"Failed to create option symbol: {e}")
    
    def _fetch_option_bars(self, option_symbol: str) -> Optional[Dict]:
        """
        Fetch option bars data from Alpaca
        
        Args:
            option_symbol: Option symbol in Alpaca format
            
        Returns:
            Dictionary with option data or None if not found
        """
        try:
            if not self.client:
                logger.error("Alpaca client not initialized")
                return None
            
            if not option_symbol or not isinstance(option_symbol, str):
                logger.error(f"Invalid option symbol: {option_symbol}")
                return None
            
            logger.debug(f"Requesting option bars for {option_symbol}")
            
            request = OptionBarsRequest(
                symbol_or_symbols=[option_symbol],
                timeframe=TimeFrame.Minute,
                start=datetime.now() - timedelta(days=1),  # Get last day of data
                end=datetime.now()
            )
            
            bars = self.client.get_option_bars(request)
            
            if not bars:
                logger.warning(f"No bars data returned from Alpaca for {option_symbol}")
                return None
            
            if option_symbol not in bars:
                logger.warning(f"Option symbol {option_symbol} not found in API response")
                return None
            
            option_bars = bars[option_symbol]
            if not option_bars:
                logger.warning(f"No option bars data for {option_symbol}")
                return None
            
            latest_bar = option_bars[-1]
            
            if not hasattr(latest_bar, 'close') or latest_bar.close is None:
                logger.warning(f"Invalid bar data for {option_symbol}: missing close price")
                return None
            
            if latest_bar.close <= 0:
                logger.warning(f"Invalid close price for {option_symbol}: {latest_bar.close}")
                return None
            
            logger.debug(f"Successfully fetched bar data for {option_symbol}: close=${latest_bar.close}")
            
            return {
                'open': latest_bar.open,
                'high': latest_bar.high,
                'low': latest_bar.low,
                'close': latest_bar.close,
                'volume': latest_bar.volume,
                'timestamp': latest_bar.timestamp
            }
            
        except Exception as e:
            logger.error(f"Failed to fetch option bars for {option_symbol}: {e}", exc_info=True)
            return None
    
    def _parse_option_data(self, option_bars: Dict, symbol: str, strike: float, 
                          option_type: str, expiration_date: str) -> Optional[OptionPricingData]:
        """
        Parse option bars data into OptionPricingData structure
        
        Args:
            option_bars: Raw option bars data from Alpaca
            symbol: Underlying symbol
            strike: Strike price
            option_type: 'call' or 'put'
            expiration_date: Expiration date
            
        Returns:
            OptionPricingData object or None if parsing fails
        """
        try:
            if not option_bars or not isinstance(option_bars, dict):
                logger.error("Invalid option_bars data: must be a non-empty dictionary")
                return None
            
            required_fields = ['close', 'volume', 'timestamp']
            for field in required_fields:
                if field not in option_bars:
                    logger.error(f"Missing required field in option_bars: {field}")
                    return None
            
            current_price = option_bars['close']
            if not isinstance(current_price, (int, float)) or current_price <= 0:
                logger.error(f"Invalid close price: {current_price}")
                return None
            
            volume = option_bars['volume']
            if not isinstance(volume, (int, float)) or volume < 0:
                logger.warning(f"Invalid volume: {volume}, using 0")
                volume = 0
            
            timestamp = option_bars['timestamp']
            if not timestamp:
                logger.warning("Missing timestamp, using current time")
                timestamp = datetime.now()
            
            # Calculate mid price (we'll use close as approximation)
            mid_price = current_price
            
            # Estimate bid/ask spread (typically 1-2% for liquid options)
            spread_percent = 0.02  # 2% spread
            bid = current_price * (1 - spread_percent / 2)
            ask = current_price * (1 + spread_percent / 2)
            
            # For now, we'll use placeholder values for Greeks
            # In production, you'd calculate these or get them from the API
            delta = 0.3 if option_type.lower() == 'call' else -0.3
            gamma = 0.02
            theta = -0.05
            vega = 0.1
            rho = 0.01
            implied_volatility = 0.25  # Placeholder
            
            logger.debug(f"Parsed option data: {symbol} {strike} {option_type} @ ${current_price}")
            
            return OptionPricingData(
                symbol=symbol,
                strike=strike,
                option_type=option_type,
                expiration_date=expiration_date,
                current_price=current_price,
                bid=bid,
                ask=ask,
                mid_price=mid_price,
                volume=volume,
                # FIXME: find a source for this data point
                open_interest=0,  # Not available in bars data
                implied_volatility=implied_volatility,
                delta=delta,
                gamma=gamma,
                theta=theta,
                vega=vega,
                rho=rho,
                timestamp=timestamp
            )
            
        except Exception as e:
            logger.error(f"Failed to parse option data: {e}", exc_info=True)
            return None
    
    def log_option_pricing_data(self, option_data: OptionPricingData, signal_type: str):
        """
        Log option pricing data in a structured format
        
        Args:
            option_data: OptionPricingData object
            signal_type: Type of signal (e.g., 'ORH_BREAKOUT', 'ORL_BREAKOUT')
        """
        logger.info(f"📊 OPTION PRICING DATA - {signal_type}")
        logger.info(f"   Contract: {option_data.symbol} {option_data.strike} {option_data.option_type.upper()} {option_data.expiration_date}")
        logger.info(f"   Current Price: ${option_data.current_price:.2f}")
        logger.info(f"   Bid/Ask: ${option_data.bid:.2f} / ${option_data.ask:.2f}")
        logger.info(f"   Mid Price: ${option_data.mid_price:.2f}")
        logger.info(f"   Volume: {option_data.volume:,}")
        logger.info(f"   Open Interest: {option_data.open_interest:,}")
        logger.info(f"   Implied Volatility: {option_data.implied_volatility:.1%}")
        logger.info(f"   Delta: {option_data.delta:.3f}")
        logger.info(f"   Gamma: {option_data.gamma:.3f}")
        logger.info(f"   Theta: {option_data.theta:.3f}")
        logger.info(f"   Vega: {option_data.vega:.3f}")
        logger.info(f"   Rho: {option_data.rho:.3f}")
        logger.info(f"   Timestamp: {option_data.timestamp}")
        logger.info("   " + "="*50)