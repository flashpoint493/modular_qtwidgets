import pytest
import os
from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="session")
def qapp():
    """Create a QApplication instance for the entire test session."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    app.quit()

@pytest.fixture(scope="session")
def project_root():
    """返回项目根目录"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@pytest.fixture(scope="session")
def fixtures_dir(project_root):
    """返回测试固件目录"""
    return os.path.join(project_root, "tests", "fixtures")
