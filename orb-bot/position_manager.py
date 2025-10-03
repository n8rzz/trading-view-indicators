"""
Position Management Module

This module contains the PositionManager class for handling open positions
in the ORB trading strategy.
"""

from typing import List, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from logger_config import initialize_trading_logger

if TYPE_CHECKING:
    from market_analyzer import ExitSignal

logger, trading_logger, log_file_path, env_info = initialize_trading_logger(level="INFO", log_to_file=True)


class OptionType(Enum):
    CALL = "CALL"
    PUT = "PUT"


class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"


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


class PositionManager:
    """Manages open positions for the ORB strategy"""
    
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.open_positions: List[OptionOrder] = []
        self.has_short_call: bool = False
        self.has_short_put: bool = False
    
    def add_position(self, option_order: OptionOrder) -> None:
        """
        Add a new position to the open positions list
        
        Args:
            option_order: The option order representing the position
        """
        self.open_positions.append(option_order)
        
        # Update position flags
        if option_order.option_type == OptionType.CALL and option_order.side == OrderSide.SELL:
            self.has_short_call = True
        elif option_order.option_type == OptionType.PUT and option_order.side == OrderSide.SELL:
            self.has_short_put = True
    
    def close_position(self, position: OptionOrder, exit_signal: 'ExitSignal') -> None:
        """
        Close a position based on exit signal
        
        Args:
            position: The position to close
            exit_signal: The exit signal that triggered the closure
        """
        if position in self.open_positions:
            self.open_positions.remove(position)
        
        if position.option_type == OptionType.CALL and position.side == OrderSide.SELL:
            self.has_short_call = False
        elif position.option_type == OptionType.PUT and position.side == OrderSide.SELL:
            self.has_short_put = False
        
        trading_logger.log_position_closed(
            symbol=self.symbol,
            position_type=f"{position.option_type.value}_{position.side.value}",
            exit_reason=exit_signal.reason,
            exit_price=exit_signal.current_price,
            strike=position.strike,
            quantity=position.quantity
        )
    
    def close_all_positions(self, exit_signal: 'ExitSignal') -> None:
        """
        Close all open positions based on exit signal
        
        Args:
            exit_signal: The exit signal that triggered the closure
        """
        positions_to_close = self.open_positions.copy()
        for position in positions_to_close:
            self.close_position(position, exit_signal)
        
        logger.info(f"Closed {len(positions_to_close)} position(s) due to exit signal: {exit_signal.reason}")
    
    def has_positions(self) -> bool:
        """
        Check if there are any open positions
        
        Returns:
            True if there are open positions, False otherwise
        """
        return len(self.open_positions) > 0
