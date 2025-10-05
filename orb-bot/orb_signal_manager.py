"""
ORB Signal Manager

This module provides ORB-specific signal detection and management.
It implements the signal detection logic for the Opening Range Breakout strategy.
"""
from typing import List, Dict, Any
import pandas as pd
from signal_manager import SignalManager, Signal, SignalType, SignalDirection
from signal_context import SignalContext
from data_structures import OpeningRange, OpportunityWindow, BreakoutType, ExitSignalType
from logger_config import initialize_trading_logger

logger, trading_logger, log_file_path, env_info = initialize_trading_logger(level="INFO", log_to_file=True)


class ORBContext(SignalContext):
    """
    Context for ORB signal detection
    
    Contains the opening range data and opportunity window needed
    for ORB signal detection.
    """
    
    def __init__(self, opening_range_data: OpeningRange, opportunity_window: OpportunityWindow):
        """
        Initialize ORB context
        
        Args:
            opening_range_data: Opening range high/low data
            opportunity_window: Opportunity window timing data
        """
        self.opening_range_data = opening_range_data
        self.opportunity_window = opportunity_window


class ORBSignalManager(SignalManager):
    """
    Signal manager for Opening Range Breakout strategy
    
    Detects entry signals (ORH/ORL breakouts) and exit signals
    (midline crosses, opportunity window end).
    """
    
    def detect_entry_signals(self, market_data: pd.DataFrame, context: ORBContext) -> List[Signal]:
        """
        Detect ORB entry signals (breakouts above ORH or below ORL)
        
        Args:
            market_data: Market data (OHLCV bars)
            context: ORB context with opening range and opportunity window data
            
        Returns:
            List of entry signals
        """
        signals = []
        current_price = self.strategy.market_analyzer.get_current_price(market_data)
        
        if not current_price:
            logger.error("Could not get current price for entry signal detection")
            return signals
        
        logger.info("Looking for ORB entry signals...")
        
        breakout = self.strategy.market_analyzer.detect_breakout(
            current_price,
            context.opening_range_data,
            context.opportunity_window
        )
        
        if not breakout:
            trading_logger.log_no_breakout(
                symbol=self.strategy.symbol,
                current_price=current_price,
                orh=context.opening_range_data.high,
                orl=context.opening_range_data.low,
                opportunity_window_active=context.opportunity_window.is_active
            )
            return signals
        
        if breakout.type == BreakoutType.ORH_BREAKOUT:
            signal = Signal(
                signal_type=SignalType.ENTRY,
                direction=SignalDirection.SHORT,  # Short put on ORH breakout
                strength=min(breakout.breakout_strength, 1.0),
                metadata={
                    'breakout_type': breakout.type.value,
                    'breakout_level': breakout.breakout_level,
                    'current_price': current_price,
                    'orh': context.opening_range_data.high,
                    'orl': context.opening_range_data.low,
                    'distance_from_midline': breakout.distance_from_midline,
                    'strategy_action': 'sell_put'
                }
            )
            signals.append(signal)
            
        elif breakout.type == BreakoutType.ORL_BREAKOUT:
            signal = Signal(
                signal_type=SignalType.ENTRY,
                direction=SignalDirection.SHORT,  # Short call on ORL breakout
                strength=min(breakout.breakout_strength, 1.0),
                metadata={
                    'breakout_type': breakout.type.value,
                    'breakout_level': breakout.breakout_level,
                    'current_price': current_price,
                    'orh': context.opening_range_data.high,
                    'orl': context.opening_range_data.low,
                    'distance_from_midline': breakout.distance_from_midline,
                    'strategy_action': 'sell_call'
                }
            )
            signals.append(signal)
        
        if signals:
            trading_logger.log_breakout_detected(
                symbol=self.strategy.symbol,
                breakout_type=breakout.type,
                direction=breakout.direction,
                breakout_level=breakout.breakout_level,
                strength=breakout.breakout_strength,
                distance_from_midline=breakout.distance_from_midline
            )
        
        return signals
        
    def detect_exit_signals(self, market_data: pd.DataFrame, context: ORBContext) -> List[Signal]:
        """
        Detect ORB exit signals (midline crosses, opportunity window end)
        
        Args:
            market_data: Market data (OHLCV bars)
            context: ORB context with opening range and opportunity window data
            
        Returns:
            List of exit signals
        """
        signals = []
        current_price = self.strategy.market_analyzer.get_current_price(market_data)
        
        if not current_price:
            logger.error("Could not get current price for exit signal detection")
            return signals
        
        logger.info("Looking for ORB exit signals...")
        
        exit_signal = self.strategy.market_analyzer.detect_exit_signal(
            current_price=current_price,
            opening_range_data=context.opening_range_data,
            opportunity_window=context.opportunity_window,
            has_short_call=self.strategy.position_manager.has_short_call,
            has_short_put=self.strategy.position_manager.has_short_put
        )
        
        if not exit_signal:
            return signals
        
        signal = Signal(
            signal_type=SignalType.EXIT,
            direction=SignalDirection.NEUTRAL,
            strength=1.0,
            metadata={
                'exit_type': exit_signal.type.value,
                'current_price': exit_signal.current_price,
                'orh': exit_signal.orh,
                'orl': exit_signal.orl,
                'midline': exit_signal.opportunity_window_midline,
                'reason': exit_signal.reason,
                'strategy_action': 'close_all_positions'
            }
        )

        signals.append(signal)
        
        trading_logger.log_exit_signal_detected(
            symbol=self.strategy.symbol,
            exit_type=exit_signal.type,
            current_price=exit_signal.current_price,
            orh=exit_signal.orh,
            orl=exit_signal.orl,
            midline=exit_signal.opportunity_window_midline,
            reason=exit_signal.reason
        )
        
        return signals
