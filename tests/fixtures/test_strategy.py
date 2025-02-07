from typing import Type, Dict, Any
from PySide6.QtWidgets import QWidget
from modular_qtwidgets.widget_strategies import WidgetCreationStrategy

class TestWidgetStrategy(WidgetCreationStrategy):
    """Test strategy for widget creation."""
    
    def can_handle(self, widget_class: Type) -> bool:
        """Test if this strategy can handle the widget class."""
        return issubclass(widget_class, QWidget)
    
    def create_widget(self, widget_class: Type, params: Dict[str, Any] = None) -> QWidget:
        """Create a test widget instance."""
        if params is None:
            params = {}
        return widget_class(**params)
