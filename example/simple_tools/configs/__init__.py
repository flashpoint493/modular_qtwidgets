"""Modular Qt Widgets package."""

from .widget_loader import WidgetCreationService
from .widget_strategies import WidgetCreationStrategy

__version__ = "0.1.0"
__all__ = [
    'WidgetCreationService',
    'WidgetCreationStrategy',
]