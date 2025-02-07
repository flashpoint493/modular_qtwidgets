# Modular QtWidgets

一个基于配置驱动的模块化Qt组件创建框架。通过简单的配置文件，即可创建复杂的Qt界面，无需编写大量重复的UI代码。

## 安装

```bash
pip install modular-qtwidgets
```

## 核心概念# Modular QtWidgets

一个基于配置驱动的模块化Qt组件创建框架。通过简单的配置文件，即可创建复杂的Qt界面，无需编写大量重复的UI代码。

## 安装

```bash
pip install modular-qtwidgets
```

## 核心概念

### 1. 配置文件结构

配置文件使用YAML格式，主要包含以下部分：

```yaml
widget_system:
  # 全局配置
  config:
    default_group_enabled: true    # 默认组是否启用
    default_widget_enabled: true   # 默认组件是否启用

  # 组件创建策略配置
  strategies:
    - name: "QWidgetStrategy"      # 策略名称
      description: "策略描述"      # 策略描述
      enabled: true               # 是否启用
      path: "path/to/strategy.py" # 策略类文件路径
      class: StrategyClassName    # 策略类名

  # 组件组配置
  groups:
    group_name:                   # 组名称
      enabled: true              # 是否启用
      description: "组描述"      # 组描述
      widgets:                   # 组内组件列表
        widget_name:             # 组件名称
          enabled: true          # 是否启用
          path: "path/to/widget.py" # 组件类文件路径
          class: WidgetClassName # 组件类名
          priority: 0            # 显示优先级（数字越小优先级越高）
          description: "组件描述" # 组件描述
          strategy: "策略名称"    # 使用的创建策略
          params:                # 组件初始化参数
            param1: value1
            param2: value2
```

### 2. 组件加载器

使用 `WidgetCreationService` 来加载和创建组件：

```python
from modular_qtwidgets import WidgetCreationService

# 初始化服务
service = WidgetCreationService("config.yaml")

# 为特定位置创建组件
def on_widget_created(widget, widget_name, widget_config):
    """组件创建回调函数
    Args:
        widget: 创建的组件实例
        widget_name: 配置中的组件名称
        widget_config: 组件的配置信息
    """
    # 处理新创建的组件
    pass

# 创建指定位置的所有组件
widgets = service.create_widgets_for_location("group_name", on_widget_created)
```

### 3. 组件创建策略

创建自定义组件策略：

```python
from modular_qtwidgets import WidgetCreationStrategy
from PySide6.QtWidgets import QWidget

class CustomWidgetStrategy(WidgetCreationStrategy):
    def can_handle(self, widget_class: Type) -> bool:
        """检查是否可以处理该组件类"""
        return issubclass(widget_class, QWidget)

    def create_widget(self, widget_class: Type, params: Dict[str, Any] = None) -> QWidget:
        """创建组件实例"""
        if params is None:
            params = {}
        return widget_class(**params)

# 注册策略
service.register_strategy("CustomStrategy", CustomWidgetStrategy())
```

## 使用场景

### 1. 在主窗口中挂载配置的组件

如果你有一个主窗口，想要在其中的垂直布局中加载配置的组件，可以这样做：

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from modular_qtwidgets import WidgetCreationService

class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_widgets()
    
    def setup_ui(self):
        # 创建主布局
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # 创建滚动区域（可选，用于内容超出窗口时）
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        # 创建容器组件
        self.container = QWidget()
        self.scroll_area.setWidget(self.container)
        self.container_layout = QVBoxLayout(self.container)
        
        # 在底部添加弹性空间（可选，使组件靠上对齐）
        self.container_layout.addStretch()
    
    def load_widgets(self):
        try:
            # 创建组件服务
            service = WidgetCreationService("config.yaml")
            
            # 定义组件创建回调
            def on_widget_created(widget, widget_name, widget_config):
                # 将新组件插入到弹性空间之前
                self.container_layout.insertWidget(
                    self.container_layout.count() - 1,  # 插入到最后一个项目（弹性空间）之前
                    widget
                )
            
            # 创建指定位置的所有组件
            widgets = service.create_widgets_for_location(
                "your_group_name",  # 配置文件中定义的组名
                on_widget_created
            )
            
            if not widgets:
                # 处理没有组件的情况
                pass
                
        except Exception as e:
            # 处理错误情况
            pass
```

这个实现提供了以下功能：

1. **滚动支持**：当组件总高度超过窗口高度时，可以滚动查看
2. **自动布局**：组件会自动垂直排列
3. **靠上对齐**：通过底部的弹性空间，组件会靠上对齐
4. **动态加载**：组件是根据配置动态创建的

配置文件示例：

```yaml
widget_system:
  config:
    default_group_enabled: true
    default_widget_enabled: true
  
  strategies:
    - name: "QWidgetStrategy"
      enabled: true
      path: "path/to/strategies.py"
      class: QtWidgetStrategy
  
  groups:
    your_group_name:
      enabled: true
      description: "Your group description"
      widgets:
        widget1:
          enabled: true
          path: "path/to/widget1.py"
          class: Widget1Class
          priority: 0
          strategy: "QWidgetStrategy"
          params:
            param1: value1
        widget2:
          enabled: true
          path: "path/to/widget2.py"
          class: Widget2Class
          priority: 1
          strategy: "QWidgetStrategy"
          params:
            param2: value2
```

注意事项：
1. 组件会按照 `priority` 值从小到大的顺序创建和添加
2. 每个组件的具体参数在 `params` 中定义
3. 确保配置文件中的路径是正确的
4. 可以通过 `enabled` 字段控制组件是否加载

## 本地开发和安装

如果你是从 GitHub 克隆此仓库进行开发，请按照以下步骤操作：

1. 克隆仓库：
   ```bash
   git clone <repository_url>
   cd modular_qtwidgets
   ```

2. 创建并激活虚拟环境（推荐）：
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Linux/macOS
   python -m venv .venv
   source .venv/bin/activate
   ```

3. 安装开发依赖：
   ```bash
   # 安装基本依赖
   pip install -e .

   # 安装测试依赖
   pip install -e ".[test]"
   ```

## 运行测试

本项目使用 pytest 进行测试。测试套件包括单元测试和集成测试，涵盖了以下方面：

1. **组件创建服务测试**：
   - 服务初始化
   - 策略注册
   - 组件创建
   - 回调函数
   - 错误处理

2. **组件策略测试**：
   - QWidget 类型检查
   - 参数处理
   - 错误处理

3. **集成测试**：
   - 主窗口集成
   - 组件创建顺序

运行测试：
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/unit/test_widget_creation_service.py

# 运行带覆盖率报告的测试
pytest --cov=modular_qtwidgets

# 运行特定测试用例
pytest tests/unit/test_widget_creation_service.py::test_service_initialization
```

### 编写新测试

如果你要为项目添加新的测试，请遵循以下规则：

1. **测试文件组织**：
   - 单元测试放在 `tests/unit/` 目录下
   - 集成测试放在 `tests/integration/` 目录下
   - 测试固件放在 `tests/fixtures/` 目录下

2. **命名约定**：
   - 测试文件名以 `test_` 开头
   - 测试函数名以 `test_` 开头
   - 测试类名以 `Test` 开头

3. **固件使用**：
   - 使用 `conftest.py` 定义共享固件
   - 使用 `@pytest.fixture` 装饰器定义测试固件
   - Qt 应用程序使用全局 `qapp` 固件

示例：
```python
import pytest
from PySide6.QtWidgets import QWidget
from modular_qtwidgets import WidgetCreationService

def test_widget_creation(widget_service, qapp):
    """测试组件创建"""
    widgets = widget_service.create_widgets_for_location("test_group")
    assert len(widgets) > 0
    assert isinstance(widgets[0], QWidget)
```

## 运行测试样例

```bash
#启动示例窗口
python example/simple_tools/main.py
```


## API参考

### WidgetCreationService

主要的组件创建服务类。

#### 初始化
```python
service = WidgetCreationService(config_path: str)
```

#### 方法
- `create_widgets_for_location(location: str, on_widget_created: Callable = None) -> List[QWidget]`
  - 创建指定位置的所有组件
  - `location`: 组件组名称
  - `on_widget_created`: 组件创建回调函数
  - 返回创建的组件列表

- `create_widget(module_path: str, class_name: str, params: Dict = None, strategy_name: str = None) -> QWidget`
  - 创建单个组件
  - `module_path`: 组件类文件路径
  - `class_name`: 组件类名
  - `params`: 初始化参数
  - `strategy_name`: 使用的策略名称
  - 返回创建的组件实例

- `register_strategy(name: str, strategy: WidgetCreationStrategy)`
  - 注册新的组件创建策略
  - `name`: 策略名称
  - `strategy`: 策略实例

### WidgetCreationStrategy

组件创建策略的基类。

#### 方法
- `can_handle(widget_class: Type) -> bool`
  - 检查是否可以处理该组件类
  - 返回是否可以处理

- `create_widget(widget_class: Type, params: Dict = None) -> QWidget`
  - 创建组件实例
  - 返回创建的组件

## 最佳实践

1. 配置文件组织
   - 按功能模块分组组织组件
   - 使用优先级控制组件显示顺序
   - 合理使用组件参数配置

2. 策略使用
   - 为不同类型的组件创建专门的策略
   - 策略类保持单一职责
   - 适当复用已有策略

## 贡献指南

1. Fork 本仓库
2. 创建你的特性分支：`git checkout -b feature/my-new-feature`
3. 提交你的改动：`git commit -am 'Add some feature'`
4. 推送到分支：`git push origin feature/my-new-feature`
5. 提交 Pull Request

在提交 PR 之前，请确保：
- 所有测试都通过
- 新功能有适当的测试覆盖
- 文档已更新
- 代码符合项目的代码风格

## 许可证

MIT License


### 1. 配置文件结构

配置文件使用YAML格式，主要包含以下部分：

```yaml
widget_system:
  # 全局配置
  config:
    default_group_enabled: true    # 默认组是否启用
    default_widget_enabled: true   # 默认组件是否启用

  # 组件创建策略配置
  strategies:
    - name: "QWidgetStrategy"      # 策略名称
      description: "策略描述"      # 策略描述
      enabled: true               # 是否启用
      path: "path/to/strategy.py" # 策略类文件路径
      class: StrategyClassName    # 策略类名

  # 组件组配置
  groups:
    group_name:                   # 组名称
      enabled: true              # 是否启用
      description: "组描述"      # 组描述
      widgets:                   # 组内组件列表
        widget_name:             # 组件名称
          enabled: true          # 是否启用
          path: "path/to/widget.py" # 组件类文件路径
          class: WidgetClassName # 组件类名
          priority: 0            # 显示优先级（数字越小优先级越高）
          description: "组件描述" # 组件描述
          strategy: "策略名称"    # 使用的创建策略
          params:                # 组件初始化参数
            param1: value1
            param2: value2
```

### 2. 组件加载器

使用 `WidgetCreationService` 来加载和创建组件：

```python
from modular_qtwidgets import WidgetCreationService

# 初始化服务
service = WidgetCreationService("config.yaml")

# 为特定位置创建组件
def on_widget_created(widget, widget_name, widget_config):
    """组件创建回调函数
    Args:
        widget: 创建的组件实例
        widget_name: 配置中的组件名称
        widget_config: 组件的配置信息
    """
    # 处理新创建的组件
    pass

# 创建指定位置的所有组件
widgets = service.create_widgets_for_location("group_name", on_widget_created)
```

### 3. 组件创建策略

创建自定义组件策略：

```python
from modular_qtwidgets import WidgetCreationStrategy
from PySide6.QtWidgets import QWidget

class CustomWidgetStrategy(WidgetCreationStrategy):
    def can_handle(self, widget_class: Type) -> bool:
        """检查是否可以处理该组件类"""
        return issubclass(widget_class, QWidget)

    def create_widget(self, widget_class: Type, params: Dict[str, Any] = None) -> QWidget:
        """创建组件实例"""
        if params is None:
            params = {}
        return widget_class(**params)

# 注册策略
service.register_strategy("CustomStrategy", CustomWidgetStrategy())
```

## 使用场景

### 1. 在主窗口中挂载配置的组件

如果你有一个主窗口，想要在其中的垂直布局中加载配置的组件，可以这样做：

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from modular_qtwidgets import WidgetCreationService

class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_widgets()
    
    def setup_ui(self):
        # 创建主布局
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # 创建滚动区域（可选，用于内容超出窗口时）
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        # 创建容器组件
        self.container = QWidget()
        self.scroll_area.setWidget(self.container)
        self.container_layout = QVBoxLayout(self.container)
        
        # 在底部添加弹性空间（可选，使组件靠上对齐）
        self.container_layout.addStretch()
    
    def load_widgets(self):
        try:
            # 创建组件服务
            service = WidgetCreationService("config.yaml")
            
            # 定义组件创建回调
            def on_widget_created(widget, widget_name, widget_config):
                # 将新组件插入到弹性空间之前
                self.container_layout.insertWidget(
                    self.container_layout.count() - 1,  # 插入到最后一个项目（弹性空间）之前
                    widget
                )
            
            # 创建指定位置的所有组件
            widgets = service.create_widgets_for_location(
                "your_group_name",  # 配置文件中定义的组名
                on_widget_created
            )
            
            if not widgets:
                # 处理没有组件的情况
                pass
                
        except Exception as e:
            # 处理错误情况
            pass
```

这个实现提供了以下功能：

1. **滚动支持**：当组件总高度超过窗口高度时，可以滚动查看
2. **自动布局**：组件会自动垂直排列
3. **靠上对齐**：通过底部的弹性空间，组件会靠上对齐
4. **动态加载**：组件是根据配置动态创建的

配置文件示例：

```yaml
widget_system:
  config:
    default_group_enabled: true
    default_widget_enabled: true
  
  strategies:
    - name: "QWidgetStrategy"
      enabled: true
      path: "path/to/strategies.py"
      class: QtWidgetStrategy
  
  groups:
    your_group_name:
      enabled: true
      description: "Your group description"
      widgets:
        widget1:
          enabled: true
          path: "path/to/widget1.py"
          class: Widget1Class
          priority: 0
          strategy: "QWidgetStrategy"
          params:
            param1: value1
        widget2:
          enabled: true
          path: "path/to/widget2.py"
          class: Widget2Class
          priority: 1
          strategy: "QWidgetStrategy"
          params:
            param2: value2
```

注意事项：
1. 组件会按照 `priority` 值从小到大的顺序创建和添加
2. 每个组件的具体参数在 `params` 中定义
3. 确保配置文件中的路径是正确的
4. 可以通过 `enabled` 字段控制组件是否加载

## 本地开发和安装

如果你是从 GitHub 克隆此仓库进行开发，请按照以下步骤操作：

1. 克隆仓库：
   ```bash
   git clone <repository_url>
   cd modular_qtwidgets
   ```

2. 创建并激活虚拟环境（推荐）：
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Linux/macOS
   python -m venv .venv
   source .venv/bin/activate
   ```

3. 安装开发依赖：
   ```bash
   # 安装基本依赖
   pip install -e .

   # 安装测试依赖
   pip install -e ".[test]"
   ```

## 运行测试

本项目使用 pytest 进行测试。测试套件包括单元测试和集成测试，涵盖了以下方面：

1. **组件创建服务测试**：
   - 服务初始化
   - 策略注册
   - 组件创建
   - 回调函数
   - 错误处理

2. **组件策略测试**：
   - QWidget 类型检查
   - 参数处理
   - 错误处理

3. **集成测试**：
   - 主窗口集成
   - 组件创建顺序

运行测试：
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/unit/test_widget_creation_service.py

# 运行带覆盖率报告的测试
pytest --cov=modular_qtwidgets

# 运行特定测试用例
pytest tests/unit/test_widget_creation_service.py::test_service_initialization
```

### 编写新测试

如果你要为项目添加新的测试，请遵循以下规则：

1. **测试文件组织**：
   - 单元测试放在 `tests/unit/` 目录下
   - 集成测试放在 `tests/integration/` 目录下
   - 测试固件放在 `tests/fixtures/` 目录下

2. **命名约定**：
   - 测试文件名以 `test_` 开头
   - 测试函数名以 `test_` 开头
   - 测试类名以 `Test` 开头

3. **固件使用**：
   - 使用 `conftest.py` 定义共享固件
   - 使用 `@pytest.fixture` 装饰器定义测试固件
   - Qt 应用程序使用全局 `qapp` 固件

示例：
```python
import pytest
from PySide6.QtWidgets import QWidget
from modular_qtwidgets import WidgetCreationService

def test_widget_creation(widget_service, qapp):
    """测试组件创建"""
    widgets = widget_service.create_widgets_for_location("test_group")
    assert len(widgets) > 0
    assert isinstance(widgets[0], QWidget)
```

## API参考

### WidgetCreationService

主要的组件创建服务类。

#### 初始化
```python
service = WidgetCreationService(config_path: str)
```

#### 方法
- `create_widgets_for_location(location: str, on_widget_created: Callable = None) -> List[QWidget]`
  - 创建指定位置的所有组件
  - `location`: 组件组名称
  - `on_widget_created`: 组件创建回调函数
  - 返回创建的组件列表

- `create_widget(module_path: str, class_name: str, params: Dict = None, strategy_name: str = None) -> QWidget`
  - 创建单个组件
  - `module_path`: 组件类文件路径
  - `class_name`: 组件类名
  - `params`: 初始化参数
  - `strategy_name`: 使用的策略名称
  - 返回创建的组件实例

- `register_strategy(name: str, strategy: WidgetCreationStrategy)`
  - 注册新的组件创建策略
  - `name`: 策略名称
  - `strategy`: 策略实例

### WidgetCreationStrategy

组件创建策略的基类。

#### 方法
- `can_handle(widget_class: Type) -> bool`
  - 检查是否可以处理该组件类
  - 返回是否可以处理

- `create_widget(widget_class: Type, params: Dict = None) -> QWidget`
  - 创建组件实例
  - 返回创建的组件

## 最佳实践

1. 配置文件组织
   - 按功能模块分组组织组件
   - 使用优先级控制组件显示顺序
   - 合理使用组件参数配置

2. 策略使用
   - 为不同类型的组件创建专门的策略
   - 策略类保持单一职责
   - 适当复用已有策略

## 贡献指南

1. Fork 本仓库
2. 创建你的特性分支：`git checkout -b feature/my-new-feature`
3. 提交你的改动：`git commit -am 'Add some feature'`
4. 推送到分支：`git push origin feature/my-new-feature`
5. 提交 Pull Request

在提交 PR 之前，请确保：
- 所有测试都通过
- 新功能有适当的测试覆盖
- 文档已更新
- 代码符合项目的代码风格

## 许可证

MIT License
