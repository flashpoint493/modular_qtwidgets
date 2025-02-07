"""Widget loader module."""

import os
import sys
import logging
import importlib.util
from typing import Any, Dict, Optional, List, Tuple, Callable, Type

import yaml
from PySide6 import QtWidgets


class WidgetCreationService:
    """Service for creating widgets using different strategies."""
    
    def __init__(self, config_path: str):
        """Initialize the service with empty strategies dictionary."""
        self.widget_config = load_config(config_path)
        self._strategies = {}
        self._register_default_strategies()
        
    def _register_default_strategies(self):
        """Register default widget creation strategies."""
        for strategy_config in self.widget_config['widget_system']['strategies']:
            if not strategy_config.get('enabled', True):
                continue
                
            strategy_path = strategy_config.get('path')
            class_name = strategy_config.get('class')
            
            if not strategy_path or not class_name:
                continue
                
            strategy_class = self.load_strategy_class(strategy_path, class_name)
            if strategy_class:
                self.register_strategy(strategy_config['name'], strategy_class())
    
    def register_strategy(self, name: str, strategy):
        """Register a new widget creation strategy."""
        self._strategies[name] = strategy
        
    def load_strategy_class(self, strategy_path: str, class_name: str) -> Optional[type]:
        """Load a strategy class from a module."""
        try:
            if not os.path.exists(strategy_path):
                raise FileNotFoundError(f"Could not find strategy module {strategy_path}")
                
            spec = importlib.util.spec_from_file_location("dynamic_strategy", strategy_path)
            if not spec or not spec.loader:
                raise ImportError(f"Failed to load spec for {strategy_path}")
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            strategy_class = getattr(module, class_name)
            required_methods = ['can_handle', 'create_widget']
            missing_methods = [method for method in required_methods if not hasattr(strategy_class, method)]
            if missing_methods:
                raise TypeError(f"Strategy class {class_name} must implement methods: {', '.join(missing_methods)}")
            return strategy_class
            
        except Exception as e:
            print(f"Failed to load strategy class: {e}")
            return None
    
    def create_widget(self, module_path: str, class_name: str, params: Dict[str, Any] = None,
                     strategy_name: str = None) -> Optional[QtWidgets.QWidget]:
        """Create a widget using registered strategies."""
        if not params:
            params = {}
            
        try:
            if not os.path.exists(module_path):
                raise FileNotFoundError(f"Could not find module {module_path}")
            
            spec = importlib.util.spec_from_file_location("dynamic_widget", module_path)
            if not spec or not spec.loader:
                raise ImportError(f"Failed to load spec for {module_path}")
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            widget_class = getattr(module, class_name)
            
            # Get strategy
            strategy = None
            if strategy_name and strategy_name in self._strategies:
                strategy = self._strategies[strategy_name]
            else:
                # Find first strategy that can handle this widget class
                for s in self._strategies.values():
                    if s.can_handle(widget_class):
                        strategy = s
                        break
                        
            if strategy:
                return strategy.create_widget(widget_class, params)
                
            raise ValueError(f"No suitable strategy found for widget class {widget_class.__name__}")
            
        except Exception as e:
            logging.error(f"Failed to create widget: {e}")
            return None
    
    def get_widgets_for_location(self, location: str) -> List[Tuple[int, str, Dict]]:
        """Get all widget configurations for a specific location."""
        if not self.widget_config:
            return []
            
        widget_system = self.widget_config.get('widget_system', {})
        if not widget_system:
            return []
            
        system_config = widget_system.get('config', {})
        default_group_enabled = system_config.get('default_group_enabled', True)
        default_widget_enabled = system_config.get('default_widget_enabled', True)
        
        groups = widget_system.get('groups', {})
        group_config = groups.get(location)
        if not group_config:
            return []
            
        if not group_config.get('enabled', default_group_enabled):
            return []
            
        widgets = []
        widget_configs = group_config.get('widgets', {})
        for widget_name, widget_config in widget_configs.items():
            if not widget_config.get('enabled', default_widget_enabled):
                continue
                    
            priority = widget_config.get('priority', 100)
            widgets.append((priority, widget_name, widget_config))
            
        return sorted(widgets, key=lambda x: x[0])
        
    def create_widgets_for_location(self, location: str, 
                                  on_widget_created: Optional[Callable[[QtWidgets.QWidget, str, Dict], None]] = None) -> List[QtWidgets.QWidget]:
        """Create all widgets for a specific location with a callback for customization.
        
        Args:
            location (str): Location name to get widgets for
            on_widget_created (Optional[Callable[[QtWidgets.QWidget, str, Dict], None]]): Optional callback that will be called 
                after each widget is created. The callback receives:
                - widget: The created widget instance
                - widget_name: Name of the widget from config
                - widget_config: Configuration dictionary for the widget
                
        Returns:
            List[QtWidgets.QWidget]: List of created widget instances
        """
        widgets = []
        widget_configs = self.get_widgets_for_location(location)
        
        for priority, widget_name, widget_config in widget_configs:
            try:
                widget_path = widget_config.get('path', '')
                widget_class = widget_config.get('class', '')
                
                if not widget_path or not widget_class:
                    continue
                
                params = widget_config.get('params', {})
                strategy = widget_config.get('strategy')
                
                widget = self.create_widget(widget_path, widget_class, params, strategy)
                if widget:
                    if on_widget_created:
                        on_widget_created(widget, widget_name, widget_config)
                    widgets.append(widget)
                    logging.info(f"Successfully created widget: {widget_class}")
                else:
                    logging.error(f"Failed to create widget: {widget_class}")
                    
            except Exception as e:
                logging.error(f"Error creating widget {widget_name}: {e}")
                
        return widgets


def load_config(config_path) -> Dict:
    """Load widget configuration from YAML file."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Failed to load widget config: {e}")
        return {}
