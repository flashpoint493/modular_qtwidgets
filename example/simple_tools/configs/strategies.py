"""Widget creation strategies."""

from typing import Any, Dict, Type
from PySide6 import QtWidgets


class QtWidgetStrategy:
    """Strategy for creating QWidget instances."""
    
    def can_handle(self, widget_class: Type) -> bool:
        """Check if this strategy can handle the widget class.
        
        Args:
            widget_class (Type): Widget class to check
            
        Returns:
            bool: True if this strategy can handle the widget class
        """
        try:
            return issubclass(widget_class, QtWidgets.QWidget)
        except TypeError:
            return False
    
    def create_widget(self, widget_class: Type, params: Dict[str, Any] = None) -> QtWidgets.QWidget:
        """Create a QWidget instance.
        
        Args:
            widget_class (Type): Widget class to create
            params (Dict[str, Any], optional): Parameters to pass to widget constructor
            
        Returns:
            QtWidgets.QWidget: Created widget instance
        """
        if not params:
            params = {}
            
        try:
            return widget_class(**params)
        except Exception as e:
            print(f"Error creating widget: {e}")
            return None
