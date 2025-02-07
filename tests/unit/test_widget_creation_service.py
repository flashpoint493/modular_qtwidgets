import os
import pytest
from PySide6.QtWidgets import QWidget, QApplication
from modular_qtwidgets.widget_loader import WidgetCreationService
from modular_qtwidgets.widget_strategies import WidgetCreationStrategy

# 创建 QApplication 实例
@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    app.quit()

@pytest.fixture
def config_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "fixtures", "test_config.yaml")

@pytest.fixture
def widget_service(config_path):
    return WidgetCreationService(config_path)

def test_service_initialization(widget_service):
    """测试服务初始化"""
    assert widget_service is not None
    assert hasattr(widget_service, "widget_config")
    assert "widget_system" in widget_service.widget_config

def test_strategy_registration(widget_service):
    """测试策略注册"""
    class TestStrategy(WidgetCreationStrategy):
        def can_handle(self, widget_class):
            return True
        def create_widget(self, widget_class, params=None):
            return QWidget()
    
    widget_service.register_strategy("test_strategy", TestStrategy())
    assert "test_strategy" in widget_service._strategies

def test_widget_creation(widget_service, qapp):
    """测试组件创建"""
    widgets = widget_service.create_widgets_for_location("test_group")
    assert len(widgets) > 0
    assert isinstance(widgets[0], QWidget)

def test_widget_creation_callback(widget_service, qapp):
    """测试组件创建回调"""
    callback_called = False
    
    def on_widget_created(widget, name, config):
        nonlocal callback_called
        callback_called = True
        assert isinstance(widget, QWidget)
        assert isinstance(name, str)
        assert isinstance(config, dict)
    
    widget_service.create_widgets_for_location("test_group", on_widget_created)
    assert callback_called

def test_invalid_location(widget_service):
    """测试无效的位置"""
    widgets = widget_service.create_widgets_for_location("non_existent_group")
    assert len(widgets) == 0

def test_disabled_widget(widget_service, config_path):
    """测试禁用的组件"""
    import yaml
    import tempfile
    
    # 创建临时配置文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        
        config["widget_system"]["groups"]["test_group"]["widgets"]["test_widget"]["enabled"] = False
        yaml.dump(config, temp_file)
        temp_config_path = temp_file.name
    
    try:
        # 创建新的服务实例
        service = WidgetCreationService(temp_config_path)
        widgets = service.create_widgets_for_location("test_group")
        assert len(widgets) == 0
    finally:
        os.unlink(temp_config_path)
