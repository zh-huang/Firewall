from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget, QTableWidget
from backend import IptablesManager
from .rule_widget import RuleWidget
from .app_widget import AppWidget
from .log_widget import LogWidget
from .monitor_widget import MonitorWidget

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.iptables_manager = IptablesManager()

    def initUI(self):
        self.setWindowTitle('My Firewall - 2153689')
        self.setGeometry(100, 100, 800, 600)
        
        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tabs.addTab(RuleWidget(), "Rule")
        self.tabs.addTab(AppWidget(), "App")
        self.tabs.addTab(LogWidget(), "Log")
        self.tabs.addTab(MonitorWidget(), "Monitor")
        layout.addWidget(self.tabs)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
