import pytest
from PySide6.QtWidgets import QWidget, QPushButton
from modular_qtwidgets.widget_strategies import DefaultWidgetStrategy

@pytest.fixture
def strategy():
    return DefaultWidgetStrategy()

def test_can_handle_qwidget(strategy):
    """测试是否可以处理 QWidget"""
    assert strategy.can_handle(QWidget)

def test_can_handle_qwidget_subclass(strategy):
    """测试是否可以处理 QWidget 的子类"""
    assert strategy.can_handle(QPushButton)

def test_cannot_handle_non_qwidget(strategy):
    """测试是否拒绝非 QWidget 类"""
    class NonWidget:
        pass
    assert not strategy.can_handle(NonWidget)

def test_create_widget_without_params(strategy):
    """测试不带参数创建组件"""
    widget = strategy.create_widget(QWidget)
    assert isinstance(widget, QWidget)

def test_create_widget_with_params(strategy):
    """测试带参数创建组件"""
    class TestWidget(QWidget):
        def __init__(self, test_param=None):
            super().__init__()
            self.test_param = test_param
    
    widget = strategy.create_widget(TestWidget, {"test_param": "test"})
    assert isinstance(widget, TestWidget)
    assert widget.test_param == "test"

def test_create_widget_invalid_params(strategy):
    """测试无效参数"""
    class TestWidget(QWidget):
        def __init__(self, test_param=None):
            super().__init__()
            self.test_param = test_param
    
    with pytest.raises(TypeError):
        strategy.create_widget(TestWidget, {"invalid_param": "value"})
