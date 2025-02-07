import os
import pytest
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from modular_qtwidgets import WidgetCreationService

@pytest.fixture(scope="session")
def qapp():
    app = QApplication([])
    yield app
    app.quit()

@pytest.fixture
def config_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "fixtures", "test_config.yaml")

class TestMainWidget(QWidget):
    def __init__(self, config_path, parent=None):
        super().__init__(parent)
        self.widgets = []
        self.setup_ui()
        self.load_widgets(config_path)
    
    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.addStretch()
    
    def load_widgets(self, config_path):
        service = WidgetCreationService(config_path)
        
        def on_widget_created(widget, name, config):
            self.layout.insertWidget(self.layout.count() - 1, widget)
            self.widgets.append(widget)
        
        service.create_widgets_for_location("test_group", on_widget_created)

def test_main_widget_integration(qapp, config_path):
    """测试主窗口集成"""
    # 创建主窗口
    main_widget = TestMainWidget(config_path)
    
    # 验证组件是否正确加载
    assert len(main_widget.widgets) > 0
    
    # 验证布局
    assert isinstance(main_widget.layout, QVBoxLayout)
    assert main_widget.layout.count() > 1  # 至少有一个组件和一个弹性空间
    
    # 验证组件参数
    test_widget = main_widget.widgets[0]
    assert hasattr(test_widget, "test_param")
    assert test_widget.test_param == "test_value"

def test_widget_creation_order(qapp, config_path):
    """测试组件创建顺序"""
    import yaml
    import tempfile
    import shutil
    
    # 创建临时配置文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        widgets = config["widget_system"]["groups"]["test_group"]["widgets"]
        widgets["test_widget2"] = {
            "enabled": True,
            "path": "tests/fixtures/test_widget.py",
            "class": "TestWidget",
            "priority": 1,
            "description": "Test widget 2",
            "strategy": "TestWidgetStrategy",
            "params": {"test_param": "test_value_2"}
        }
        
        yaml.dump(config, temp_file)
        temp_config_path = temp_file.name
    
    try:
        # 创建主窗口
        main_widget = TestMainWidget(temp_config_path)
        
        # 验证组件顺序（按优先级排序）
        assert len(main_widget.widgets) == 2
        assert main_widget.widgets[0].test_param == "test_value"
        assert main_widget.widgets[1].test_param == "test_value_2"
    finally:
        os.unlink(temp_config_path)
