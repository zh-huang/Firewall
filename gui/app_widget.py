from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout
from backend import AppManager

class AppWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.appManager = AppManager()
        self.refreshConnections()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.button_layout = QHBoxLayout()

        self.add_button = QPushButton('Refersh')
        self.add_button.clicked.connect(self.refreshConnections)
        self.button_layout.addWidget(self.add_button)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

    def refreshConnections(self):
        self.table.clear()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['User', 'Program', 'PID', 'FD', 'Proto', 'Local Address', 'Foreign Address', 'State'])
        
        connections = self.appManager.getNetworkConnections()
        self.updateTable(connections)

    def updateTable(self, connections):
        self.table.setRowCount(len(connections) - 1)
        for i, line in enumerate(connections[1:]):
            parts = self.appManager.parseConnectionLine(line)
            for j, part in enumerate(parts):
                self.table.setItem(i, j, QTableWidgetItem(part))
    
