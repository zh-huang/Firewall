from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget, QTableWidget
from PyQt5.QtWidgets import QApplication
import sys
import subprocess

class RuleWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_rules(self):
        result = subprocess.run(['sudo', 'ufw', 'status', 'numbered'], capture_output=True, text=True)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('UFW Guardian')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tabs.addTab(RuleWidget(), "规则")
        self.tabs.addTab(RuleWidget(), "应用程序")
        self.tabs.addTab(RuleWidget(), "日志")
        self.tabs.addTab(RuleWidget(), "监控")
        layout.addWidget(self.tabs)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())