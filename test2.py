import sys
import subprocess
import re
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem

class FirewallApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Firewall Manager')
        self.setGeometry(100, 100, 1000, 600)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(['Proto', 'Local Address', 'Foreign Address', 'State', 'User', 'Program', 'PID', 'FD'])

        self.refreshButton = QPushButton('Refresh', self)
        self.refreshButton.clicked.connect(self.refreshConnections)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.refreshButton)

        self.setLayout(layout)

    def refreshConnections(self):
        connections = self.getNetworkConnections()
        self.updateTable(connections)

    def getNetworkConnections(self):
        try:
            result = subprocess.run(['ss', '-tulnp'], capture_output=True, text=True)
            return result.stdout.splitlines()
        except Exception as e:
            return ["Error: " + str(e)]

    def updateTable(self, connections):
        self.tableWidget.setRowCount(len(connections) - 1)  # First line is the header
        for i, line in enumerate(connections[1:]):  # Skip the header
            parts = self.parseConnectionLine(line)
            for j, part in enumerate(parts):
                self.tableWidget.setItem(i, j, QTableWidgetItem(part))

    def parseConnectionLine(self, line):
        # Split the line into parts
        parts = re.split(r'\s+', line)
        if parts[0] in ('tcp', 'udp'):
            proto = parts[0]
            local_address = parts[3]
            foreign_address = parts[4]
            state = parts[1] if proto == 'tcp' else ''
            pid_info = ' '.join(parts[6:]) if len(parts) > 6 else ''
            user, program, pid, fd = self.parsePidInfo(pid_info)
            return [proto, local_address, foreign_address, state, user, program, pid, fd]
        return ['', '', '', '', '', '', '', '']

    def parsePidInfo(self, pid_info):
        user = program = pid = fd = ''
        pid_pattern = re.compile(r'users:\(\("([^"]+)",pid=(\d+),fd=(\d+)\)\)')
        user_pattern = re.compile(r'^(\S+)')

        user_match = user_pattern.search(pid_info)
        pid_match = pid_pattern.search(pid_info)

        if user_match:
            user = user_match.group(1)
        if pid_match:
            program = pid_match.group(1)
            pid = pid_match.group(2)
            fd = pid_match.group(3)

        return user, program, pid, fd

if __name__ == '__main__':
    app = QApplication(sys.argv)
    firewallApp = FirewallApp()
    firewallApp.show()
    sys.exit(app.exec_())
