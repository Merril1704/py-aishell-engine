"""
Main window for the PyQt GUI.
"""
from PyQt5.QtWidgets import QApplication, QMainWindow

def start_gui():
    app = QApplication([])
    window = QMainWindow()
    window.setWindowTitle('NL-Terminal')
    window.show()
    app.exec_()
