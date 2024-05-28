from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QListWidget, QHBoxLayout
from backend import IptablesManager
import psutil


class MonitorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.update_connections()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.connections_list = QListWidget()
        layout.addWidget(self.connections_list)

        self.button_layout = QHBoxLayout()
        
        self.save_button = QPushButton('Refresh')
        self.save_button.clicked.connect(self.update_connections)
        self.button_layout.addWidget(self.save_button)
        
        layout.addLayout(self.button_layout)
        
        self.setLayout(layout)
        
    def update_connections(self):
        self.connections_list.clear()
        connections = psutil.net_connections(kind='inet')
        for conn in connections:
            if conn.status == psutil.CONN_ESTABLISHED:
                local_address = ":".join([conn.laddr.ip, str(conn.laddr.port)])
                remote_address = ":".join([conn.raddr.ip, str(conn.raddr.port)]) if conn.raddr else "UNKNOWN"
                self.connections_list.addItem(f"Local: {local_address} -> Remote: {remote_address}")