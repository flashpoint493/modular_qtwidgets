from PySide6.QtWidgets import QFileDialog, QMessageBox, QLineEdit, QPushButton, QVBoxLayout, QWidget, QTextEdit, QHBoxLayout, QApplication
from PySide6.QtCore import QProcess
import os
import sys

class ScriptsLauncher(QWidget):
    def __init__(self, default_script_path=""):
        super().__init__()
        self.setup_ui(default_script_path)
        self.process = None

    def setup_ui(self, default_script_path):
        # Initialize your UI components here
        self.file_path_edit = QLineEdit(default_script_path)
        self.open_file_button = QPushButton('Open File')
        self.execute_button = QPushButton('Execute Script')
        self.output_text_edit = QTextEdit()
        self.output_text_edit.setReadOnly(True)

        # Connect signals
        self.open_file_button.clicked.connect(self.openFile)
        self.execute_button.clicked.connect(self.executeScript)

        # Create layouts
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_path_edit)
        file_layout.addWidget(self.open_file_button)
        file_layout.addWidget(self.execute_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(file_layout)
        main_layout.addWidget(self.output_text_edit)

        self.setLayout(main_layout)

    def openFile(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Script File",
            "",
            "Python Files (*.py);;All Files (*)"
        )
        if file_path:
            self.file_path_edit.setText(file_path)

    def executeScript(self):
        script_path = self.file_path_edit.text()
        if not script_path:
            QMessageBox.warning(self, "Warning", "Please select a script file first!")
            return
        
        if not os.path.exists(script_path):
            QMessageBox.warning(self, "Warning", "Selected file does not exist!")
            return

        # Create a new process if none exists
        if self.process is None:
            self.process = QProcess()
            self.process.readyReadStandardOutput.connect(self.handle_stdout)
            self.process.readyReadStandardError.connect(self.handle_stderr)
            self.process.finished.connect(self.process_finished)

        # Clear previous output
        self.output_text_edit.clear()
        
        # Start the process
        python_executable = sys.executable
        self.process.start(python_executable, [script_path])

    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode()
        self.output_text_edit.append(stdout)

    def handle_stderr(self):
        data = self.process.readAllStandardError()
        stderr = bytes(data).decode()
        self.output_text_edit.append(stderr)

    def process_finished(self, exit_code, exit_status):
        self.output_text_edit.append(f"\nProcess finished with exit code: {exit_code}")
        self.process = None  # Reset process

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScriptsLauncher()
    window.show()
    sys.exit(app.exec_())