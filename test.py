import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton

class FirewallApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Firewall Manager')
        self.setGeometry(100, 100, 600, 400)

        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)

        self.refreshButton = QPushButton('Refresh', self)
        self.refreshButton.clicked.connect(self.refreshConnections)

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.refreshButton)

        self.setLayout(layout)

    def refreshConnections(self):
        connections = self.getNetworkConnections()
        self.textEdit.clear()
        self.textEdit.append("Network Connections:\n")
        self.textEdit.append(connections)

    def getNetworkConnections(self):
        try:
            # Get network connections using netstat command
            result = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return "Error: " + str(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    firewallApp = FirewallApp()
    firewallApp.show()
    sys.exit(app.exec_())
