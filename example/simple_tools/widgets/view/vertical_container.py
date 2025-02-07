"""Vertical container widget for organizing multiple widgets."""

import os
import logging
from typing import List
from PySide6 import QtWidgets
from modular_qtwidgets.widget_loader import WidgetCreationService

class VerticalContainerWidget(QtWidgets.QWidget):
    """Main container widget that loads and organizes child widgets vertically."""
    
    _location = "scripts_components"

    def __init__(self, parent=None):
        """Initialize the container widget.

        Args:
            parent (QtWidgets.QWidget, optional): Parent widget.
        """
        super().__init__(parent)
        self.item_widgets: List[QtWidgets.QWidget] = []
        self.setup_ui()
        self.load_widgets()
        
    def setup_ui(self) -> None:
        """Set up the widget's UI."""
        # Create main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Create scroll area
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        # Create container widget for scroll area
        self.container = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.container)
        self.container_layout = QtWidgets.QVBoxLayout(self.container)
        
        # Add stretch at the bottom
        self.container_layout.addStretch()

    def load_widgets(self) -> None:
        """Load widgets from configuration file."""
        try:
            # Get the config file path
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            config_path = os.path.join(current_dir, "configs", "simple_tools.yaml")
            
            # Create widget service
            service = WidgetCreationService(config_path)
            
            # Define callback for widget creation
            def on_widget_created(widget: QtWidgets.QWidget, widget_name: str, widget_config: dict):
                self.container_layout.insertWidget(self.container_layout.count() - 1, widget)
                self.item_widgets.append(widget)
            
            # Create widgets with callback
            widgets = service.create_widgets_for_location(self._location, on_widget_created)
            
            if not widgets:
                logging.warning("No widgets loaded from configuration")
                error_label = QtWidgets.QLabel("No widgets loaded from configuration")
                self.container_layout.insertWidget(self.container_layout.count() - 1, error_label)
                
        except Exception as e:
            logging.error(f"Error loading widgets: {e}")
            error_label = QtWidgets.QLabel(f"Error loading widgets: {str(e)}")
            self.container_layout.insertWidget(self.container_layout.count() - 1, error_label)
