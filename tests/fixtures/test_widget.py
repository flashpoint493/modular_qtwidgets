from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class TestWidget(QWidget):
    """Test widget for unit tests."""
    
    def __init__(self, test_param: str = "", parent=None):
        super().__init__(parent)
        self.test_param = test_param
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the widget's UI."""
        layout = QVBoxLayout(self)
        self.label = QLabel(f"Test Widget: {self.test_param}")
        layout.addWidget(self.label)
