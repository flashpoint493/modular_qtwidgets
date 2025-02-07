from PySide6.QtWidgets import QMainWindow, QApplication
from ..view.vertical_container import VerticalContainerWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Tools Example")
        self.resize(800, 600)
        
        # Create and set the central widget
        self.central_widget = VerticalContainerWidget()
        self.setCentralWidget(self.central_widget)

if __name__ == "__main__":
    # Create the application object
    app = QApplication([])
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Start the event loop
    app.exec_()