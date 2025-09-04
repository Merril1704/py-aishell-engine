"""
Main window for the PyQt GUI.
"""
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPlainTextEdit, QLineEdit, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from engine import CommandEngine

class TerminalWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.command_engine = CommandEngine()
        self.layout = QVBoxLayout(self)
        self.terminal = QPlainTextEdit(self)
        self.terminal.setReadOnly(True)
        self.terminal.setFont(QFont('Consolas', 12))
        self.terminal.setStyleSheet("background: #23272e; color: #e6e6e6; border-radius: 8px; padding: 8px;")
        self.input = QLineEdit(self)
        self.input.setFont(QFont('Consolas', 12))
        self.input.setStyleSheet("background: #2c313c; color: #e6e6e6; border-radius: 8px; padding: 6px;")
        self.input.setPlaceholderText("Enter command or natural language...")
        self.input.returnPressed.connect(self.handle_input)
        self.layout.addWidget(self.terminal)
        self.layout.addWidget(self.input)
        self.setLayout(self.layout)
        
        # Welcome message
        self.terminal.appendPlainText("Welcome to NL-Terminal!")
        self.terminal.appendPlainText("You can use natural language or direct commands.")
        self.terminal.appendPlainText("Examples: 'list files', 'show current directory', 'create folder test'")
        self.terminal.appendPlainText("-" * 60)

    def handle_input(self):
        cmd = self.input.text().strip()
        if not cmd:
            return
            
        self.terminal.appendPlainText(f"> {cmd}")
        
        try:
            # Use the Command Engine to process input
            success, output, error = self.command_engine.process_input(cmd)
            
            if success:
                if output:
                    self.terminal.appendPlainText(output)
                else:
                    self.terminal.appendPlainText("Command executed successfully (no output)")
            else:
                # Check if this is a confirmation prompt
                if "Are you sure" in error or "Confirm" in error:
                    # Show confirmation dialog
                    reply = QMessageBox.question(
                        self, 
                        'Confirmation Required',
                        error,
                        QMessageBox.Yes | QMessageBox.No,
                        QMessageBox.No
                    )
                    
                    if reply == QMessageBox.Yes:
                        # Re-execute with force (you might need to implement this)
                        self.terminal.appendPlainText("User confirmed. Executing command...")
                        # For now, just show that user confirmed
                        self.terminal.appendPlainText("(Command confirmation system not fully implemented yet)")
                    else:
                        self.terminal.appendPlainText("Command cancelled by user.")
                else:
                    # Regular error
                    self.terminal.appendPlainText(f"Error: {error}")
                    
        except Exception as e:
            self.terminal.appendPlainText(f"System Error: {str(e)}")
        
        self.input.clear()

    def closeEvent(self, event):
        """Clean up when closing"""
        self.command_engine.cleanup()
        event.accept()

class TerminalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NL-Terminal - AI Shell Engine")
        self.setGeometry(100, 100, 900, 600)
        self.terminal_widget = TerminalWidget(self)
        self.setCentralWidget(self.terminal_widget)
        self.setStyleSheet("background: #1a1d23;")

    def closeEvent(self, event):
        """Clean up when closing the main window"""
        if hasattr(self.terminal_widget, 'closeEvent'):
            self.terminal_widget.closeEvent(event)
        event.accept()

def run_terminal():
    import sys
    app = QApplication(sys.argv)
    window = TerminalWindow()
    window.show()
    sys.exit(app.exec_())

def start_gui():
    import sys
    app = QApplication(sys.argv if sys.argv else [])
    window = TerminalWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_terminal()
