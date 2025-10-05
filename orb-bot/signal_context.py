"""
Signal Context Module

This module contains the abstract base class for signal detection context.
"""

from abc import ABC


class SignalContext(ABC):
    """
    Base class for signal detection context

    Each strategy should implement its own context class that contains
    the strategy-specific data needed for signal detection.
    """

    def __init__(self):
        if self.__class__ is SignalContext:
            raise TypeError("Cannot instantiate abstract class SignalContext")
