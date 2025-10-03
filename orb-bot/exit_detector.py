"""
Exit Detection Module

This module contains the ExitDetector class for detecting exit signals
in the ORB trading strategy.
"""

import pytz
from datetime import datetime
from typing import Optional
from data_structures import OpeningRange, OpportunityWindow, ExitSignal


class ExitDetector:
    """Handles exit signal detection for ORB strategy positions"""
    
    def __init__(self, timezone: pytz.timezone):
        self.timezone = timezone
    
    def detect_midline_cross_exit(self, current_price: float, opening_range_data: OpeningRange,
                                 opportunity_window: OpportunityWindow, has_short_call: bool = False,
                                 has_short_put: bool = False) -> Optional[ExitSignal]:
        """
        Detect midline cross exit signals
        
        - Check for midline cross exit (applies to both short calls and short puts)
        - For short calls: price re-entered opening range and crossed above midline
        - For short puts: price re-entered opening range and crossed below midline

        Args:
            current_price: Current market price
            opening_range_data: Opening range data (ORH, ORL)
            opportunity_window: Opportunity window data
            has_short_call: Whether we have an open short call position
            has_short_put: Whether we have an open short put position
            
        Returns:
            ExitSignal if exit conditions are met, None otherwise
        """
        if not (has_short_call or has_short_put):
            return None
        
        orh = opening_range_data.high
        orl = opening_range_data.low
        midline = opportunity_window.midline
        
        if not self._should_exit_short_call(current_price, orl, midline, has_short_call) and \
           not self._should_exit_short_put(current_price, orh, midline, has_short_put):
            return None
        
        direction = "above" if current_price > midline else "below"
        
        return ExitSignal(
            type='MIDLINE_CROSS',  # SignalType.MIDLINE_CROSS.value
            current_price=current_price,
            orh=orh,
            orl=orl,
            opportunity_window_midline=midline,
            timestamp=datetime.now(self.timezone),
            reason=f"Price re-entered opening range and crossed {direction} opportunity window midline. Current: ${current_price:.2f}, Midline: ${midline:.2f}"
        )
    
    def _should_exit_short_call(self, current_price: float, orl: float, midline: float, has_short_call: bool) -> bool:
        """
        Check if short call position should be exited
        
        Args:
            current_price: Current market price
            orl: Opening range low
            midline: Opportunity window midline
            has_short_call: Whether we have a short call position
            
        Returns:
            True if short call should be exited
        """
        return has_short_call and current_price > orl and current_price > midline
    
    def _should_exit_short_put(self, current_price: float, orh: float, midline: float, has_short_put: bool) -> bool:
        """
        Check if short put position should be exited
        
        Args:
            current_price: Current market price
            orh: Opening range high
            midline: Opportunity window midline
            has_short_put: Whether we have a short put position
            
        Returns:
            True if short put should be exited
        """
        return has_short_put and current_price < orh and current_price < midline
