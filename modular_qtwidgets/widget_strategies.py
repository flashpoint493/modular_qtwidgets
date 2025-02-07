"""Widget creation strategies."""

from typing import Type, Dict, Any
from PySide6 import QtWidgets

class WidgetCreationStrategy:
    """Base class for widget creation strategies."""
    
    def can_handle(self, widget_class: Type) -> bool:
        """Check if this strategy can handle the widget class.
        
        Args:
            widget_class (Type): Widget class to check
            
        Returns:
            bool: True if this strategy can handle the widget class
        """
        raise NotImplementedError()
    
    def create_widget(self, widget_class: Type, params: Dict[str, Any] = None) -> QtWidgets.QWidget:
        """Create a widget instance.
        
        Args:
            widget_class (Type): Widget class to create
            params (Dict[str, Any], optional): Parameters to pass to widget constructor
            
        Returns:
            QtWidgets.QWidget: Created widget instance
        """
        raise NotImplementedError()

class DefaultWidgetStrategy(WidgetCreationStrategy):
    """Strategy for creating QWidget instances."""
    
    def can_handle(self, widget_class: Type) -> bool:
        """Check if this strategy can handle the widget class.
        
        Args:
            widget_class (Type): Widget class to check
            
        Returns:
            bool: True if this strategy can handle the widget class
        """
        return issubclass(widget_class, QtWidgets.QWidget)
    
    def create_widget(self, widget_class: Type, params: Dict[str, Any] = None) -> QtWidgets.QWidget:
        """Create a QWidget instance.
        
        Args:
            widget_class (Type): Widget class to create
            params (Dict[str, Any], optional): Parameters to pass to widget constructor
            
        Returns:
            QtWidgets.QWidget: Created widget instance
        """
        if params:
            return widget_class(**params)
        return widget_class()
